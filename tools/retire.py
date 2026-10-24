"""Retiring a set on the grid: what a merged storage request's retirement would delete, checked
against the set's freeze, and what stays so the set can be rebuilt.

Source: the thread "Check frozen manifest job", 2026-10-24, the owner's ask of that day: remove
datasets to keep working under the 20 TB cap, keep what is needed to regenerate any set removed,
and trigger the removals from the textbook's artifact. The planner (tools/storage.py) turns the
artifact's selection into a request the owner merges; this script is the grid's side of a
retirement in that request (docs/research/lineage-and-retirement.md, "Retiring a set").

    python3 tools/retire.py actions REQUEST
        the request's actions, one line each: kind TAB id TAB place TAB folder TAB tree
    python3 tools/retire.py plan FOLDER --id ID --tree SHA256 --out DIR
        checks the folder against its freeze and writes DIR/<id>.json, the counts, and
        DIR/<id>.delete, the paths a retirement would delete, NUL-separated
    python3 tools/retire.py bundle DIR
        the body of a POST to git/trees with storage/retire/<id>.json for every plan in DIR

A plan stands only when all of these hold, and otherwise it says why and lists nothing:

- the folder is a set's own folder under one of the data roots, with no link anywhere on its path,
  so a path in a request can never reach the home, the lab's code or another set;
- its FROZEN.json names the tree hash the owner merged, and the file list is that hash's list;
- the folder holds exactly the files the freeze listed, at their sizes, so what goes is what the
  freeze stands for and the set can be proved rebuilt by its tree hash.

What stays is the freeze (FROZEN.json and its file list) and every file a rebuild from the source
could not give back or that is small next to the images: labels, masks, segmentations,
annotations, metadata, tables and texts. This script deletes nothing: deletion waits for the
owner's answer on whether a merged request may delete through the grid gate. It runs under the
grid's Python 3.6 as well as 3.12, so it uses nothing newer.
"""

import argparse
import gzip
import hashlib
import json
import os
import re
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import freeze  # noqa: E402

FORMAT = "spine-datasets/retire-plan 1"
ROOTS = ("/rs/rs_grp_oschome/go2432/data/", "/rs/rs_grp_oschome/shared/datasets/")
KEPT_WORDS = re.compile(r"seg|label|mask|annot|meta|manifest|split|readme|licen", re.IGNORECASE)
KEPT_EXTENSIONS = (".json", ".csv", ".tsv", ".txt", ".xml", ".md", ".pdf", ".yaml", ".yml",
                   ".xlsx", ".xls", ".html", ".py", ".sh")
ACTION_FIELDS = ("kind", "id", "place", "folder", "tree_sha256")


def read_actions(path):
    with open(path, encoding="utf-8") as handle:
        request = json.load(handle)
    if request.get("format") != "spine-datasets/storage-request 1":
        raise ValueError("%s is no storage request" % path)
    rows = []
    for action in request.get("actions", []):
        row = [str(action.get(field) or "-") for field in ACTION_FIELDS]
        if any("\t" in value or "\n" in value for value in row):
            raise ValueError("an action of %s holds a tab or a newline" % path)
        rows.append(row)
    return rows


def folder_problems(folder):
    if not folder.startswith("/") or os.path.normpath(folder) != folder:
        return ["the folder is not a plain absolute path"]
    root = next((root for root in ROOTS if folder.startswith(root)), None)
    if root is None:
        return ["the folder is under none of the data roots"]
    if not folder[len(root):] or folder[len(root):].startswith("."):
        return ["the folder is a data root itself, not a set's folder"]
    if os.path.realpath(folder) != folder:
        return ["the folder has a link on its path"]
    if not os.path.isdir(folder):
        return ["the folder is not there"]
    return []


def freeze_problems(folder, tree):
    summary_path = os.path.join(folder, freeze.SUMMARY)
    list_path = os.path.join(folder, freeze.FILE_LIST)
    if not (os.path.isfile(summary_path) and os.path.isfile(list_path)):
        return ["the folder is not frozen"]
    if freeze.read_summary(summary_path).get("tree_sha256") != tree:
        return ["the folder's freeze is not the one the request names"]
    with gzip.open(list_path, "rb") as handle:
        if hashlib.sha256(handle.read()).hexdigest() != tree:
            return ["the file list is not the one its tree hash names"]
    return []


