"""The storage planner: what the datasets take on the lab volume and in the owner's home, and
whether a trial combination of removals, fetches and moves fits under both caps.

Source: the thread "Check frozen manifest job", 2026-10-24, the owner's ask of that day: see the
drive usage, try combinations of datasets that fit under 20 TB, trigger the removals and additions
from the textbook's artifact, and keep some of the data in the owner's own home on the grid, which
holds 4 TB.

This script never touches the grid. It reads the records (datasets/<id>.json), the overlap table
(lineage/OVERLAP.json) and the latest reading of the volume (storage/VOLUME.json, copied by hand
or by a session from the grid's status word), and it writes:

- PLAN.json, the feed the artifact reads, which .github/workflows/storage.yml publishes on the
  branch storage-feed after every change to what it is made from: the volume, the home, the target, and every set
  with its size, place, reach and whether it can be rebuilt; ids and whole numbers only, never a
  path below the top folder;
- for `request`, a request file under storage/requests/, which a workflow offers as a pull request
  that names every set by name. The owner's merge of that pull request is his word for each set it
  names; nothing is deleted, fetched or moved before it, and a session never merges one.

A selection is a list of actions separated by commas or spaces: `-id` retires a held set (its
images go, its record, freeze and file list stay, so it can be rebuilt), `+id` fetches a set,
`id@home` and `id@lab` move a held set. Since a selection may begin with a dash, it is
given after `--`: `python3 tools/storage.py check -- "-amos22 +idc_lidc_idri"`. Each fetch is planned at the size its record knows; the
grid's size rule (SchwingNet's grid/size-rule.sh) still reads the exact size from the source before
a byte lands and refuses a fetch that would pass the quota, whatever the plan said.
"""

import argparse
import glob
import json
import os
import re
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import census  # noqa: E402

FORMAT = "spine-datasets/storage 1"
REQUEST_FORMAT = "spine-datasets/storage-request 1"
LAB_ROOT = "/rs/rs_grp_oschome/"
TARGET_BYTES = 20 * 10 ** 12
HOME_QUOTA_BYTES = 4 * 10 ** 12
ACTION = re.compile(r"^(?:([+-])([a-z0-9_]+)|([a-z0-9_]+)@(lab|home))$")
ON_GRID = ("held", "fetched")


# Reading the records.

def load_records(folder):
    records = {}
    for path in sorted(glob.glob(os.path.join(folder, "*.json"))):
        with open(path, encoding="utf-8") as handle:
            record = json.load(handle)
        records[record["id"]] = record
    return records


def location_of(record):
    """Where a held set lives: the lab volume, the owner's home, or nowhere yet."""
    path = record.get("grid_path")
    if record.get("status") not in ON_GRID or not isinstance(path, str) or not path:
        return "none"
    return "lab" if path.startswith(LAB_ROOT) else "home"


def size_of(record):
    """(bytes, known): what a freeze measured is known; a stated size in counts is not."""
    measured = census.grid_bytes(record)
    if measured is not None:
        return measured, True
    stated = census.counts_of(record)[0]["bytes"]
    return stated, False


def can_rebuild(record):
    steps = record.get("how_to_get")
    return bool(steps) and isinstance(steps, list)


def overlap_of(table, ident):
    found = []
    for pair in (table or {}).get("pairs", []):
        if ident not in (pair["a"], pair["b"]):
            continue
        other = pair["b"] if pair["a"] == ident else pair["a"]
        found.append({"with": other, "patients": pair["patients"], "series": pair["series"],
                      "same_bytes": pair["same_bytes"]})
    return found


def reach_of(record, location):
    """held once on the grid, whatever the record's reach says of how it was got; else the
    record's reach, with get counted as fetchable only while nothing waits on the owner."""
    if location != "none":
        return "held"
    return record.get("reach", "")


def fetchable(record):
    return record.get("reach") == "get" or record.get("status") == "granted"


def set_entry(record, table):
    size, known = size_of(record)
    location = location_of(record)
    return {
        "id": record["id"],
        "name": record.get("name", ""),
        "group": record.get("group", ""),
        "reach": reach_of(record, location),
        "fetchable": location == "none" and fetchable(record),
        "status": record.get("status", ""),
        "location": location,
        "bytes": size,
        "bytes_known": known,
        "licence": census.licence_kind(record.get("licence")),
        "rebuild": can_rebuild(record),
        "frozen": census.tree_of(record) is not None,
        "overlap": overlap_of(table, record["id"]),
    }


