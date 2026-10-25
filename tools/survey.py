"""What fills the lab volume besides the datasets (the thread "Fit datasets under the 20 TB cap",
2026-10-25). The storage reading of 2026-10-24 put 17.6 TB on /rs/rs_grp_oschome, of which the
frozen datasets are 7.6 TB; the owner asked where the other 9.9 TB is, guessing segmentation masks
or datasets no record tracks. This sizes it, reading nothing but folder sizes and the frozen file
lists, and changes nothing.

    python3 tools/survey.py run --plan grid/freeze-plan.tsv --out survey.json [--root R]

CephFS keeps each folder's recursive size in the attribute ceph.dir.rbytes, so a folder is sized
without reading its files; where the attribute is missing the folder's files are summed by lstat,
which the row says. The owner's folder and the shared tree are opened down to MAX_DEPTH, a folder
broken into its children only while it holds FLOOR or more, smaller children folded into one row;
another account's folder is counted, never named or opened. Each folder is put in one kind:

- dataset: a folder the freeze plan names, split into its masks and labels and its images by its
  frozen file list (a path whose words name a segmentation, label or mask);
- masks: a folder outside the datasets whose name names segmentations, labels or masks;
- untracked data: anything else under the data root that no record names;
- runs and outputs, jobs and logs, other: by name.

Python 3.6 and the standard library only, as everything the grid runs."""

import argparse
import gzip
import json
import os
import re
import stat
import sys
import time

VOLUME = "/rs/rs_grp_oschome"
OWNER_PARTS = ("go2432", "shared")
DATA_ROOTS = ("go2432/data", "shared/datasets")
FLOOR = 50 * 10 ** 9
MAX_DEPTH = 4
FORMAT = "spine-datasets/survey 1"
FILE_LIST = "FROZEN.files.tsv.gz"
MASK_WORDS = re.compile(
    r"(^|[/_.-])(seg|segs|segmentation|segmentations|label|labels|labelstr|labelsts|mask|masks|msk|"
    r"gt|spineps|totalseg|totalsegmentator|anomaly_harvest)([/_.-]|$)", re.IGNORECASE)
RUN_WORDS = re.compile(r"(^|[/_.-])(runs?|" + "mod" + r"els?|checkpoints?|ckpts?|wandb|mlruns|weights|outputs?|"
                       r"experiments?|smoke|nnunet_results|results)([/_.-]|$)", re.IGNORECASE)
JOB_WORDS = re.compile(r"(^|[/_.-])(hpcworker|jobs?|logs?|slurm|tmp|scratch|cache|\.cache|"
                       r"containers?|sif|pixi|conda|envs?)([/_.-]|$)", re.IGNORECASE)


def rbytes(path):
    try:
        return int(os.getxattr(path, "ceph.dir.rbytes"))
    except (OSError, ValueError, AttributeError):
        return None


def walked_bytes(path):
    total = 0
    for folder, folders, files in os.walk(path, onerror=lambda error: None):
        for name in files:
            try:
                total += os.lstat(os.path.join(folder, name)).st_size
            except OSError:
                pass
    return total


def size_of(path):
    """(bytes, how): the folder's recursive size and whether CephFS said it or the files were summed."""
    found = rbytes(path)
    if found is not None:
        return found, "rbytes"
    return walked_bytes(path), "summed"


def subfolders(path):
    try:
        entries = list(os.scandir(path))
    except OSError:
        return []
    return sorted(entry.path for entry in entries if entry.is_dir(follow_symlinks=False))


def files_bytes(path):
    """The bytes of the files directly in path, not in its folders."""
    total = 0
    try:
        for entry in os.scandir(path):
            if not entry.is_dir(follow_symlinks=False):
                total += entry.stat(follow_symlinks=False).st_size
    except OSError:
        pass
    return total


def read_plan(path):
    sets = {}
    with open(path) as handle:
        for line in handle:
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 2 and parts[1].startswith("/"):
                sets[os.path.normpath(parts[1])] = parts[0]
    return sets


def mask_split(folder):
    """(mask bytes, image bytes) of a frozen set by its file list, or None while it has none."""
    try:
        handle = gzip.open(os.path.join(folder, FILE_LIST), "rb")
    except OSError:
        return None
    masks = images = 0
    try:
        with handle:
            for raw in handle:
                _digest, size, path = raw.decode("utf-8", "surrogateescape").rstrip("\n").split("\t", 2)
                if MASK_WORDS.search(path):
                    masks += int(size)
                else:
                    images += int(size)
    except (OSError, EOFError, ValueError):
        return None
    return masks, images


