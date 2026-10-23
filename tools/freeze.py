"""A dataset frozen: every file's path, size and sha256, the folders' totals and one tree hash.

Source: the thread "Frozen dataset manifests", 2026-10-23, the owner's ask of that day: every
dataset put on the grid comes with a metadata file that freezes its directory tree and hashes it,
so the copy is shown identical, and its files, its folders and its size can be read at once and in
detail without scanning the data again.

A dataset is read once, when it is frozen. `freeze` walks the dataset's folder on the grid (the
record's grid_path, or the promoter's shared/<id>) and writes two files into it:

- FROZEN.files.tsv.gz, one line per file, `sha256 TAB bytes TAB path`, sorted by the path's UTF-8
  bytes, the path relative to the folder with / between its parts;
- FROZEN.json, the summary: the totals, the tree's sha256, which is the sha256 of the file list
  uncompressed, so one hash stands for every byte and every name, each folder down to a depth with
  its files, bytes and its own tree hash, the largest files and the counts by extension.

FROZEN.json is small, and its public copy, with no name below the top folders (public_copy),
lives in the repository as frozen/<id>.json, where GitHub, the census and a session read a
dataset's size and outline with no grid access at all; the record's
`measured` carries its bytes, files and tree_sha256 (`measured` below prints that block), and
`python3 tools/census.py check` holds the two to each other. The file list stays beside the data,
since a set of a million DICOM slices lists to tens of megabytes.

`verify` reads the folder again against the list: `--quick` compares names and sizes alone, which
takes the time of a directory walk, and the default hashes every file again. Either names each
file missing, added or changed, and exits 1 on any. `show` prints the folders and their sizes from
the summary, or from the file list for any folder at any depth, without touching the data.

A folder's own tree hash is the sha256 of the lines of the files under it, their paths taken from
that folder, so two copies of one subtree, or one subtree before and after a move, have one hash.
Nothing is followed through a symbolic link: a link is listed with the hash of its target's text
and the size -1, so a link that comes to point elsewhere changes the tree's hash. The promoter's
PROMOTED.json, the freeze's own two files and its checkpoint, at the folder's top, and a folder
.incoming-* the promoter is still filling, are left out, since they are written beside the data
and are not the data.

A long freeze survives its wall time: each file hashed is appended to .FROZEN.partial as it is
read, and a freeze started again takes a file from there while its size and modification time are
unchanged, so a requeued job carries on where the last one stopped; the checkpoint is removed when
the freeze is written. `--workers N` hashes N files at once, since a network filesystem gives a
reader more when several files are read side by side.

It runs on the grid's own python3, which on its EL7 nodes may be as old as 3.6, so it uses nothing
newer and only the standard library, as tools/promote.py does.

    python3 tools/freeze.py freeze DIR --id ID [--workers N] [--depth N] [--copy frozen/ID.json] [--out DIR]
    python3 tools/freeze.py verify DIR [--quick] [--workers N] [--out DIR]
    python3 tools/freeze.py show DIR_OR_FROZEN_JSON [--under PATH] [--depth N]
    python3 tools/freeze.py measured FROZEN_JSON
    python3 tools/freeze.py plan
    python3 tools/freeze.py check [--root DIR]
    python3 tools/freeze.py bundle COPIES_DIR      the git tree that carries the public copies back
    python3 tools/freeze.py apply COPIES_DIR [--root DIR]

The public copies a freeze job keeps under its home come back by a branch of their own,
freeze-report: grid/freeze.sh report, which the grid gate's word freeze report runs, sends the tree
`bundle` prints for every copy that passes the public copy's rules, as one commit with no parent,
and a session then runs `apply` on a checkout of that branch's frozen/ folder, which puts each copy
under frozen/ and writes its measured block into the record, for a pull request that the census
and the check read like any other. The tree hash cannot come back through the gate's log, which
hides every long run of letters and digits, so it comes this way.
"""

import argparse
import gzip
import hashlib
import io
import json
import os
import re
import stat
import sys
import time
from multiprocessing import Pool