# The feed.

def read_json(path):
    if not path or not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def build_plan(records, volume, table):
    sets = [set_entry(record, table) for _, record in sorted(records.items())]
    held_lab = sum(entry["bytes"] or 0 for entry in sets if entry["location"] == "lab")
    used = volume.get("used_bytes")
    home_used = volume.get("home_used_bytes")
    return {
        "format": FORMAT,
        "built_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "target_bytes": volume.get("target_bytes", TARGET_BYTES),
        "volume": {
            "quota_bytes": volume.get("quota_bytes"),
            "used_bytes": used,
            "read_at": volume.get("read_at"),
            "datasets_bytes": held_lab,
            "other_bytes": None if used is None else max(0, used - held_lab),
        },
        "home": {
            "quota_bytes": volume.get("home_quota_bytes", HOME_QUOTA_BYTES),
            "used_bytes": home_used,
            "read_at": volume.get("home_read_at"),
        },
        "sets": sets,
    }


# A trial combination.

def parse_selection(text):
    """[(kind, id, place)] for each action, kind one of retire, fetch, move; ValueError on a word
    that is no action."""
    actions = []
    for word in re.split(r"[\s,]+", text.strip()):
        if not word:
            continue
        found = ACTION.match(word)
        if not found:
            raise ValueError("not an action: %r (use -id, +id, id@home or id@lab)" % word)
        if found.group(1) == "-":
            actions.append(("retire", found.group(2), None))
        elif found.group(1) == "+":
            actions.append(("fetch", found.group(2), "lab"))
        else:
            actions.append(("move", found.group(3), found.group(4)))
    return actions


def action_problems(kind, entry, place):
    if kind == "retire":
        if entry["location"] == "none":
            return ["%s is not on the grid, so there is nothing to retire" % entry["id"]]
        problems = []
        if not entry["frozen"]:
            problems.append("%s is not frozen, so a rebuild could not be proved identical" % entry["id"])
        if not entry["rebuild"]:
            problems.append("%s has no recipe to rebuild it from" % entry["id"])
        return problems
    if kind == "fetch":
        if entry["location"] != "none":
            return ["%s is already on the grid" % entry["id"]]
        if not entry["fetchable"]:
            return ["%s is %s (%s), not open to fetch; its task says what it waits on" % (
                entry["id"], entry["reach"], entry["status"])]
        if entry["bytes"] is None:
            return ["%s has no size in its record, so it cannot be planned" % entry["id"]]
        return []
    if entry["location"] == "none":
        return ["%s is not on the grid, so it cannot be moved" % entry["id"]]
    if entry["location"] == place:
        return ["%s is already in the %s" % (entry["id"], place)]
    if entry["bytes"] is None:
        return ["%s has no measured size, so its move cannot be planned" % entry["id"]]
    return []


def deltas(kind, entry, place):
    """(lab change, home change) in bytes."""
    size = entry["bytes"] or 0
    if kind == "retire":
        return (-size, 0) if entry["location"] == "lab" else (0, -size)
    if kind == "fetch":
        return size, 0
    return (size, -size) if place == "lab" else (-size, size)


def check(plan, actions):
    """The totals after the actions and every reason they could not go ahead."""
    by_id = {entry["id"]: entry for entry in plan["sets"]}
    problems, seen = [], set()
    lab_change = home_change = 0
    for kind, ident, place in actions:
        if ident in seen:
            problems.append("%s is named twice" % ident)
            continue
        seen.add(ident)
        entry = by_id.get(ident)
        if entry is None:
            problems.append("%s has no record" % ident)
            continue
        found = action_problems(kind, entry, place)
        problems.extend(found)
        if not found:
            lab, home = deltas(kind, entry, place)
            lab_change += lab
            home_change += home
    volume, home = plan["volume"], plan["home"]
    lab_after = None if volume["used_bytes"] is None else volume["used_bytes"] + lab_change
    home_after = None if home["used_bytes"] is None else home["used_bytes"] + home_change
    if lab_after is None:
        problems.append("the lab volume's use has not been read (storage/VOLUME.json)")
    else:
        cap = min(plan["target_bytes"], volume["quota_bytes"] or plan["target_bytes"])
        if lab_after > cap:
            problems.append("the lab volume would hold %s, over its cap of %s" % (tb(lab_after), tb(cap)))
    if home_change > 0 and home_after is None:
        problems.append("the home's use has not been read, so nothing can move or land there yet")
    elif home_after is not None and home_after > home["quota_bytes"]:
        problems.append("the home would hold %s, over its %s" % (tb(home_after), tb(home["quota_bytes"])))
    return {"lab_after": lab_after, "home_after": home_after, "lab_change": lab_change,
            "home_change": home_change, "problems": problems}


