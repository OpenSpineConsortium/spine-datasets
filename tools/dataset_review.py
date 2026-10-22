"""The automated review every dataset pull request passes before the owner merges it.

Source: the thread "Automated dataset PR review", 2026-10-21 (issue #100). A merged manifest is
what the promoter (tools/promote.py), running as the owner's grid account, fetches and installs
read-only under /rs/rs_grp_oschome/shared/datasets/<id>/raw, so what reaches the default branch
must already be right. Two commands:

`check` reads the whole tree and is part of scripts/check.sh: every manifests/<id>.json holds by
the promoter's own rules (promote.valid_manifest): an id with a record, the record's link and
licence copied exactly, a licence that allows the fetch (an open one, or a grant in the history),
the record at fetching or fetched, every file under raw/ with an https link on the source's own
site and no token or signature in it, a positive size, a sha256, and sizes that add up.

`diff --base REF` reads what a pull request adds, and is run by the required check on every pull
request (.github/workflows/ci.yml):

- FAIL, the check goes red:
  - an added line in a record, a manifest or a letter (a file's path or link aside, which are the
    publisher's names), or the pull request's title or body, with a word the confidentiality rule
    bans (CONTRIBUTING.md, "The confidentiality rule, first");
  - a record whose history lost or changed an earlier entry (history only grows);
  - a token, key or signed link in the title or body (check_docs.py holds the files to the same);
  - a data file added to the repository (an image, an archive, a volume, a table of rows), outside
    docs/ and tests/, where it is flagged instead, since a figure or a fixture may belong there;
  - a record moved to fetched without a manifest, or with a grid_path outside the shared tree;
  - a change to the promoter's own code or budget (tools/promote.py, grid/promote.sh,
    grid/promote.json), which runs as the owner on the grid, in a pull request someone other than
    the owner opened;
  - a change on the promoter's own branch promote/<id> to anything but that one record.
- FLAG, written in the report for whoever merges, the check stays green:
  - a line that reads as something binding done in the owner's name (signed, agreed, paid,
    attested, accepted terms), which only the owner may do;
  - a licence or link changed other than by replacing "to confirm on the page";
  - a non-commercial or no-derivatives licence, which also needs a grant in the history to be
    fetched at all.
- NOTE: a CT manifest while X-ray sets still wait to be fetched; the promoter takes X-ray first.

The report goes to the job's log and, on GitHub, to the job's summary page.

`manifest` writes a manifest from what the source itself publishes, for the routes whose API
gives every file's size and checksum: Mendeley Data (sha256) and Zenodo (md5). It takes a Mendeley
dataset as its id or its page's address, one or several for a record that gathers several, the
latest version unless the address or --version names one; it readies the record in the same
step (the licence as the page reads it, given with --licence, and the status fetching with its
history entry), then holds the result to the promoter's rules and says what is still to do. It
needs the network, so it runs on a collaborator's own machine or on the grid, never in the check.

    python3 tools/dataset_review.py check
    python3 tools/dataset_review.py diff --base origin/main
    python3 tools/dataset_review.py manifest ID --mendeley https://data.mendeley.com/datasets/DATASET/N
    python3 tools/dataset_review.py manifest ID --zenodo RECORD
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import promote  # noqa: E402
from check_docs import SECRET_PATTERNS  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SHARED = "/rs/rs_grp_oschome/shared/datasets"
XRAY_GROUPS = ("fluoro", "video", "projections", "films")
TRUSTED_PATHS = ("tools/promote.py", "grid/promote.sh", "grid/promote.json")
# Who may change what runs as the owner on the grid; the promoter holds the same rule on its side.
OWNERS = ("Gregory-Schwing-MD-PhD",)
# Lines of a record or manifest that name a place rather than describe anything: a file name such
# as train.zip is the publisher's, not the project's words.
NAMING_FIELD = re.compile(r'^\s*"(path|url|link|sha256|md5|source)"\s*:')

# The confidentiality rule's words, built from pieces so this file's own text does not read as
# breaking it wherever it is quoted.
BANNED = re.compile(
    r"\b(" + "|".join((
        "neural " + "networks?", "mod" + "els?", "mod" + "ell?ing", "machine " + "learning",
        "deep " + "learning", "train" + "(?:ing|ed|s)?", "detect" + "ors?", "classif" + "iers?",
    )) + r")\b",
    re.IGNORECASE,
)
BANNED_CASED = re.compile(r"\b" + "A" + "I" + r"\b")
BINDING = re.compile(
    r"\b(signed|countersigned|agreed to|accepted the (terms|agreement|licen[cs]e)|attest(ed|ation)|"
    r"paid|payment|ticked the|clicked (accept|agree|i agree))\b",
    re.IGNORECASE,
)
DATA_SUFFIXES = (
    ".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp", ".gif", ".dcm", ".dicom", ".nii", ".nrrd",
    ".mha", ".mhd", ".npy", ".npz", ".h5", ".hdf5", ".zip", ".tar", ".gz", ".tgz", ".7z", ".rar",
    ".mp4", ".avi", ".mkv", ".mov", ".csv", ".parquet",
)
SCANNED = re.compile(r"^(datasets/[a-z0-9_]+\.json|manifests/[a-z0-9_]+\.json|letters/[^/]+\.md)$")


class Report:
    def __init__(self):
        self.lines = []

    def add(self, level, text):
        self.lines.append((level, text))

    def failed(self):
        return any(level == "FAIL" for level, _ in self.lines)

    def text(self):
        if not self.lines:
            return "dataset review: nothing to say"
        return "\n".join("%s: %s" % pair for pair in self.lines)

    def publish(self):
        print(self.text())
        summary = os.environ.get("GITHUB_STEP_SUMMARY")
        if summary:
            with open(summary, "a", encoding="utf-8") as handle:
                handle.write("## Dataset review\n\n")
                for level, text in self.lines or [("OK", "nothing to say")]:
                    handle.write("- **%s** %s\n" % (level, text))


def read_json(path):
    with open(path, encoding="ascii") as handle:
        return json.load(handle)


# check: the whole tree.

def check_tree(root=ROOT, report=None):
    report = report or Report()
    folder = root / "manifests"
    for path in sorted(folder.glob("*.json")) if folder.is_dir() else []:
        ident = path.stem
        record_path = root / "datasets" / (ident + ".json")
        record = read_json(record_path) if record_path.exists() else None
        try:
            manifest = read_json(path)
        except (ValueError, UnicodeDecodeError) as error:
            report.add("FAIL", "manifests/%s.json is not ASCII JSON: %s" % (ident, error))
            continue
        for problem in promote.valid_manifest(manifest, record, ident):
            report.add("FAIL", "manifests/%s.json: %s" % (ident, problem))
    for path in sorted((root / "datasets").glob("*.json")):
        record = read_json(path)
        if record.get("status") != "fetched" or not (record.get("grid_path") or "").startswith(SHARED):
            continue
        if not (folder / path.name).exists():
            report.add("FAIL", "datasets/%s says fetched into the shared tree but has no manifest" % path.name)
    return report


# diff: what a pull request adds.

def git(*args, root=ROOT):
    return subprocess.run(["git", *args], cwd=root, check=True, capture_output=True, text=True).stdout


def changed_files(base, root=ROOT):
    """(status, path) of every file the change adds, modifies or deletes since it left base.

    NUL-separated, since git quotes a name with non-ASCII bytes in its plain output."""
    fields = git("diff", "--name-status", "--no-renames", "-z", base + "...HEAD", root=root).split("\0")
    return [(fields[i], fields[i + 1]) for i in range(0, len(fields) - 1, 2) if fields[i]]


def added_lines(base, path, root=ROOT):
    out = git("diff", "--unified=0", base + "...HEAD", "--", path, root=root)
    return [line[1:] for line in out.splitlines() if line.startswith("+") and not line.startswith("+++")]


def old_json(base, path, root=ROOT):
    fork = git("merge-base", base, "HEAD", root=root).strip()
    try:
        return json.loads(git("show", "%s:%s" % (fork, path), root=root))
    except (subprocess.CalledProcessError, ValueError):
        return None


def banned_words(text):
    found = [match.group(0) for match in BANNED.finditer(text)]
    return found + [match.group(0) for match in BANNED_CASED.finditer(text)]


def review_text(where, text, report):
    words = banned_words(text)
    if words:
        report.add("FAIL", "%s says %s; CONTRIBUTING.md's confidentiality rule bans those words"
                   % (where, ", ".join(sorted(set(words)))))
    if BINDING.search(text):
        report.add("FLAG", "%s reads as something binding (%s); only the owner signs, pays, attests or accepts"
                   % (where, BINDING.search(text).group(0)))


def review_record(path, base, report, root=ROOT):
    before = old_json(base, path, root=root)
    after = json.loads((root / path).read_text(encoding="ascii"))
    ident = after.get("id", Path(path).stem)
    if before:
        old_history = before.get("history", [])
        if after.get("history", [])[:len(old_history)] != old_history:
            report.add("FAIL", "%s: an earlier history entry was changed or removed; history only grows" % path)
        for field in ("licence", "link"):
            old, new = before.get(field), after.get(field)
            if old != new and "to confirm" not in (old or ""):
                report.add("FLAG", "%s: %s changed from '%s' to '%s'; the pull request must say the page shows it"
                           % (path, field, old, new))
    if promote.RESTRICTED_LICENCE.search(after.get("licence", "")):
        report.add("FLAG", "%s: the licence '%s' restricts use; the owner decides" % (path, after.get("licence")))
    if after.get("status") == "fetched" and (before or {}).get("status") != "fetched":
        grid_path = after.get("grid_path") or ""
        if grid_path != "%s/%s/raw" % (SHARED, ident):
            report.add("FAIL", "%s: fetched needs grid_path %s/%s/raw, which the promoter writes" % (path, SHARED, ident))


def xray_waiting(root=ROOT):
    waiting = []
    for path in sorted((root / "datasets").glob("*.json")):
        record = read_json(path)
        if record.get("group") in XRAY_GROUPS and record.get("status") == "granted":
            waiting.append(record["id"])
        elif record.get("group") in XRAY_GROUPS and record.get("route") == "download" and record.get("status") == "todo":
            waiting.append(record["id"])
    return waiting


def pull_request():
    """The pull request the check runs for, from GitHub's event file, or None outside one."""
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    if not event_path or not os.path.exists(event_path):
        return None
    with open(event_path, encoding="utf-8") as handle:
        return json.load(handle).get("pull_request")