FORMAT = "spine-datasets/frozen 1"
SUMMARY = "FROZEN.json"
FILE_LIST = "FROZEN.files.tsv.gz"
CHECKPOINT = ".FROZEN.partial"
# Written beside the data at its top, never part of it.
LEFT_OUT = (SUMMARY, FILE_LIST, CHECKPOINT, "PROMOTED.json")
INCOMING = re.compile(r"^\.incoming-")
LINK_BYTES = -1
SHA256_SHAPE = re.compile(r"^[0-9a-f]{64}$")
ID_SHAPE = re.compile(r"^[a-z0-9_]+$")
DEFAULT_DEPTH = 2
# The summary stays small enough for git: past this many folders it keeps the shallower ones.
MAX_FOLDERS = 2000
LARGEST = 10
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Reading the tree.

def walk(top):
    """Every file and link under top, as (relative path, absolute path, lstat), in no set order."""
    found = []
    pending = [""]
    while pending:
        relative = pending.pop()
        folder = os.path.join(top, relative) if relative else top
        for entry in os.scandir(folder):
            if not relative and (entry.name in LEFT_OUT or INCOMING.match(entry.name)):
                continue
            path = entry.name if not relative else relative + "/" + entry.name
            if "\n" in path or "\t" in path:
                raise ValueError("a name with a tab or a newline cannot be listed: %r" % path)
            info = entry.stat(follow_symlinks=False)
            if stat.S_ISDIR(info.st_mode):
                pending.append(path)
            elif stat.S_ISREG(info.st_mode) or stat.S_ISLNK(info.st_mode):
                found.append((path, entry.path, info))
    return found


def digest_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def hash_one(item):
    """(path, sha256, bytes) for one file, or for a link the hash of where it points."""
    path, absolute, is_link, size = item
    if is_link:
        return path, hashlib.sha256(os.readlink(absolute).encode("utf-8", "surrogateescape")).hexdigest(), LINK_BYTES
    return path, digest_of(absolute), size


def stamp(info):
    return "%d:%d" % (info.st_size, int(info.st_mtime))


# The checkpoint a requeued job carries on from.

def read_checkpoint(out):
    done = {}
    path = os.path.join(out, CHECKPOINT)
    if not os.path.exists(path):
        return done
    with io.open(path, encoding="utf-8", errors="surrogateescape") as handle:
        for line in handle:
            parts = line.rstrip("\n").split("\t", 3)
            if len(parts) == 4 and SHA256_SHAPE.match(parts[0]):
                done[parts[3]] = (parts[0], int(parts[1]), parts[2])
    return done


def hashed(out, found, workers=1, log=None):
    """{path: (sha256, bytes)} for every file found, from the checkpoint in out where it still holds."""
    done = read_checkpoint(out)
    result = {}
    todo = []
    for path, absolute, info in found:
        is_link = stat.S_ISLNK(info.st_mode)
        kept = done.get(path)
        if kept and kept[2] == stamp(info):
            result[path] = (kept[0], kept[1])
        else:
            todo.append((path, absolute, is_link, info.st_size))
    stamps = dict((path, stamp(info)) for path, _absolute, info in found)
    pool = Pool(workers) if workers > 1 and len(todo) > 1 else None
    try:
        results = pool.imap_unordered(hash_one, todo, 16) if pool else map(hash_one, todo)
        with io.open(os.path.join(out, CHECKPOINT), "a", encoding="utf-8", errors="surrogateescape") as out:
            for number, (path, digest, size) in enumerate(results, 1):
                result[path] = (digest, size)
                out.write("%s\t%d\t%s\t%s\n" % (digest, size, stamps[path], path))
                if number % 1000 == 0:
                    out.flush()
                    if log:
                        log("%d of %d files hashed" % (number, len(todo)))
    finally:
        if pool:
            pool.terminate()
    return result


# What the freeze writes.

def sort_key(path):
    return path.encode("utf-8", "surrogateescape")


def lines_of(files, under=""):
    """The file list's lines for the files under one folder, paths taken from that folder."""
    prefix = under + "/" if under else ""
    lines = []
    for path in sorted(files, key=sort_key):
        if path.startswith(prefix):
            digest, size = files[path]
            lines.append("%s\t%d\t%s\n" % (digest, size, path[len(prefix):]))
    return "".join(lines).encode("utf-8", "surrogateescape")


def tree_digest(files, under=""):
    return hashlib.sha256(lines_of(files, under)).hexdigest()


def folders_of(files, depth):
    """{folder: [files, bytes]} for every folder down to depth, sizes counting every file below."""
    totals = {}
    for path, (_digest, size) in files.items():
        parts = path.split("/")[:-1]
        for level in range(1, min(len(parts), depth) + 1):
            entry = totals.setdefault("/".join(parts[:level]), [0, 0])
            entry[0] += 1
            entry[1] += max(size, 0)
    return totals


