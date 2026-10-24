"""Which sets on the grid hold the same scans: the ledger of every frozen file and the overlap table.

Source: the thread "Check frozen manifest job", 2026-10-24, the owner's ask of that day to remove
sets for more useful ones without losing any, one patient once across sets, every sample traced
and any set rebuilt (docs/research/lineage-and-retirement.md, step 2 of its plan). The owner chose
on the same day to build this and run it as one read-only job.

`build` reads, for every frozen set, the file list its freeze wrote beside the data
(FROZEN.files.tsv.gz: sha256, bytes and path of each file), and the header of a few DICOM files in
each folder that holds them. It never reads an image's pixels, never writes into a dataset's
folder, and needs no fetch. It writes two things into its own folder:

- lineage.sqlite, the ledger, which stays on the grid: one row per file (set, path, sha256, bytes,
  name stem) and one per DICOM folder read (set, folder, patient, study, series);
- OVERLAP.json, counts alone: for each set its files, bytes, DICOM series, studies and patients,
  the bytes no other set holds; and for each pair of sets that share anything, how many files and
  bytes are byte for byte the same, how many DICOM series and studies they share by UID, how many
  patient IDs, how many image names, and how many of one's names are the other's UIDs. It holds no
  path, name, UID or patient ID, so it may leave the grid (public_problems holds it to that), and
  freeze.sh report carries it back as lineage/OVERLAP.json.

Since a NIfTI volume carries no UID and each release re-encodes it (the first pass, grid job
40775283, found no pair sharing a byte), `build` also reads every NIfTI image volume's header
(its first 348 bytes, the gzip's start alone), and keys it by its geometry: the sizes and voxel
spacings of its three axes, sorted, so a volume stored in another axis order keys the same. Only
volumes whose geometry another set's volume shares are then read whole, once, for two signatures:
the sha256 of the voxel bytes, the same scan stored the same way however the file was compressed,
and the sum of the scaled voxel values with their count, the same values in any axis order or any
integer type. These read image data, so they run only in the job the owner gave his word for
(2026-10-24, "Go" on the voxel fingerprint), and the counts alone leave the grid: for each pair,
how many volumes share a geometry (a lead), share their values (the same scan), and share their
voxel bytes (the same scan stored alike).

Three kinds of evidence, strongest first: a DICOM series or study UID is unique by construction,
so a shared one is the same scan; a shared sha256 is the same bytes; a shared name is a lead only,
since sets name cases case_001 alike, so names count only when they look like an identifier
(stem_counts). A shared patient ID is a lead too, since two collections may number patients the
same way, and counts only when it mixes letters and digits and is six characters or more.

It runs on the grid's own python3, which may be as old as 3.6, with the standard library alone, as
tools/freeze.py does.

    python3 tools/lineage.py build --plan PLAN [--shared DIR] --out DIR [--workers N]
    python3 tools/lineage.py check OVERLAP.json
    python3 tools/lineage.py tree OVERLAP.json TREE.json   add it to freeze.sh report's git tree
"""

import argparse
import gzip
import io
import json
import os
import re
import sqlite3
import struct
import sys
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

FILE_LIST = "FROZEN.files.tsv.gz"
LEDGER = "lineage.sqlite"
OVERLAP = "OVERLAP.json"
FORMAT = "spine-datasets/overlap 2"
OLD_FORMAT = "spine-datasets/overlap 1"
ID_SHAPE = re.compile(r"^[a-z0-9_]+$")
# files smaller than this are licences, readmes and empty masks, which many sets share by chance
DATA_BYTES = 64 * 1024
HEADER_BYTES = 256 * 1024
DICOM_TRIES = 3

IMAGE_ENDINGS = (".nii.gz", ".nii", ".mha", ".mhd", ".nrrd", ".nrrd.gz", ".dcm", ".png", ".jpg",
                 ".jpeg", ".tif", ".tiff", ".npz", ".npy", ".h5")
STEM_SUFFIX = re.compile(r"(_0000|_ct|_img|_image|_volume|_seg|_label|_labels|_mask|_msk)$")
GENERIC_WORDS = re.compile(r"^(case|patient|pat|img|image|sub|subject|vol|volume|scan|ct|sample|data|"
                           r"label|mask|seg|series|study|id|train|test|val)[-_]?\d+$")


# Reading a few DICOM tags without a DICOM library.