def review_pull_request_text(pull, report):
    if not pull:
        return
    for where, text in (("the title", pull.get("title") or ""), ("the description", pull.get("body") or "")):
        review_text("the pull request's " + where[4:], text, report)
        for name, pattern in SECRET_PATTERNS:
            if pattern.search(text):
                report.add("FAIL", "the pull request's %s holds what looks like a %s" % (where[4:], name))


def review_trusted(path, pull, report):
    """A change to what runs as the owner fails unless an owner opened the pull request."""
    author = ((pull or {}).get("user") or {}).get("login")
    if pull is None:
        report.add("FLAG", "%s runs as the owner on the grid; the owner reads this change before merging" % path)
    elif author not in OWNERS:
        report.add("FAIL", "%s runs as the owner on the grid; only the owner's own pull request changes it" % path)
    else:
        report.add("NOTE", "%s runs as the owner on the grid; the promoter takes it only from the owner's own "
                   "pull request with no commit tied to anyone else" % path)


def review_promote_branch(changes, pull, report):
    """The promoter's own branch promote/<id> changes that one record and nothing else."""
    head = (((pull or {}).get("head") or {}).get("ref")) or ""
    if not head.startswith("promote/"):
        return
    allowed = "datasets/%s.json" % head[len("promote/"):]
    for status, path in changes:
        if path != allowed:
            report.add("FAIL", "%s on %s: the promoter's branch changes only %s" % (path, head, allowed))