def folder_rows(files, depth):
    while True:
        totals = folders_of(files, depth)
        if len(totals) <= MAX_FOLDERS or depth <= 1:
            break
        depth -= 1
    by_folder = {}
    for path in sorted(files, key=sort_key):
        parts = path.split("/")[:-1]
        for level in range(1, min(len(parts), depth) + 1):
            by_folder.setdefault("/".join(parts[:level]), []).append(path)
    rows = []
    for folder in sorted(totals, key=sort_key):
        within = dict((path, files[path]) for path in by_folder[folder])
        count, size = totals[folder]
        rows.append({"path": folder, "files": count, "bytes": size, "tree_sha256": tree_digest(within, folder)})
    return rows, depth


def extension_of(path):
    name = path.rsplit("/", 1)[-1].lower()
    for double in (".nii.gz", ".tar.gz", ".mha.gz", ".tsv.gz"):
        if name.endswith(double):
            return double
    return os.path.splitext(name)[1] or "(none)"


def shape_of(files):
    """How many folders and files sit at each depth, the tree's outline with no name in it."""
    folders, at_depth = {}, {}
    for path in files:
        parts = path.split("/")
        at_depth[len(parts)] = at_depth.get(len(parts), 0) + 1
        for level in range(1, len(parts)):
            folders.setdefault(level, set()).add("/".join(parts[:level]))
    deepest = max(list(at_depth) + [0])
    return [{"depth": level, "folders": len(folders.get(level, ())), "files": at_depth.get(level, 0)}
            for level in range(1, deepest + 1)]


def summary_of(ident, top, files, depth=DEFAULT_DEPTH, frozen_at=None):
    sizes = [size for _digest, size in files.values() if size >= 0]
    extensions = {}
    for path, (_digest, size) in files.items():
        entry = extensions.setdefault(extension_of(path), [0, 0])
        entry[0] += 1
        entry[1] += max(size, 0)
    rows, depth = folder_rows(files, depth)
    largest = sorted(((size, path) for path, (_d, size) in files.items()), key=lambda pair: (-pair[0], sort_key(pair[1])))
    return {
        "format": FORMAT,
        "id": ident,
        "root": os.path.abspath(top),
        "frozen_at": frozen_at or time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "files": len(files),
        "links": sum(1 for _d, size in files.values() if size == LINK_BYTES),
        "bytes": sum(sizes),
        "tree_sha256": tree_digest(files),
        "file_list": FILE_LIST,
        "depth": depth,
        "shape": shape_of(files),
        "folders": rows,
        "largest": [{"path": path, "bytes": size} for size, path in largest[:LARGEST]],
        "extensions": dict((name, {"files": n, "bytes": b}) for name, (n, b) in sorted(extensions.items())),
    }


# Extensions the public copy names; any other is counted under (other), since a name with a dot
# in it, a subject's for one, would otherwise show its end.
KNOWN_EXTENSIONS = frozenset((
    "(none)", ".nii.gz", ".tar.gz", ".mha.gz", ".tsv.gz", ".nii", ".dcm", ".dicom", ".ima", ".mha", ".mhd",
    ".raw", ".nrrd", ".npy", ".npz", ".h5", ".hdf5", ".mat", ".pkl", ".pt", ".png", ".jpg", ".jpeg", ".tif",
    ".tiff", ".bmp", ".gif", ".mp4", ".avi", ".mkv", ".mov", ".zip", ".tar", ".gz", ".tgz", ".7z", ".rar",
    ".json", ".csv", ".tsv", ".txt", ".xml", ".yaml", ".yml", ".md", ".pdf", ".xlsx", ".xls", ".vtk",
    ".stl", ".obj", ".ply", ".py", ".sh", ".log", ".bin", ".dat", ".parquet",
))
# A set with more top folders than this most likely keeps a folder per subject at its top.
MAX_PUBLIC_FOLDERS = 12