PATIENT_ID = (0x0010, 0x0020)
STUDY_UID = (0x0020, 0x000D)
SERIES_UID = (0x0020, 0x000E)
WANTED = (PATIENT_ID, STUDY_UID, SERIES_UID)
LONG_VRS = {b"OB", b"OD", b"OF", b"OL", b"OV", b"OW", b"SQ", b"SV", b"UC", b"UN", b"UR", b"UT", b"UV"}
UNDEFINED = 0xFFFFFFFF
IMPLICIT_LE = "1.2.840.10008.1.2"
BIG_ENDIAN = "1.2.840.10008.1.2.2"


class NotDicom(ValueError):
    pass


def dicom_tags(data):
    """{tag: text} for the patient ID and the study and series UIDs found in a header's bytes."""
    found = {}
    if data[128:132] == b"DICM":
        meta_end, syntax = read_meta(data, 132, found)
        if syntax == BIG_ENDIAN:
            raise NotDicom("big endian")
        read_elements(data, meta_end, syntax != IMPLICIT_LE, found)
    else:
        if len(data) < 8 or struct.unpack_from("<H", data, 0)[0] not in (0x0002, 0x0008):
            raise NotDicom("no preamble and no group 0002 or 0008 first")
        read_elements(data, 0, False, found)
    return found


def read_meta(data, pos, found):
    """The end of the file meta group (0002) and its transfer syntax; meta is always explicit LE."""
    syntax = IMPLICIT_LE
    while pos + 8 <= len(data):
        group, element = struct.unpack_from("<HH", data, pos)
        if group != 0x0002:
            break
        vr, length, value_at = explicit_header(data, pos)
        value = data[value_at:value_at + length]
        if element == 0x0010:
            syntax = text_of(value)
        pos = value_at + length
    return pos, syntax


def explicit_header(data, pos):
    vr = data[pos + 4:pos + 6]
    if vr in LONG_VRS:
        return vr, struct.unpack_from("<I", data, pos + 8)[0], pos + 12
    return vr, struct.unpack_from("<H", data, pos + 6)[0], pos + 8


def read_elements(data, pos, explicit, found, end=None, depth=0):
    """Walk elements from pos until the wanted tags are found, group 0020 is passed, a delimiter
    closes this level, or the bytes run out; returns where it stopped."""
    end = len(data) if end is None else end
    while pos + 8 <= end:
        group, element = struct.unpack_from("<HH", data, pos)
        if group == 0xFFFE:
            if element in (0xE00D, 0xE0DD):
                return pos + 8
            raise NotDicom("an item tag outside a sequence")
        if group > 0x0020 and depth == 0:
            return pos
        if explicit:
            vr, length, value_at = explicit_header(data, pos)
        else:
            vr, length, value_at = None, struct.unpack_from("<I", data, pos + 4)[0], pos + 8
        if vr == b"SQ" or (length == UNDEFINED):
            pos = skip_sequence(data, value_at, length, explicit, depth)
            continue
        if value_at + length > len(data):
            return len(data)
        if depth == 0 and (group, element) in WANTED:
            found[(group, element)] = text_of(data[value_at:value_at + length])
            if len(found) == len(WANTED):
                return value_at + length
        pos = value_at + length
    return pos


def skip_sequence(data, pos, length, explicit, depth):
    """Past a sequence, of a given length or closed by its delimiter, its items read as nested."""
    if length != UNDEFINED:
        return pos + length
    if depth > 8:
        raise NotDicom("sequences nested too deep")
    while pos + 8 <= len(data):
        group, element, item_length = struct.unpack_from("<HHI", data, pos)
        if (group, element) == (0xFFFE, 0xE0DD):
            return pos + 8
        if (group, element) != (0xFFFE, 0xE000):
            raise NotDicom("no item where a sequence item belongs")
        if item_length == UNDEFINED:
            pos = read_elements(data, pos + 8, explicit, {}, depth=depth + 1)
        else:
            pos = pos + 8 + item_length
    return len(data)


def text_of(value):
    return value.decode("ascii", "replace").strip("\x00 ").strip()


def looks_like_dicom_path(path):
    base = path.rsplit("/", 1)[-1].lower()
    return base.endswith(".dcm") or base.endswith(".ima") or "." not in base