def review_diff(base, root=ROOT, report=None, pull=None):
    report = report or Report()
    changes = changed_files(base, root=root)
    review_promote_branch(changes, pull, report)
    for status, path in changes:
        if status == "D":
            continue
        if path.lower().endswith(DATA_SUFFIXES):
            level = "FLAG" if path.startswith(("docs/", "tests/")) else "FAIL"
            report.add(level, "%s is a data file; data stay on the grid and the record says where" % path)
            continue
        if path in TRUSTED_PATHS:
            review_trusted(path, pull, report)
        if SCANNED.match(path):
            for line in added_lines(base, path, root=root):
                if not (path.endswith(".json") and NAMING_FIELD.match(line)):
                    review_text(path, line, report)
        if path.startswith("datasets/") and path.endswith(".json") and path != "datasets/README.md":
            review_record(path, base, report, root=root)
        if path.startswith("manifests/") and path.endswith(".json") and status == "A":
            record_path = root / "datasets" / Path(path).name
            if record_path.exists() and read_json(record_path).get("group") == "ct" and xray_waiting(root):
                report.add("NOTE", "%s is a CT set while %d X-ray sets wait; the promoter takes X-ray first"
                           % (path, len(xray_waiting(root))))
    review_pull_request_text(pull, report)
    return report