def public_copy(summary):
    """The summary as the public repository keeps it, frozen/<id>.json: the totals, the tree hash,
    the outline by depth and the counts by known extension, with the top folders only where there
    are few of them, and no other name, since a set held under an agreement may name its subjects
    in its folders and files."""
    copy = dict((key, value) for key, value in summary.items()
                if key not in ("folders", "largest", "root", "extensions"))
    top = [row for row in summary.get("folders", []) if "/" not in row["path"]]
    copy["folders"] = top if len(top) <= MAX_PUBLIC_FOLDERS else []
    copy["depth"] = 1
    extensions = {}
    for name, counts in summary.get("extensions", {}).items():
        entry = extensions.setdefault(name if name in KNOWN_EXTENSIONS else "(other)", {"files": 0, "bytes": 0})
        entry["files"] += counts["files"]
        entry["bytes"] += counts["bytes"]
    copy["extensions"] = extensions
    return copy


def write_read_only(path, data):
    if os.path.exists(path):
        os.chmod(path, 0o644)
    with open(path + ".tmp", "wb") as handle:
        handle.write(data)
    os.rename(path + ".tmp", path)
    os.chmod(path, 0o444)


def summary_bytes(summary):
    return (json.dumps(summary, indent=1, sort_keys=True, ensure_ascii=True) + "\n").encode("ascii")


def write_frozen(out, summary, files):
    """FROZEN.files.tsv.gz then FROZEN.json, both read-only; the gzip carries no time or name, so
    one tree always gives one file."""
    buffer = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=buffer, mtime=0) as handle:
        handle.write(lines_of(files))
    write_read_only(os.path.join(out, FILE_LIST), buffer.getvalue())
    write_read_only(os.path.join(out, SUMMARY), summary_bytes(summary))


def freeze(top, ident, workers=1, depth=DEFAULT_DEPTH, known=None, log=None, out=None):
    """Freeze one dataset's folder, writing into out (the folder itself unless given, for a folder
    the freeze may not write); known is {path: (sha256, bytes)} a caller has just read itself, as
    the promoter has, so those files are not read a second time."""
    out = out or top
    found = walk(top)
    if known:
        reuse = [item for item in found if item[0] in known and known[item[0]][1] == item[2].st_size
                 and not stat.S_ISLNK(item[2].st_mode)]
        reused = set(item[0] for item in reuse)
        rest = [item for item in found if item[0] not in reused]
        files = dict((path, known[path]) for path, _a, _i in reuse)
        files.update(hashed(out, rest, workers, log))
    else:
        files = hashed(out, found, workers, log)
    summary = summary_of(ident, top, files, depth)
    write_frozen(out, summary, files)
    try:
        os.remove(os.path.join(out, CHECKPOINT))
    except OSError:
        pass
    return summary


# Reading a freeze back.

def read_file_list(out):
    files = {}
    with gzip.open(os.path.join(out, FILE_LIST), "rb") as handle:
        for raw in handle:
            digest, size, path = raw.decode("utf-8", "surrogateescape").rstrip("\n").split("\t", 2)
            files[path] = (digest, int(size))
    return files


def read_summary(path):
    with io.open(path, encoding="ascii") as handle:
        return json.load(handle)


def compare(expected, actual):
    """(missing, added, changed) between two {path: (sha256, bytes)}; a None hash compares size alone."""
    missing = sorted((p for p in expected if p not in actual), key=sort_key)
    added = sorted((p for p in actual if p not in expected), key=sort_key)
    changed = []
    for path in sorted(set(expected) & set(actual), key=sort_key):
        (want_digest, want_size), (got_digest, got_size) = expected[path], actual[path]
        if want_size != got_size or (got_digest is not None and got_digest != want_digest):
            changed.append(path)
    return missing, added, changed


def verify(top, quick=False, workers=1, out=None):
    out = out or top
    expected = read_file_list(out)
    summary = read_summary(os.path.join(out, SUMMARY))
    problems = []
    with gzip.open(os.path.join(out, FILE_LIST), "rb") as handle:
        if hashlib.sha256(handle.read()).hexdigest() != summary["tree_sha256"]:
            problems.append("the file list is not the one FROZEN.json's tree_sha256 names")
    found = walk(top)
    if quick:
        actual = dict((path, (None, LINK_BYTES if stat.S_ISLNK(info.st_mode) else info.st_size))
                      for path, _a, info in found)
    else:
        todo = [(path, absolute, stat.S_ISLNK(info.st_mode), info.st_size) for path, absolute, info in found]
        pool = Pool(workers) if workers > 1 and len(todo) > 1 else None
        try:
            results = pool.imap_unordered(hash_one, todo, 16) if pool else map(hash_one, todo)
            actual = dict((path, (digest, size)) for path, digest, size in results)
        finally:
            if pool:
                pool.terminate()
    missing, added, changed = compare(expected, actual)
    problems += ["missing: %s" % p for p in missing]
    problems += ["added: %s" % p for p in added]
    problems += ["changed: %s" % p for p in changed]
    return problems


