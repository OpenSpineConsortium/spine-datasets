"""Every dataset record maps to a task, and every folder of the grid's data root to a record or a task.

The owner's ask of 2026-10-25 04:53 UTC: "just make sure every dataset on the grid maps to a task
which was opened, is opened or has been closed on the repo which has all those, for accounting
purposes". The tasks are this repository's issues. Each record under datasets/ carries the number
of its task in `task`: its "Obtain ..." task where tasks/TASKS.md opened one, else an
"Account for ..." task, opened and closed at once for a set that was on the grid before it had a
task (label accounting). A folder of the data root that holds no record's set (a bank derived from
other sets, a working folder, a set aside) is listed in grid/folders.json with the task that
accounts for it.

    python3 tools/accounting.py check    every record has a task, every folder a record or a task
    python3 tools/accounting.py show     the folders and records, side by side

The check reads files only, never GitHub, so it runs in scripts/check.sh: that a number names an
issue that exists is the board's and a person's to see, since an issue is never deleted here.
"""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATASETS = ROOT / "datasets"
FOLDERS = ROOT / "grid" / "folders.json"
KINDS = ("records", "derived", "working", "set-aside", "empty")


class AccountingError(Exception):
    pass


def records(folder=DATASETS):
    return {path.stem: json.loads(path.read_text(encoding="utf-8")) for path in sorted(folder.glob("*.json"))}


def is_task(value):
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def record_problems(found):
    return [f"datasets/{rid}.json: no task (a whole number naming this repository's issue)"
            for rid, record in found.items() if not is_task(record.get("task"))]


def folder_problems(ledger, found):
    problems = []
    for name, entry in sorted(ledger.get("folders", {}).items()):
        where = f"grid/folders.json: {name}"
        kind = entry.get("kind")
        if kind not in KINDS:
            problems.append(f"{where}: kind is one of {', '.join(KINDS)}")
        if kind == "records":
            named = entry.get("records") or []
            if not named:
                problems.append(f"{where}: names no record")
            problems += [f"{where}: no record datasets/{rid}.json" for rid in named if rid not in found]
        elif not is_task(entry.get("task")):
            problems.append(f"{where}: a folder no record holds needs the task that accounts for it")
        if not str(entry.get("what", "")).strip():
            problems.append(f"{where}: says nothing of what it holds")
    return problems


def load_ledger(path=FOLDERS):
    if not path.exists():
        return {"folders": {}}
    ledger = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(ledger.get("folders"), dict):
        raise AccountingError("grid/folders.json: no folders object")
    return ledger


def problems(folder=DATASETS, ledger_path=FOLDERS):
    found = records(folder)
    return record_problems(found) + folder_problems(load_ledger(ledger_path), found)


def show(folder=DATASETS, ledger_path=FOLDERS):
    found = records(folder)
    lines = [f"{rid}\t#{record.get('task')}\t{record.get('status')}" for rid, record in found.items()]
    for name, entry in sorted(load_ledger(ledger_path)["folders"].items()):
        target = ",".join(entry.get("records") or []) or f"#{entry.get('task')}"
        lines.append(f"folder {name}\t{entry.get('kind')}\t{target}")
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("action", choices=("check", "show"))
    args = parser.parse_args(argv)
    if args.action == "show":
        print(show())
        return 0
    found = problems()
    for line in found:
        print(line)
    if found:
        return 1
    print(f"accounting ok ({len(records())} records, {len(load_ledger()['folders'])} folders)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