def read_header(path):
    """(patient, study, series) of one file, or None when it is no DICOM this reader can read."""
    try:
        with open(path, "rb") as handle:
            tags = dicom_tags(handle.read(HEADER_BYTES))
    except (OSError, NotDicom, struct.error):
        return None
    if STUDY_UID not in tags and SERIES_UID not in tags:
        return None
    return tags.get(PATIENT_ID, ""), tags.get(STUDY_UID, ""), tags.get(SERIES_UID, "")


def dicom_candidates(rows):
    """{folder: [paths]}: up to DICOM_TRIES files per folder that may be DICOM, in path order."""
    folders = {}
    for path in rows:
        if not looks_like_dicom_path(path):
            continue
        folder = path.rsplit("/", 1)[0] if "/" in path else ""
        tries = folders.setdefault(folder, [])
        if len(tries) < DICOM_TRIES:
            tries.append(path)
    return folders


def first_header(top, paths):
    for path in paths:
        found = read_header(os.path.join(top, path))
        if found:
            return found
    return None


# Names.

def stem_of(path):
    """The image name without its folder, its ending and a channel or label suffix, lowercased;
    None for a file that is no image."""
    base = path.rsplit("/", 1)[-1].lower()
    for ending in IMAGE_ENDINGS:
        if base.endswith(ending):
            base = base[:-len(ending)]
            break
    else:
        return None
    return STEM_SUFFIX.sub("", base) or None


def stem_counts(stem):
    """Whether a name looks like an identifier another set could share on purpose: a UID, or one
    with eight digits or more, or letters and digits that are not a generic word and a number."""
    if stem is None or len(stem) < 8:
        return False
    if stem.count(".") >= 3:
        return True
    if GENERIC_WORDS.match(stem):
        return False
    digits = sum(ch.isdigit() for ch in stem)
    return digits >= 8 or (digits >= 3 and any(ch.isalpha() for ch in stem))


def patient_counts(patient):
    return (len(patient) >= 6 and any(ch.isdigit() for ch in patient)
            and any(ch.isalpha() for ch in patient))


# The sets to read.

def sets_from(plan, shared=None):
    """[(id, folder)] of every set with a file list: the plan's lines, then each shared/<id> the
    promoter froze; a set named twice is read from the plan's folder."""
    found, seen = [], set()
    if plan:
        with io.open(plan, encoding="utf-8") as handle:
            for line in handle:
                parts = line.rstrip("\n").split("\t")
                if len(parts) >= 2 and ID_SHAPE.match(parts[0]) and parts[0] not in seen:
                    if os.path.isfile(os.path.join(parts[1], FILE_LIST)):
                        found.append((parts[0], parts[1]))
                        seen.add(parts[0])
    if shared and os.path.isdir(shared):
        for name in sorted(os.listdir(shared)):
            folder = os.path.join(shared, name)
            if ID_SHAPE.match(name) and name not in seen and os.path.isfile(os.path.join(folder, FILE_LIST)):
                found.append((name, folder))
                seen.add(name)
    return found


def file_rows(folder):
    with gzip.open(os.path.join(folder, FILE_LIST), "rb") as handle:
        for raw in handle:
            digest, size, path = raw.decode("utf-8", "surrogateescape").rstrip("\n").split("\t", 2)
            yield digest, int(size), path


# NIfTI volumes: the geometry from the header, the signatures from the voxels.

NIFTI_HEADER = 348
LABEL_WORDS = re.compile(r"(^|[/_.-])(seg|segs|segmentation|segmentations|label|labels|labelstr|mask|masks|msk|gt)([/_.-]|$)",
                         re.IGNORECASE)
# datatype code -> (array typecode, bytes per voxel); the integer and float types volumes are stored in
NIFTI_TYPES = {2: ("B", 1), 4: ("h", 2), 8: ("i", 4), 16: ("f", 4), 64: ("d", 8), 256: ("b", 1),
               512: ("H", 2), 768: ("I", 4)}


def is_volume(path):
    lower = path.lower()
    return lower.endswith((".nii.gz", ".nii")) and not LABEL_WORDS.search(lower)


def open_volume(path):
    return gzip.open(path, "rb") if path.lower().endswith(".gz") else open(path, "rb")