# manifest: from the source's own file list.

MENDELEY_DATASET = "https://data.mendeley.com/public-api/datasets/%s"
MENDELEY_FILES = "https://data.mendeley.com/public-api/datasets/%s/files?folder_id=root&version=%s"
ZENODO_RECORD = "https://zenodo.org/api/records/%s"
# A Mendeley dataset as a collaborator has it: its bare id, its page's address, or the page's
# address with the version after it, as the page's own link and its DOI 10.17632/<id>.<n> give it.
MENDELEY_ID = re.compile(
    r"^(?:https?://data\.mendeley\.com/datasets/|(?:https?://doi\.org/)?10\.17632/)?([a-z0-9]{6,20})(?:[/.](\d{1,4}))?/?$")
UNSET_STATUSES = ("todo", "researched", "asked", "granted")

# Mendeley's public API answers 403 to Python's own User-Agent and 200 to a browser's.
USER_AGENT = "Mozilla/5.0 (spine-datasets manifest)"


class ManifestError(Exception):
    """A step the manifest command cannot take, said in one line with what to do."""


def fetch_json(url):
    import ssl
    import urllib.error
    import urllib.request
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=60) as answer:
            return json.load(answer)
    except urllib.error.HTTPError as error:
        raise ManifestError("%s answered %d %s; check the id and the version on the dataset's page"
                            % (url, error.code, error.reason)) from None
    except urllib.error.URLError as error:
        if isinstance(error.reason, ssl.SSLCertVerificationError):
            raise ManifestError("this Python cannot verify %s's certificate; on a Mac run it as "
                                "SSL_CERT_FILE=/etc/ssl/cert.pem python3 tools/dataset_review.py ..., "
                                "or run python.org's Install Certificates.command once" % url) from None
        raise ManifestError("%s could not be reached: %s" % (url, error.reason)) from None
    except ValueError:
        raise ManifestError("%s did not answer JSON" % url) from None


def mendeley_dataset(given, version=None):
    """(id, version) from what the collaborator gave: a version in the address wins, then
    --version, then the latest version Mendeley's public API names for the dataset."""
    match = MENDELEY_ID.match((given or "").strip())
    if not match:
        raise ManifestError("'%s' is not a Mendeley Data id or https://data.mendeley.com/datasets/<id>/<n>" % given)
    ident, in_address = match.groups()
    found = in_address or version
    if not found:
        try:
            latest = fetch_json(MENDELEY_DATASET % ident)
        except ManifestError:
            latest = None
        found = latest.get("version") if isinstance(latest, dict) else None
        if not isinstance(found, int) or isinstance(found, bool):
            raise ManifestError("Mendeley did not say %s's latest version; give it, as the page shows it, "
                                "with --version N or as https://data.mendeley.com/datasets/%s/N" % (ident, ident))
    return ident, str(found)


def mendeley_files(listing, folder=""):
    """The manifest's file entries from Mendeley's public file list; folder, for a record that
    gathers several datasets, keeps each one's files under raw/<its id>/ so no two names meet."""
    if not isinstance(listing, list):
        raise ManifestError("Mendeley's file list is not a list; the dataset may hold no public files")
    files = []
    for item in listing:
        details = item.get("content_details") if isinstance(item, dict) else None
        if not isinstance(details, dict) or not details.get("download_url"):
            name = item.get("filename") if isinstance(item, dict) else item
            raise ManifestError("Mendeley's list holds '%s' with no download link, perhaps a folder; "
                                "write that part of the manifest by hand from the page" % name)
        files.append({
            "path": "raw/" + folder + item["filename"], "url": details["download_url"], "bytes": details["size"],
            "sha256": details["sha256_hash"], "verified_against": "Mendeley Data's public API",
        })
    return files


def mendeley_manifest_files(datasets, version):
    """Every file of one or more Mendeley datasets, and how each was read, for the history."""
    files, read = [], []
    for given in datasets:
        ident, number = mendeley_dataset(given, version)
        folder = ident + "/" if len(datasets) > 1 else ""
        found = mendeley_files(fetch_json(MENDELEY_FILES % (ident, number)), folder)
        if not found:
            raise ManifestError("Mendeley lists no files for %s version %s" % (ident, number))
        files += found
        read.append("%s version %s, %d files" % (ident, number, len(found)))
    return files, read