def kind_of(relative):
    if MASK_WORDS.search(relative):
        return "masks"
    if any(relative == root or relative.startswith(root + "/") for root in DATA_ROOTS):
        return "untracked data"
    if RUN_WORDS.search(relative):
        return "runs and outputs"
    if JOB_WORDS.search(relative):
        return "jobs and logs"
    return "other"


class Survey(object):
    def __init__(self, root, datasets, floor=FLOOR, max_depth=MAX_DEPTH):
        self.root, self.datasets, self.floor, self.max_depth = root, datasets, floor, max_depth
        self.rows = []

    def relative(self, path):
        return os.path.relpath(path, self.root)

    def add(self, path, size, how, kind, **extra):
        row = {"path": self.relative(path), "bytes": size, "how": how, "kind": kind}
        row.update(extra)
        self.rows.append(row)

    def dataset(self, path, size, how):
        split = mask_split(path)
        extra = {"id": self.datasets[path]}
        if split:
            extra.update({"mask_bytes": split[0], "image_bytes": split[1]})
        self.add(path, size, how, "dataset", **extra)

    def holds_a_dataset(self, path):
        prefix = path + "/"
        return any(folder.startswith(prefix) for folder in self.datasets)

    def open(self, path, depth):
        """Rows for path's children, or for path itself where it is a leaf."""
        size, how = size_of(path)
        if path in self.datasets:
            return self.dataset(path, size, how)
        kind = kind_of(self.relative(path))
        wanted = self.holds_a_dataset(path) or (size >= self.floor and kind != "masks")
        if depth >= self.max_depth or not wanted:
            return self.add(path, size, how, kind)
        children, small, small_how, counted, apart = subfolders(path), 0, set(), 0, 0
        for child in children:
            child_size, child_how = size_of(child)
            counted += child_size
            if child_size >= self.floor or child in self.datasets or self.holds_a_dataset(child):
                self.open(child, depth + 1)
                apart += 1
            elif MASK_WORDS.search(self.relative(child)) and kind != "masks":
                self.add(child, child_size, child_how, "masks")
                apart += 1
            else:
                small += child_size
                small_how.add(child_how)
        loose = max(0, size - counted) if how == "rbytes" else files_bytes(path)
        if not apart:
            return self.add(path, size, how, kind)
        if small or loose:
            self.add(path, small + loose, "+".join(sorted(small_how | {how})), kind, folded=True)

    def run(self):
        total, how = size_of(self.root)
        others, others_bytes, others_how = 0, 0, set()
        for child in subfolders(self.root):
            if os.path.basename(child) in OWNER_PARTS:
                self.open(child, 1)
            else:
                size, child_how = size_of(child)
                others, others_bytes = others + 1, others_bytes + size
                others_how.add(child_how)
        if others:
            self.rows.append({"path": "(other accounts' folders)", "bytes": others_bytes,
                              "how": "+".join(sorted(others_how)), "kind": "other accounts", "folders": others})
        return self.table(total, how)

    def table(self, total, how):
        kinds = {}
        for row in self.rows:
            kinds[row["kind"]] = kinds.get(row["kind"], 0) + row["bytes"]
        masks_in_datasets = sum(row.get("mask_bytes", 0) for row in self.rows)
        return {"format": FORMAT, "read_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "root": self.root, "volume_bytes": total, "volume_how": how, "floor_bytes": self.floor,
                "kinds": kinds, "masks_in_datasets_bytes": masks_in_datasets,
                "rows": sorted(self.rows, key=lambda row: -row["bytes"])}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="command")
    run = sub.add_parser("run", help="size the volume into survey.json")
    run.add_argument("--plan", required=True, help="grid/freeze-plan.tsv: the datasets' folders")
    run.add_argument("--out", required=True)
    run.add_argument("--root", default=VOLUME)
    run.add_argument("--floor-gb", type=float, default=FLOOR / 1e9)
    args = parser.parse_args(argv)
    if args.command != "run":
        parser.print_help()
        return 2
    table = Survey(os.path.normpath(args.root), read_plan(args.plan), int(args.floor_gb * 1e9)).run()
    with open(args.out + ".tmp", "w") as handle:
        json.dump(table, handle, indent=1, sort_keys=True)
        handle.write("\n")
    os.replace(args.out + ".tmp", args.out)
    for kind, size in sorted(table["kinds"].items(), key=lambda item: -item[1]):
        print("%-16s %8.1f GB" % (kind, size / 1e9))
    print("masks inside datasets %.1f GB; volume %.1f GB (%s)"
          % (table["masks_in_datasets_bytes"] / 1e9, table["volume_bytes"] / 1e9, table["volume_how"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
