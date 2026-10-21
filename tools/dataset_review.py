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
  - an added line in a record, a manifest or a letter, or the pull request's title or body, with a
    word the confidentiality rule bans (CONTRIBUTING.md, "The confidentiality rule, first");
  - a record whose history lost or changed an earlier entry (history only grows);
  - a token, key or signed link in the title or body (check_docs.py holds the files to the same);
  - a data file added to the repository (an image, an archive, a volume, a table of rows), outside
    docs/ and tests/, where it is flagged instead, since a figure or a fixture may belong there;
  - a record moved to fetched without a manifest, or with a grid_path outside the shared tree.
- FLAG, written in the report for whoever merges, the check stays green:
  - a line that reads as something binding done in the owner's name (signed, agreed, paid,
    attested, accepted terms), which only the owner may do;
  - a licence or link changed other than by replacing "to confirm on the page";
  - a non-commercial or no-derivatives licence;
  - a change to the promoter's own code or budget (tools/promote.py, grid/promote.sh,
    grid/promote.json), which runs as the owner on the grid.
- NOTE: a CT manifest while X-ray sets still wait to be fetched; the promoter takes X-ray first.

The report goes to the job's log and, on GitHub, to the job's summary page.

`manifest` writes a manifest from what the source itself publishes, for the routes whose API
gives every file's size and checksum: Mendeley Data (sha256) and Zenodo (md5). It needs the
network, so it runs on a collaborator's own machine or on the grid, never in the check.

    python3 tools/dataset_review.py check
    python3 tools/dataset_review.py diff --base origin/main
    python3 tools/dataset_review.py manifest ID --mendeley DATASET --version N
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
        if record.get("status") != "fetched" or not record.get("grid_path", "").startswith(SHARED):
            continue
        if not (folder / path.name).exists():
            report.add("FAIL", "datasets/%s says fetched into the shared tree but has no manifest" % path.name)
    return report


# diff: what a pull request adds.

def git(*args, root=ROOT):
    return subprocess.run(["git", *args], cwd=root, check=True, capture_output=True, text=True).stdout


def changed_files(base, root=ROOT):
    """(status, path) of every file the change adds, modifies or deletes since it left base."""
    out = git("diff", "--name-status", "--no-renames", base + "...HEAD", root=root)
    return [tuple(line.split("\t", 1)) for line in out.splitlines() if line]


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


def review_pull_request_text(report):
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    if not event_path or not os.path.exists(event_path):
        return
    with open(event_path, encoding="utf-8") as handle:
        pull = json.load(handle).get("pull_request") or {}
    for where, text in (("the title", pull.get("title") or ""), ("the description", pull.get("body") or "")):
        review_text("the pull request's " + where[4:], text, report)
        for name, pattern in SECRET_PATTERNS:
            if pattern.search(text):
                report.add("FAIL", "the pull request's %s holds what looks like a %s" % (where[4:], name))


def review_diff(base, root=ROOT, report=None):
    report = report or Report()
    for status, path in changed_files(base, root=root):
        if status == "D":
            continue
        if path.lower().endswith(DATA_SUFFIXES):
            level = "FLAG" if path.startswith(("docs/", "tests/")) else "FAIL"
            report.add(level, "%s is a data file; data stay on the grid and the record says where" % path)
            continue
        if path in TRUSTED_PATHS:
            report.add("FLAG", "%s runs as the owner on the grid; the owner reads this change before merging" % path)
        if SCANNED.match(path):
            for line in added_lines(base, path, root=root):
                review_text(path, line, report)
        if path.startswith("datasets/") and path.endswith(".json") and path != "datasets/README.md":
            review_record(path, base, report, root=root)
        if path.startswith("manifests/") and path.endswith(".json") and status == "A":
            record_path = root / "datasets" / Path(path).name
            if record_path.exists() and read_json(record_path).get("group") == "ct" and xray_waiting(root):
                report.add("NOTE", "%s is a CT set while %d X-ray sets wait; the promoter takes X-ray first"
                           % (path, len(xray_waiting(root))))
    review_pull_request_text(report)
    return report


# manifest: from the source's own file list.

MENDELEY_FILES = "https://data.mendeley.com/public-api/datasets/%s/files?folder_id=root&version=%s"
ZENODO_RECORD = "https://zenodo.org/api/records/%s"


def fetch_json(url):
    import urllib.request
    with urllib.request.urlopen(url, timeout=60) as answer:
        return json.load(answer)


def mendeley_files(listing):
    """The manifest's file entries from Mendeley's public file list."""
    files = []
    for item in listing:
        details = item["content_details"]
        files.append({
            "path": "raw/" + item["filename"], "url": details["download_url"], "bytes": details["size"],
            "sha256": details["sha256_hash"], "verified_against": "Mendeley Data's public API",
        })
    return files


def zenodo_files(record):
    files = []
    for item in record["files"]:
        algorithm, _, value = item["checksum"].partition(":")
        if algorithm != "md5":
            raise ValueError("Zenodo gave a %s checksum for %s" % (algorithm, item["key"]))
        files.append({
            "path": "raw/" + item["key"], "url": item["links"]["self"], "bytes": item["size"],
            "md5": value, "verified_against": "Zenodo's API",
        })
    return files


def build_manifest(record, files, today):
    return {
        "id": record["id"], "source": record["link"], "licence": record["licence"], "date": today, "files": files, "bytes_total": sum(entry["bytes"] for entry in files),
    }


def write_manifest(args, root=ROOT):
    from datetime import datetime, timezone
    record = read_json(root / "datasets" / (args.id + ".json"))
    if args.mendeley:
        files = mendeley_files(fetch_json(MENDELEY_FILES % (args.mendeley, args.version)))
    else:
        files = zenodo_files(fetch_json(ZENODO_RECORD % args.zenodo))
    manifest = build_manifest(record, files, datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    path = root / "manifests" / (args.id + ".json")
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(manifest, indent=1, ensure_ascii=True) + "\n", encoding="ascii")
    print("wrote %s: %d files, %d bytes" % (path.relative_to(root), len(files), manifest["bytes_total"]))
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("check", help="every manifest in the tree holds")
    diff = sub.add_parser("diff", help="review what a pull request adds")
    diff.add_argument("--base", required=True, help="the branch the pull request goes into, e.g. origin/main")
    make = sub.add_parser("manifest", help="write manifests/<id>.json from the source's own file list")
    make.add_argument("id")
    where = make.add_mutually_exclusive_group(required=True)
    where.add_argument("--mendeley", help="the Mendeley Data dataset id, e.g. xkt857dsxk")
    where.add_argument("--zenodo", help="the Zenodo record number")
    make.add_argument("--version", default="1", help="the Mendeley version")
    args = parser.parse_args(argv)
    if args.command == "manifest":
        return write_manifest(args)
    report = check_tree() if args.command == "check" else check_tree(report=review_diff(args.base))
    report.publish()
    return 1 if report.failed() else 0


if __name__ == "__main__":
    sys.exit(main())