def nifti_header(path):
    """(endian, dims, spacings, datatype, vox_offset, slope, inter) from a NIfTI-1 header, or None."""
    try:
        with open_volume(path) as handle:
            raw = handle.read(NIFTI_HEADER)
    except (OSError, EOFError, ValueError):
        return None
    if len(raw) < NIFTI_HEADER:
        return None
    for endian in "<>":
        if struct.unpack(endian + "i", raw[:4])[0] == NIFTI_HEADER:
            break
    else:
        return None
    dim = struct.unpack(endian + "8h", raw[40:56])
    datatype = struct.unpack(endian + "h", raw[70:72])[0]
    pixdim = struct.unpack(endian + "8f", raw[76:108])
    vox_offset, slope, inter = struct.unpack(endian + "3f", raw[108:120])
    if not 3 <= dim[0] <= 7 or any(size < 1 for size in dim[1:4]):
        return None
    return endian, dim[1:dim[0] + 1], pixdim[1:4], datatype, int(vox_offset), slope, inter


def geometry_of(header):
    """The three spatial axes' sizes and spacings, sorted, so an axis order does not change it."""
    if not header:
        return None
    _endian, dims, spacings, _datatype, _offset, _slope, _inter = header
    axes = sorted("%dx%.3f" % (size, abs(spacing)) for size, spacing in zip(dims[:3], spacings))
    extra = "".join("x%d" % size for size in dims[3:] if size > 1)
    return ",".join(axes) + extra


def signatures_of(path):
    """(sha256 of the voxel bytes, scaled sum with count) of one volume, or ('', '') when unreadable."""
    import array
    import hashlib
    header = nifti_header(path)
    if not header or header[3] not in NIFTI_TYPES:
        return "", ""
    endian, dims, _spacings, datatype, offset, slope, inter = header
    typecode, width = NIFTI_TYPES[datatype]
    count = 1
    for size in dims:
        count *= size
    digest, total = hashlib.sha256(), 0
    try:
        with open_volume(path) as handle:
            handle.read(max(offset, NIFTI_HEADER))
            left = count * width
            while left > 0:
                block = handle.read(min(left, 64 * 1024 * 1024))
                if not block or len(block) % width:
                    return "", ""
                left -= len(block)
                digest.update(block)
                values = array.array(typecode)
                values.frombytes(block)
                if (endian == ">") != (sys.byteorder == "big"):
                    values.byteswap()
                total += sum(values)
    except (OSError, EOFError, ValueError, MemoryError):
        return "", ""
    if slope and slope == slope:
        total = total * slope + (inter if inter == inter else 0) * count
    return digest.hexdigest(), "%d:%.0f" % (count, total)


def fingerprint_shared(db, folders, workers=1, log=None, budget=None):
    """Read whole only the volumes whose geometry a volume of another set shares.

    Summing voxels holds Python's lock, so the reads run in processes, a batch at a time; once
    budget seconds have gone no further batch starts, the volumes left keep blank signatures and
    the table's nifti_read says how many were read, so a pass that would outrun the job's wall
    time still writes its table."""
    rows = db.execute(
        "SELECT v.dataset, v.path FROM volume v WHERE EXISTS (SELECT 1 FROM volume w"
        " WHERE w.geometry = v.geometry AND w.dataset != v.dataset) ORDER BY v.dataset, v.path").fetchall()
    if log:
        log("%d volumes share a geometry with another set's; reading their voxels" % len(rows))
    started, done, step = time.time(), 0, max(1, workers) * 8
    with ProcessPoolExecutor(max_workers=max(1, workers)) as pool:
        for first in range(0, len(rows), step):
            if budget is not None and time.time() - started > budget:
                if log:
                    log("the voxel budget is spent: %d of %d volumes read" % (done, len(rows)))
                break
            batch = rows[first:first + step]
            paths = [os.path.join(folders[ident], path) for ident, path in batch]
            for (ident, path), (voxels, vsum) in zip(batch, pool.map(signatures_of, paths)):
                db.execute("UPDATE volume SET voxels = ?, vsum = ? WHERE dataset = ? AND path = ?",
                           (voxels, vsum, ident, path))
            done += len(batch)
            db.commit()
            if log and done % 200 < step:
                log("%d of %d volumes read, %.0f s" % (done, len(rows), time.time() - started))
    db.commit()


# The ledger.

SCHEMA = """
CREATE TABLE dataset(id TEXT PRIMARY KEY, folder TEXT, files INTEGER, bytes INTEGER);
CREATE TABLE file(dataset TEXT, path TEXT, sha256 TEXT, bytes INTEGER, stem TEXT);
CREATE TABLE dicom(dataset TEXT, folder TEXT, patient TEXT, study TEXT, series TEXT);
CREATE TABLE volume(dataset TEXT, path TEXT, geometry TEXT, voxels TEXT, vsum TEXT);
"""