def tb(value):
    return "%.2f TB" % (value / 10 ** 12)


def request_of(plan, actions, result, selection):
    by_id = {entry["id"]: entry for entry in plan["sets"]}
    return {
        "format": REQUEST_FORMAT,
        "made_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "selection": selection,
        "actions": [{"kind": kind, "id": ident, "place": place, "bytes": by_id[ident]["bytes"],
                     "bytes_known": by_id[ident]["bytes_known"]} for kind, ident, place in actions],
        "lab_after": result["lab_after"],
        "home_after": result["home_after"],
    }


def summary(plan, actions, result):
    """The request's text: every set by name, what happens to it and the totals after."""
    by_id = {entry["id"]: entry for entry in plan["sets"]}
    words = {"retire": "retire (images deleted; record, freeze and recipe kept)",
             "fetch": "fetch to the lab volume", "move": "move to the %s"}
    lines = []
    for kind, ident, place in actions:
        entry = by_id[ident]
        what = words[kind] % place if kind == "move" else words[kind]
        size = "size unknown" if entry["bytes"] is None else tb(entry["bytes"])
        if not entry["bytes_known"] and entry["bytes"] is not None:
            size += " stated, exact size read before it lands"
        lines.append("- %s (%s): %s, %s" % (ident, entry["name"], what, size))
    lines.append("")
    lines.append("Lab volume after: %s of a %s cap." % (
        tb(result["lab_after"]), tb(min(plan["target_bytes"], plan["volume"]["quota_bytes"] or plan["target_bytes"]))))
    if result["home_after"] is not None:
        lines.append("Home after: %s of %s." % (tb(result["home_after"]), tb(plan["home"]["quota_bytes"])))
    return "\n".join(lines) + "\n"


# Commands.

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--records", default="datasets")
    parser.add_argument("--volume", default="storage/VOLUME.json")
    parser.add_argument("--overlap", default="lineage/OVERLAP.json")
    sub = parser.add_subparsers(dest="command", required=True)
    plan_cmd = sub.add_parser("plan", help="write the feed")
    plan_cmd.add_argument("--out", default="storage/PLAN.json")
    plan_cmd.add_argument("--check", action="store_true", help="fail when the feed on disk is stale")
    check_cmd = sub.add_parser("check", help="test a selection against both caps")
    check_cmd.add_argument("selection")
    request_cmd = sub.add_parser("request", help="write a request file and its text for a selection")
    request_cmd.add_argument("selection")
    request_cmd.add_argument("--out", required=True)
    request_cmd.add_argument("--text", required=True)
    args = parser.parse_args(argv)

    plan = build_plan(load_records(args.records), read_json(args.volume) or {}, read_json(args.overlap))
    if args.command == "plan":
        return write_plan(plan, args.out, args.check)
    try:
        actions = parse_selection(args.selection)
    except ValueError as error:
        print(error, file=sys.stderr)
        return 2
    if not actions:
        print("no action named", file=sys.stderr)
        return 2
    result = check(plan, actions)
    for problem in result["problems"]:
        print(problem, file=sys.stderr)
    if result["problems"]:
        return 1
    print(summary(plan, actions, result), end="")
    if args.command == "request":
        os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as handle:
            json.dump(request_of(plan, actions, result, args.selection), handle, indent=1, sort_keys=True)
            handle.write("\n")
        with open(args.text, "w", encoding="utf-8") as handle:
            handle.write(summary(plan, actions, result))
    return 0


def comparable(plan):
    return {key: value for key, value in plan.items() if key != "built_at"}


def write_plan(plan, out, check_only):
    if check_only:
        on_disk = read_json(out)
        if on_disk is None or comparable(on_disk) != comparable(plan):
            print("%s is stale: run python3 tools/storage.py plan" % out, file=sys.stderr)
            return 1
        return 0
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    with open(out, "w", encoding="utf-8") as handle:
        json.dump(plan, handle, indent=1, sort_keys=True)
        handle.write("\n")
    print("wrote %s: %d sets" % (out, len(plan["sets"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