def measured_of(summary):
    """The block a record's `measured` takes from a freeze."""
    return {
        "bytes": summary["bytes"],
        "files": summary["files"],
        "tree_sha256": summary["tree_sha256"],
        "frozen": summary["frozen_at"][:10],
        "by": "tools/freeze.py",
    }


def size_text(value):
    for unit, scale in (("TB", 10 ** 12), ("GB", 10 ** 9), ("MB", 10 ** 6), ("kB", 10 ** 3)):
        if value >= scale:
            return "%.1f %s" % (value / float(scale), unit)
    return "%d B" % value


def show_rows(summary, files=None, under="", depth=None):
    """The table `show` prints: from the summary's folders, or from the file list when asked for a
    folder or a depth the summary does not keep."""
    if files is None:
        rows = [(row["path"], row["files"], row["bytes"]) for row in summary["folders"]]
    else:
        prefix = under + "/" if under else ""
        within = dict((p[len(prefix):], v) for p, v in files.items() if p.startswith(prefix))
        totals = folders_of(within, depth or 1)
        rows = [(prefix + folder, n, b) for folder, (n, b) in sorted(totals.items(), key=lambda kv: sort_key(kv[0]))]
    if under:
        inside = [size for path, (_d, size) in files.items() if path.startswith(under + "/")]
        head = [(under, len(inside), sum(max(size, 0) for size in inside))]
    else:
        head = [("(all)", summary["files"], summary["bytes"])]
    return head + rows


# The repository's copies under frozen/.

def check_repository(root=ROOT):
    """frozen/<id>.json against its record: a summary that holds together, a record that exists, and
    a record whose measured block names the same bytes, files and tree hash."""
    problems = []
    folder = os.path.join(root, "frozen")
    if not os.path.isdir(folder):
        return problems
    for name in sorted(os.listdir(folder)):
        if not name.endswith(".json"):
            if name != "README.md":
                problems.append("frozen/%s: only <id>.json and README.md belong here" % name)
            continue
        ident = name[:-5]
        try:
            summary = read_summary(os.path.join(folder, name))
        except (ValueError, UnicodeDecodeError) as error:
            problems.append("frozen/%s: not ASCII JSON (%s)" % (name, error))
            continue
        problems += ["frozen/%s: %s" % (name, p) for p in summary_problems(summary, ident)]
        record_path = os.path.join(root, "datasets", name)
        if not os.path.exists(record_path):
            problems.append("frozen/%s: no record datasets/%s" % (name, name))
            continue
        with io.open(record_path, encoding="utf-8") as handle:
            measured = json.load(handle).get("measured") or {}
        for field in ("bytes", "files", "tree_sha256"):
            if measured.get(field) != summary.get(field):
                problems.append("datasets/%s: measured.%s is %r, the freeze says %r"
                                % (name, field, measured.get(field), summary.get(field)))
    return problems


def summary_problems(summary, ident):
    problems = []
    if summary.get("format") != FORMAT:
        problems.append("format is not %r" % FORMAT)
    if summary.get("id") != ident or not ID_SHAPE.match(ident):
        problems.append("id is not the file's name")
    if not SHA256_SHAPE.match(str(summary.get("tree_sha256", ""))):
        problems.append("tree_sha256 is not 64 hex digits")
    for field in ("files", "bytes"):
        if not isinstance(summary.get(field), int) or summary[field] < 0:
            problems.append("%s is not a whole number" % field)
    for row in summary.get("folders", []):
        if row.get("bytes", 0) > summary.get("bytes", 0) or row.get("files", 0) > summary.get("files", 0):
            problems.append("folder %s holds more than the whole" % row.get("path"))
        if "/" in str(row.get("path", "")):
            problems.append("folder %s is below the top; the public copy names none" % row.get("path"))
    if "largest" in summary or "root" in summary:
        problems.append("the public copy keeps no file names and no root (tools/freeze.py public_copy)")
    if len(summary.get("folders", [])) > MAX_PUBLIC_FOLDERS:
        problems.append("the public copy names at most %d top folders" % MAX_PUBLIC_FOLDERS)
    unknown = sorted(set(summary.get("extensions", {})) - KNOWN_EXTENSIONS - set(["(other)"]))
    if unknown:
        problems.append("extensions the public copy does not name: %s" % ", ".join(unknown))
    if sum(level.get("files", 0) for level in summary.get("shape", [])) != summary.get("files"):
        problems.append("shape's files do not add up to files")
    return problems