def build(sets, out, workers=1, log=None, budget=None):
    """Write the ledger and the overlap table into out; returns the table."""
    os.makedirs(out, exist_ok=True)
    ledger = os.path.join(out, LEDGER)
    if os.path.exists(ledger + ".tmp"):
        os.remove(ledger + ".tmp")
    db = sqlite3.connect(ledger + ".tmp")
    db.executescript(SCHEMA)
    for ident, folder in sets:
        started = time.time()
        files, size = load_set(db, ident, folder, workers)
        if log:
            log("%s: %d files, %d bytes, %.0f s" % (ident, files, size, time.time() - started))
    db.execute("CREATE INDEX volume_geometry ON volume(geometry)")
    fingerprint_shared(db, dict(sets), workers, log, budget)
    db.executescript("""
CREATE INDEX file_sha ON file(sha256);
CREATE INDEX dicom_series ON dicom(series);
CREATE INDEX dicom_study ON dicom(study);
""")
    db.commit()
    table = overlap(db)
    db.close()
    os.replace(ledger + ".tmp", ledger)
    write_overlap(table, os.path.join(out, OVERLAP))
    return table


def load_set(db, ident, folder, workers):
    count, total, paths = 0, 0, []
    batch = []
    for digest, size, path in file_rows(folder):
        batch.append((ident, path, digest, size, stem_of(path)))
        paths.append(path)
        count += 1
        total += size
        if len(batch) >= 50000:
            db.executemany("INSERT INTO file VALUES (?,?,?,?,?)", batch)
            batch = []
    db.executemany("INSERT INTO file VALUES (?,?,?,?,?)", batch)
    db.execute("INSERT INTO dataset VALUES (?,?,?,?)", (ident, folder, count, total))
    candidates = dicom_candidates(paths)
    volumes = [path for path in paths if is_volume(path)]
    del paths
    with ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
        headers = pool.map(lambda item: (item[0], first_header(folder, item[1])), sorted(candidates.items()))
        db.executemany("INSERT INTO dicom VALUES (?,?,?,?,?)",
                       ((ident, sub, h[0], h[1], h[2]) for sub, h in headers if h))
        shapes = pool.map(lambda path: (path, geometry_of(nifti_header(os.path.join(folder, path)))), volumes)
        db.executemany("INSERT INTO volume VALUES (?,?,?,'','')",
                       ((ident, path, key) for path, key in shapes if key))
    db.commit()
    return count, total