def is_kept(path):
    """A file a retirement keeps: one whose path speaks of labels or metadata, or a small kind."""
    return bool(KEPT_WORDS.search(path)) or path.lower().endswith(KEPT_EXTENSIONS)


def drift_problems(folder, expected):
    actual = dict((path, (None, freeze.LINK_BYTES if os.path.islink(absolute) else info.st_size))
                  for path, absolute, info in freeze.walk(folder))
    missing, added, changed = freeze.compare(expected, actual)
    problems = []
    for word, paths in (("missing", missing), ("added", added), ("changed in size", changed)):
        if paths:
            problems.append("%d files %s since the freeze" % (len(paths), word))
    return problems


def plan(folder, ident, tree):
    """(counts, paths to delete); the paths are empty whenever a problem stands."""
    counts = {"format": FORMAT, "id": ident, "tree_sha256": tree,
              "planned_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    problems = folder_problems(folder) or freeze_problems(folder, tree)
    expected = {} if problems else freeze.read_file_list(folder)
    problems = problems or drift_problems(folder, expected)
    doomed = [] if problems else sorted((p for p in expected if not is_kept(p)), key=freeze.sort_key)
    kept = [] if problems else [p for p in expected if is_kept(p)]
    counts.update({
        "problems": problems,
        "files_to_delete": len(doomed),
        "bytes_to_delete": sum(max(expected[p][1], 0) for p in doomed),
        "files_kept": len(kept),
        "bytes_kept": sum(max(expected[p][1], 0) for p in kept),
    })
    return counts, doomed


def write_plan(folder, ident, tree, out):
    if not freeze.ID_SHAPE.match(ident) or not freeze.SHA256_SHAPE.match(tree):
        raise ValueError("the id or the tree hash is not in its shape")
    counts, doomed = plan(folder, ident, tree)
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, ident + ".delete.tmp"), "wb") as handle:
        for path in doomed:
            handle.write(path.encode("utf-8", "surrogateescape") + b"\0")
    os.replace(os.path.join(out, ident + ".delete.tmp"), os.path.join(out, ident + ".delete"))
    with open(os.path.join(out, ident + ".json"), "w", encoding="ascii") as handle:
        json.dump(counts, handle, indent=1, sort_keys=True)
        handle.write("\n")
    return counts


def bundle(folder):
    entries = []
    for name in sorted(os.listdir(folder)):
        ident = name[:-5] if name.endswith(".json") else ""
        if not freeze.ID_SHAPE.match(ident):
            continue
        with open(os.path.join(folder, name), encoding="ascii") as handle:
            counts = json.load(handle)
        if counts.get("format") != FORMAT or counts.get("id") != ident:
            continue
        text = json.dumps(counts, indent=1, sort_keys=True) + "\n"
        entries.append({"path": "storage/retire/%s.json" % ident, "mode": "100644", "type": "blob",
                        "content": text})
    return {"tree": entries}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="command")
    actions = sub.add_parser("actions")
    actions.add_argument("request")
    planner = sub.add_parser("plan")
    planner.add_argument("folder")
    planner.add_argument("--id", required=True)
    planner.add_argument("--tree", required=True)
    planner.add_argument("--out", required=True)
    bundler = sub.add_parser("bundle")
    bundler.add_argument("folder")
    args = parser.parse_args(argv)
    if args.command == "actions":
        for row in read_actions(args.request):
            print("\t".join(row))
        return 0
    if args.command == "plan":
        counts = write_plan(args.folder, args.id, args.tree, args.out)
        for problem in counts["problems"]:
            print("%s: %s" % (args.id, problem))
        print("%s: %d files (%.1f GB) to delete, %d files (%.1f GB) kept" % (
            args.id, counts["files_to_delete"], counts["bytes_to_delete"] / 1e9,
            counts["files_kept"], counts["bytes_kept"] / 1e9))
        return 1 if counts["problems"] else 0
    if args.command == "bundle":
        body = bundle(args.folder)
        if not body["tree"]:
            print("no plan to report", file=sys.stderr)
            return 1
        json.dump(body, sys.stdout)
        return 0
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