# What is still to freeze.

SHARED_TREE = "/rs/rs_grp_oschome/shared/datasets/"
GRID_PATH = re.compile(r"^/rs/[^;\s]+$")


def folder_to_freeze(grid_path):
    """A set's folder as the freeze takes it: the promoter's shared/<id> for its raw/, so the paths
    read raw/... as the manifest and PROMOTED.json have them, else the record's grid_path itself;
    None for a grid_path that names several folders or says more than a path, frozen by hand."""
    path = grid_path.strip().rstrip("/")
    if not GRID_PATH.match(path):
        return None
    if path.startswith(SHARED_TREE) and path.endswith("/raw"):
        return os.path.dirname(path)
    return path


def plan(root=ROOT):
    """(id, folder, bytes the record states or None) for every set on the grid not yet frozen."""
    found = []
    folder = os.path.join(root, "datasets")
    for name in sorted(os.listdir(folder)):
        if not name.endswith(".json"):
            continue
        with io.open(os.path.join(folder, name), encoding="utf-8") as handle:
            record = json.load(handle)
        measured = record.get("measured") if isinstance(record.get("measured"), dict) else {}
        if not record.get("grid_path") or measured.get("tree_sha256"):
            continue
        if record.get("status") not in ("fetched", "held"):
            continue
        found.append((record["id"], folder_to_freeze(str(record["grid_path"])), stated_bytes(record)))
    return found


def stated_bytes(record):
    """The size the record gives, for the estimate only: what was measured, else its counts."""
    measured = record.get("measured") if isinstance(record.get("measured"), dict) else {}
    if isinstance(measured.get("bytes"), int):
        return measured["bytes"]
    counts = record.get("counts") if isinstance(record.get("counts"), dict) else {}
    for key, scale in (("bytes", 1), ("zip_bytes", 1), ("size_tb", 10 ** 12), ("size_gb", 10 ** 9),
                       ("gigabytes", 10 ** 9), ("size_mb", 10 ** 6)):
        value = counts.get(key)
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            return int(value * scale)
    return None


# Bringing the public copies back from the grid.

def copies_in(folder, log=None):
    """{id: public copy} for each <id>.json in a folder that passes the public copy's rules; any
    other file is named in the log and left out, so nothing with a name in it leaves the grid."""
    found = {}
    for name in sorted(os.listdir(folder)):
        ident = name[:-5] if name.endswith(".json") else ""
        if not ID_SHAPE.match(ident):
            continue
        try:
            copy = read_summary(os.path.join(folder, name))
        except (ValueError, UnicodeDecodeError) as error:
            problems = ["not ASCII JSON (%s)" % error]
        else:
            problems = summary_problems(copy, ident)
        if problems:
            if log:
                log("%s: left out: %s" % (ident, "; ".join(problems)))
            continue
        found[ident] = copy
    return found


def bundle(folder, log=None):
    """The body of a POST to git/trees: frozen/<id>.json for every copy that passes."""
    return {"tree": [{"path": "frozen/%s.json" % ident, "mode": "100644", "type": "blob",
                      "content": summary_bytes(copy).decode("ascii")}
                     for ident, copy in sorted(copies_in(folder, log).items())]}


def apply_copies(folder, root=ROOT, log=None):
    """Each copy into frozen/ and its measured block into its record; the ids written."""
    written = []
    for ident, copy in sorted(copies_in(folder, log).items()):
        record_path = os.path.join(root, "datasets", ident + ".json")
        if not os.path.exists(record_path):
            if log:
                log("%s: left out: no record datasets/%s.json" % (ident, ident))
            continue
        with io.open(record_path, encoding="utf-8") as handle:
            record = json.load(handle)
        measured = record.get("measured") if isinstance(record.get("measured"), dict) else {}
        measured.update(measured_of(copy))
        record["measured"] = measured
        with io.open(record_path, "w", encoding="ascii", newline="\n") as handle:
            handle.write(json.dumps(record, indent=1, ensure_ascii=True) + "\n")
        with open(os.path.join(root, "frozen", ident + ".json"), "wb") as handle:
            handle.write(summary_bytes(copy))
        written.append(ident)
    return written


