# Frozen: each set on the grid, every file hashed

Source: the thread "Frozen dataset manifests", 2026-10-23, the owner's ask of that day: every
dataset on the grid comes with a file that freezes its tree and hashes it, so a copy is shown
identical and its size, files and folders are read at once, without scanning the data again.

frozen/<id>.json is the public copy of the set's FROZEN.json (tools/freeze.py): the number of
files and bytes, the tree's sha256, which stands for every name and every byte, the outline by
depth (how many folders and files at each level), the counts and bytes by known extension, and,
where a set has at most twelve, its top folders with their own totals and hashes. It names no file
and nothing below the top, and no top folder where there are more of them, since a set held under
an agreement may name its subjects in its folders and files, and this repository is public.

The whole freeze stays beside the data on the grid: FROZEN.json, with every folder down to two
levels and the largest files, and FROZEN.files.tsv.gz, one line per file (sha256, bytes, path).

    python3 tools/freeze.py show frozen/<id>.json          # the totals and top folders, here
    python3 tools/freeze.py show <folder> --under raw/x --depth 2   # any folder, on the grid
    python3 tools/freeze.py verify <folder> --quick        # names and sizes, minutes
    python3 tools/freeze.py verify <folder>                # every byte again

The record's `measured` carries the freeze's bytes, files, tree_sha256 and date
(`tools/freeze.py measured`), and `python3 tools/freeze.py check`, in scripts/check.sh, fails when
a copy here and its record disagree, or when a copy names anything below the top. The census lists
a set on the grid with no tree_sha256 under what the records still lack, and counts the sets
frozen.

The promoter freezes each set it installs, from the hashes it has just checked, and its record
update brings this file with it. The sets that landed before are frozen by grid/freeze.sh, only on
the owner's word with the number of jobs; `python3 tools/freeze.py plan` lists them.