def overlap(db):
    """The overlap table from the ledger: counts per set and per pair, no names."""
    db.create_function("stem_counts", 1, lambda s: 1 if stem_counts(s) else 0)
    db.create_function("patient_counts", 1, lambda p: 1 if patient_counts(p or "") else 0)
    db.executescript("""
CREATE TEMP TABLE set_sha AS SELECT DISTINCT dataset, sha256, bytes FROM file WHERE bytes >= %d;
CREATE INDEX temp.set_sha_sha ON set_sha(sha256);
CREATE TEMP TABLE set_stem AS SELECT DISTINCT dataset, stem FROM file WHERE stem_counts(stem);
CREATE INDEX temp.set_stem_stem ON set_stem(stem);
CREATE TEMP TABLE set_uid AS
  SELECT DISTINCT dataset, lower(series) AS uid FROM dicom WHERE series != ''
  UNION SELECT DISTINCT dataset, lower(study) FROM dicom WHERE study != '';
CREATE INDEX temp.set_uid_uid ON set_uid(uid);
""" % DATA_BYTES)
    sets = {}
    for ident, files, size in db.execute("SELECT id, files, bytes FROM dataset ORDER BY id"):
        sets[ident] = {"files": files, "bytes": size}
    for ident, series, studies, patients in db.execute(
            "SELECT dataset, count(DISTINCT nullif(series,'')), count(DISTINCT nullif(study,'')),"
            " count(DISTINCT nullif(patient,'')) FROM dicom GROUP BY dataset"):
        sets[ident].update({"dicom_series": series, "dicom_studies": studies, "patients": patients})
    for ident, volumes, read in db.execute(
            "SELECT dataset, count(*), sum(voxels != '') FROM volume GROUP BY dataset"):
        sets[ident].update({"nifti_volumes": volumes, "nifti_read": read or 0})
    for ident, unique in db.execute(
            "SELECT a.dataset, sum(a.bytes) FROM set_sha a WHERE NOT EXISTS"
            " (SELECT 1 FROM set_sha b WHERE b.sha256 = a.sha256 AND b.dataset != a.dataset)"
            " GROUP BY a.dataset"):
        sets[ident]["unique_bytes"] = unique
    for entry in sets.values():
        for key in ("dicom_series", "dicom_studies", "patients", "unique_bytes", "nifti_volumes", "nifti_read"):
            entry.setdefault(key, 0)
    pairs = {}
    queries = {
        "same_files": "SELECT a.dataset, b.dataset, count(*) FROM set_sha a JOIN set_sha b"
                      " ON a.sha256 = b.sha256 AND a.dataset < b.dataset GROUP BY 1, 2",
        "same_bytes": "SELECT a.dataset, b.dataset, sum(a.bytes) FROM set_sha a JOIN set_sha b"
                      " ON a.sha256 = b.sha256 AND a.dataset < b.dataset GROUP BY 1, 2",
        "series": "SELECT a.dataset, b.dataset, count(DISTINCT a.series) FROM dicom a JOIN dicom b"
                  " ON a.series = b.series AND a.dataset < b.dataset WHERE a.series != '' GROUP BY 1, 2",
        "studies": "SELECT a.dataset, b.dataset, count(DISTINCT a.study) FROM dicom a JOIN dicom b"
                   " ON a.study = b.study AND a.dataset < b.dataset WHERE a.study != '' GROUP BY 1, 2",
        "patients": "SELECT a.dataset, b.dataset, count(DISTINCT a.patient) FROM dicom a JOIN dicom b"
                    " ON a.patient = b.patient AND a.dataset < b.dataset WHERE patient_counts(a.patient)"
                    " GROUP BY 1, 2",
        "names": "SELECT a.dataset, b.dataset, count(*) FROM set_stem a JOIN set_stem b"
                 " ON a.stem = b.stem AND a.dataset < b.dataset GROUP BY 1, 2",
        "names_to_uids": "SELECT s.dataset, u.dataset, count(DISTINCT s.stem) FROM set_stem s JOIN set_uid u"
                         " ON s.stem = u.uid AND s.dataset != u.dataset GROUP BY 1, 2",
        "same_geometry": "SELECT a.dataset, b.dataset, count(DISTINCT a.path) FROM volume a JOIN volume b"
                         " ON a.geometry = b.geometry AND a.dataset < b.dataset GROUP BY 1, 2",
        "same_values": "SELECT a.dataset, b.dataset, count(DISTINCT a.path) FROM volume a JOIN volume b"
                       " ON a.geometry = b.geometry AND a.vsum = b.vsum AND a.dataset < b.dataset"
                       " WHERE a.vsum != '' GROUP BY 1, 2",
        "same_voxels": "SELECT a.dataset, b.dataset, count(DISTINCT a.path) FROM volume a JOIN volume b"
                       " ON a.voxels = b.voxels AND a.dataset < b.dataset WHERE a.voxels != '' GROUP BY 1, 2",
    }
    for key, query in queries.items():
        for a, b, value in db.execute(query):
            first, second = sorted((a, b))
            entry = pairs.setdefault((first, second), {})
            entry[key] = entry.get(key, 0) + (value or 0)
    pair_list = []
    for (a, b), counts in sorted(pairs.items()):
        row = {"a": a, "b": b}
        for key in queries:
            row[key] = counts.get(key, 0)
        pair_list.append(row)
    return {"format": FORMAT, "built_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "data_bytes_floor": DATA_BYTES, "sets": sets, "pairs": pair_list}


# The public table.

OLD_PAIR_KEYS = {"a", "b", "same_files", "same_bytes", "series", "studies", "patients", "names", "names_to_uids"}
OLD_SET_KEYS = {"files", "bytes", "dicom_series", "dicom_studies", "patients", "unique_bytes"}
PAIR_KEYS = OLD_PAIR_KEYS | {"same_geometry", "same_values", "same_voxels"}
SET_KEYS = OLD_SET_KEYS | {"nifti_volumes", "nifti_read"}


def public_problems(table):
    """What would keep the table on the grid: anything but ids and whole numbers where they belong."""
    problems = []
    if not isinstance(table, dict) or table.get("format") not in (FORMAT, OLD_FORMAT):
        return ["not an overlap table of format %s" % FORMAT]
    pair_keys, set_keys = (PAIR_KEYS, SET_KEYS) if table["format"] == FORMAT else (OLD_PAIR_KEYS, OLD_SET_KEYS)
    if set(table) - {"format", "built_at", "data_bytes_floor", "sets", "pairs"}:
        problems.append("keys beyond the table's own")
    if not re.match(r"^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ$", str(table.get("built_at", ""))):
        problems.append("built_at is no UTC time")
    sets = table.get("sets")
    if not isinstance(sets, dict):
        return problems + ["sets is not a mapping"]
    for ident, entry in sets.items():
        if not ID_SHAPE.match(ident) or not isinstance(entry, dict) or set(entry) != set_keys:
            problems.append("set %r is not an id with its counts" % ident[:40])
        elif not all(whole(value) for value in entry.values()):
            problems.append("set %s has a count that is no whole number" % ident)
    for row in table.get("pairs", []):
        if not isinstance(row, dict) or set(row) != pair_keys:
            problems.append("a pair without exactly its counts")
            continue
        if row["a"] not in sets or row["b"] not in sets or not row["a"] < row["b"]:
            problems.append("a pair that names no two sets in order")
        if not all(whole(row[key]) for key in pair_keys - {"a", "b"}):
            problems.append("a pair with a count that is no whole number")
    return problems


def whole(value):
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def table_text(table):
    return json.dumps(table, indent=1, sort_keys=True, ensure_ascii=True) + "\n"


def write_overlap(table, path):
    problems = public_problems(table)
    if problems:
        raise ValueError("the overlap table would carry more than counts: " + "; ".join(problems))
    with io.open(path + ".tmp", "w", encoding="ascii", newline="\n") as handle:
        handle.write(table_text(table))
    os.replace(path + ".tmp", path)


def read_overlap(path):
    with io.open(path, encoding="ascii") as handle:
        return json.load(handle)


def add_to_tree(overlap_path, tree_path):
    """Add lineage/OVERLAP.json to a git/trees body, after the public check; True when added."""
    table = read_overlap(overlap_path)
    if public_problems(table):
        return False
    with io.open(tree_path, encoding="ascii") as handle:
        tree = json.load(handle)
    tree["tree"] = [entry for entry in tree["tree"] if entry.get("path") != "lineage/" + OVERLAP]
    tree["tree"].append({"path": "lineage/" + OVERLAP, "mode": "100644", "type": "blob",
                         "content": table_text(table)})
    with io.open(tree_path + ".tmp", "w", encoding="ascii", newline="\n") as handle:
        handle.write(json.dumps(tree, sort_keys=True))
    os.replace(tree_path + ".tmp", tree_path)
    return True


# The command line.

def log_line(text):
    sys.stderr.write("%s %s\n" % (time.strftime("%H:%M:%S"), text))
    sys.stderr.flush()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command")
    run = sub.add_parser("build", help="the ledger and the overlap table from every frozen set")
    run.add_argument("--plan", help="grid/freeze-plan.tsv: id TAB folder per line")
    run.add_argument("--shared", help="the promoter's shared tree, each <id>/ frozen beside raw/")
    run.add_argument("--out", required=True)
    run.add_argument("--workers", type=int, default=1)
    run.add_argument("--voxel-hours", type=float, default=8.0,
                     help="no voxel batch starts after this many hours (the job's wall time is 12)")
    look = sub.add_parser("check", help="whether an overlap table holds counts alone")
    look.add_argument("overlap")
    pack = sub.add_parser("tree", help="add the overlap table to freeze.sh report's git tree")
    pack.add_argument("overlap")
    pack.add_argument("tree")
    args = parser.parse_args(argv)
    if args.command == "build":
        sets = sets_from(args.plan, args.shared)
        if not sets:
            parser.error("no frozen set found from --plan or --shared")
        log_line("%d frozen sets to read" % len(sets))
        table = build(sets, args.out, args.workers, log_line, args.voxel_hours * 3600)
        print("%d sets, %d pairs that share something; %s" % (len(table["sets"]), len(table["pairs"]),
                                                            os.path.join(args.out, OVERLAP)))
        return 0
    if args.command == "check":
        problems = public_problems(read_overlap(args.overlap))
        for problem in problems:
            print(problem)
        return 1 if problems else 0
    if args.command == "tree":
        if not add_to_tree(args.overlap, args.tree):
            sys.stderr.write("the overlap table is not counts alone; left out of the report\n")
            return 1
        return 0
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