# The command line.

def log_line(text):
    sys.stderr.write("%s %s\n" % (time.strftime("%H:%M:%S"), text))
    sys.stderr.flush()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command")
    run = sub.add_parser("freeze", help="hash a dataset's folder and write FROZEN.json and its file list into it")
    run.add_argument("dir")
    run.add_argument("--id", required=True)
    run.add_argument("--workers", type=int, default=1)
    run.add_argument("--depth", type=int, default=DEFAULT_DEPTH)
    run.add_argument("--copy", help="also write the summary here, as frozen/<id>.json")
    run.add_argument("--out", help="write the freeze here, for a folder the freeze may not write into")
    check = sub.add_parser("verify", help="read the folder again against its file list")
    check.add_argument("dir")
    check.add_argument("--quick", action="store_true", help="names and sizes only, no hashing")
    check.add_argument("--workers", type=int, default=1)
    check.add_argument("--out", help="where the freeze was written, when not in the folder")
    look = sub.add_parser("show", help="the folders and their sizes, without reading the data")
    look.add_argument("path", help="a frozen folder, or a FROZEN.json, or its public copy frozen/<id>.json")
    look.add_argument("--under", default="")
    look.add_argument("--depth", type=int)
    block = sub.add_parser("measured", help="the record's measured block from a FROZEN.json")
    block.add_argument("summary")
    todo = sub.add_parser("plan", help="every set on the grid not yet frozen: id, folder, stated bytes")
    todo.add_argument("--root", default=ROOT)
    repo = sub.add_parser("check", help="frozen/<id>.json against the records")
    repo.add_argument("--root", default=ROOT)
    pack = sub.add_parser("bundle", help="the git tree of the public copies in a folder, as JSON")
    pack.add_argument("copies")
    put = sub.add_parser("apply", help="the public copies in a folder into frozen/ and the records")
    put.add_argument("copies")
    put.add_argument("--root", default=ROOT)
    args = parser.parse_args(argv)
    if args.command == "freeze":
        if not ID_SHAPE.match(args.id):
            parser.error("--id must be a record's id")
        summary = freeze(args.dir, args.id, args.workers, args.depth, log=log_line, out=args.out)
        if args.copy:
            with open(args.copy, "wb") as handle:
                handle.write(summary_bytes(public_copy(summary)))
        print("%s: %d files, %s, tree %s" % (args.id, summary["files"], size_text(summary["bytes"]), summary["tree_sha256"]))
        return 0
    if args.command == "verify":
        problems = verify(args.dir, args.quick, args.workers, args.out)
        for problem in problems:
            print(problem)
        print("identical" if not problems else "%d differences" % len(problems))
        return 1 if problems else 0
    if args.command == "show":
        top = args.path if os.path.isdir(args.path) else None
        summary = read_summary(os.path.join(top, SUMMARY) if top else args.path)
        files = None
        if args.under or (args.depth and args.depth != summary["depth"]):
            if top is None:
                parser.error("--under and --depth need the frozen folder itself, whose file list has every file")
            files = read_file_list(top)
        for path, count, size in show_rows(summary, files, args.under.strip("/"), args.depth):
            print("%12s %10s  %s" % (size_text(size), count, path))
        return 0
    if args.command == "measured":
        print(json.dumps(measured_of(read_summary(args.summary)), indent=1, sort_keys=True))
        return 0
    if args.command == "plan":
        rows = plan(args.root)
        for ident, folder, size in rows:
            if folder is None:
                sys.stderr.write("%s: its grid_path names more than one folder; freeze each by hand\n" % ident)
                continue
            print("%s\t%s\t%s" % (ident, folder, size if size is not None else "-"))
        known = [size for _i, _f, size in rows if size is not None]
        sys.stderr.write("%d sets to freeze, %s stated for %d of them\n" % (len(rows), size_text(sum(known)), len(known)))
        return 0
    if args.command == "check":
        problems = check_repository(args.root)
        for problem in problems:
            print(problem)
        return 1 if problems else 0
    if args.command == "bundle":
        tree = bundle(args.copies, log_line)
        if not tree["tree"]:
            sys.stderr.write("no public copy to send\n")
            return 1
        print(json.dumps(tree, sort_keys=True))
        return 0
    if args.command == "apply":
        written = apply_copies(args.copies, args.root, log_line)
        print("%d sets frozen into the repository: %s" % (len(written), " ".join(written)))
        return 0
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