def zenodo_files(record):
    files = []
    for item in record["files"]:
        algorithm, _, value = item["checksum"].partition(":")
        if algorithm != "md5":
            raise ManifestError("Zenodo gave a %s checksum for %s" % (algorithm, item["key"]))
        files.append({
            "path": "raw/" + item["key"], "url": item["links"]["self"], "bytes": item["size"],
            "md5": value, "verified_against": "Zenodo's API",
        })
    return files


def build_manifest(record, files, today):
    return {
        "id": record["id"], "source": record["link"], "licence": record["licence"], "date": today, "files": files, "bytes_total": sum(entry["bytes"] for entry in files),
    }


def readied(record, today, read, licence=None):
    """The record as the manifest's pull request leaves it: the licence as read on the page, if
    given, and the status fetching with its history entry, unless it is fetching or fetched."""
    record = json.loads(json.dumps(record))
    history = record.setdefault("history", [])
    if licence and licence != record.get("licence"):
        record["licence"] = licence
        history.append({"date": today, "step": "note", "note": "licence read on the page: " + licence})
    if record.get("status") in UNSET_STATUSES:
        record["status"] = "fetching"
        history.append({"date": today, "step": "fetching",
                        "note": "manifest ready (%s); the promoter fetches it after merge" % "; ".join(read)})
        record["next"] = "the promoter installs it after merge"
    return record


def write_json(path, value):
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(value, indent=1, ensure_ascii=True) + "\n", encoding="ascii")


def write_manifest(args, root=ROOT):
    from datetime import datetime, timezone
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    record_path = root / "datasets" / (args.id + ".json")
    if not record_path.exists():
        raise ManifestError("there is no record datasets/%s.json; the manifest is named after its record" % args.id)
    record = read_json(record_path)
    if args.mendeley:
        files, read = mendeley_manifest_files(args.mendeley, args.version)
    else:
        files, read = zenodo_files(fetch_json(ZENODO_RECORD % args.zenodo)), ["Zenodo record %s" % args.zenodo]
    if not args.leave_record:
        record = readied(record, today, read, args.licence)
        write_json(record_path, record)
    manifest = build_manifest(record, files, today)
    path = root / "manifests" / (args.id + ".json")
    write_json(path, manifest)
    print("wrote %s: %d files, %d bytes (%s)" % (path.relative_to(root), len(files), manifest["bytes_total"],
                                                  "; ".join(read)))
    if not args.leave_record:
        print("updated %s: status %s" % (record_path.relative_to(root), record.get("status")))
    problems = promote.valid_manifest(manifest, record, args.id)
    for problem in problems:
        print("still to do: " + problem)
    if any("to confirm" in problem or "licence" in problem for problem in problems):
        print("read the licence line on the dataset's page and run again with --licence \"<that line>, "
              "as the page reads it, %s\"" % today)
    return 1 if problems else 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("check", help="every manifest in the tree holds")
    diff = sub.add_parser("diff", help="review what a pull request adds")
    diff.add_argument("--base", required=True, help="the branch the pull request goes into, e.g. origin/main")
    make = sub.add_parser("manifest", help="write manifests/<id>.json from the source's own file list")
    make.add_argument("id")
    where = make.add_mutually_exclusive_group(required=True)
    where.add_argument("--mendeley", action="append", metavar="DATASET",
                       help="a Mendeley Data id or page address, e.g. xkt857dsxk or "
                            "https://data.mendeley.com/datasets/xkt857dsxk/1; repeat it for a record of several")
    where.add_argument("--zenodo", help="the Zenodo record number")
    make.add_argument("--version", help="the Mendeley version, where the address gives none; the latest otherwise")
    make.add_argument("--licence", help="the licence line as the page reads it, written into the record and the manifest")
    make.add_argument("--leave-record", action="store_true",
                      help="write only the manifest, leaving the record's status and history as they are")
    args = parser.parse_args(argv)
    if args.command == "manifest":
        try:
            return write_manifest(args)
        except ManifestError as error:
            print("manifest: " + str(error), file=sys.stderr)
            return 1
    if args.command == "check":
        report = check_tree()
    else:
        report = check_tree(report=review_diff(args.base, pull=pull_request()))
    report.publish()
    return 1 if report.failed() else 0


if __name__ == "__main__":
    sys.exit(main())
