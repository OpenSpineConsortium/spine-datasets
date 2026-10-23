"""The census: every dataset counted from its one record, folded in as records come and change.

Source: the thread "Dataset census and roadmap", 2026-10-23, the owner's ask of that day for an
automatic census tracker that never passes over a dataset more than once: one formatted metadata
file per dataset, and a script that keeps the census current and lets it accumulate as datasets,
and so their metadata files, are added.

The metadata file is the record, datasets/<id>.json (datasets/README.md). A dataset's files are
read once, when they land: the promoter checks every byte and checksum (tools/promote.py), and
what that pass, or the owner's own chain, measured is written into the record. This script never
opens a dataset. It reads the records alone, and it folds into the last census only the records
that are new or whose content changed since, by the sha256 of the record; a record that did not
change is carried over as it was, unless the rules that derive a row changed since (this file or
tools/pipeline.py, whose stage the census shows), when every row is derived afresh. Each record
keeps the date the census first saw it (on the census's first run, the date of its oldest history
step, when the work on it began; a record removed and written again keeps its first date) and the
date its content last changed, and the census keeps a dated log of what moved: a record added, a
status or a count changed, a record removed, the rules changed.

From the records it derives, never stores twice: the stage (tools/pipeline.py's, so the board and
the census agree), the counts in standard keys (subjects, still X-ray images, X-ray videos and
sweeps, the frames inside those, CT volumes, bytes, read from the record's counts under the names
the records use), the licence's kind (open, restricted, unknown), and for a record with a pairing
block, a real X-ray set with the subject's CT, its tier:
A on the grid, B open or granted, C behind a letter, an agreement or the owner's hand, D refused,
embargoed or never released, E a real pair of something other than the spine, whose shipped pose
or CT is the registration code's truth. A pair moves from tier to tier by itself as its record's
status moves.

It writes three files: census.json, the ledger the next run folds into; CENSUS.md, which GitHub
renders; and census.html, the page, with the totals, the paired breakout, every dataset, what the
records still lack and the log. The census workflow writes them to the branch census
(.github/workflows/census.yml) and the docs site serves census.html.

    python3 tools/census.py render --out DIR [--previous census.json] [--issues issues.json]
                                   [--repo OWNER/NAME] [--date YYYY-MM-DD]
    python3 tools/census.py same OLD NEW
    python3 tools/census.py check

`same` exits 0 when two census.json files differ in nothing but the day they were written, so a
quiet day pushes nothing, while a change to the rules or the repository's name, which census.json
records, puts the new pages on the branch. `check` also refuses two records with one id and a
record whose id is not its file's name, since one dataset is one record. The standard library
alone; no token, no network: the workflow fetches the issues with gh and the last census from the
branch, and hands both in as files.
"""

import argparse
import hashlib
import html
import json
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import pipeline  # noqa: E402

ROOT = pipeline.ROOT
DEFAULT_REPO = pipeline.DEFAULT_REPO

# The rules a row is derived by are the code of this file and of tools/pipeline.py, whose stage
# the census shows: a change to either derives every row afresh on the next run, so no carried
# row keeps a stage or a count the old code gave it.
RULES_FILES = (Path(__file__).resolve(), Path(pipeline.__file__).resolve())

KINDS = {
    "fluoro": "Fluoroscopy",
    "video": "Fluoroscopy video",
    "projections": "CBCT projections",
    "films": "Radiographs",
    "ct": "CT",
    "future": "Veterinary and later",
}

# The standard count keys, and the names the records already use for each, first match winning,
# read by the kind of set. A still image counts once as an X-ray image. A run, clip, recording,
# sweep or cine series counts once as a video whatever its frames, and in a video or projection
# set the frames inside the videos are counted apart, as run_frames: COBRA2026's 375,618
# projections are 692 sweeps, not 375,618 images. A CT set's "images" are slices and its "frames"
# are not X-rays, so for CT every X-ray count is read from its standard key alone.
SUBJECT_KEYS = ("subjects", "patients", "people", "men", "cases", "specimens")
STILL_KEYS = ("xray_images", "radiographs", "films", "spot_frames", "frames", "projections", "images")
RUN_KEYS = ("videos", "clips", "recordings", "sequences", "runs", "sweeps", "series")
RUN_FRAME_KEYS = ("run_frames", "frames", "projections", "images")
CT_KEYS = ("ct_volumes", "cts", "ct_scans", "cbct_volumes", "volumes")
RUN_GROUPS = ("video", "projections")
BYTE_KEYS = (("bytes", 1), ("zip_bytes", 1), ("size_tb", 10 ** 12), ("size_gb", 10 ** 9),
             ("gigabytes", 10 ** 9), ("size_mb", 10 ** 6))
STANDARD_KEYS = ("subjects", "xray_images", "videos", "run_frames", "ct_volumes", "bytes")
BYTES_IN_RESULT = re.compile(r"(\d[\d,]*) bytes")

RESTRICTED = re.compile(
    r"non-?commercial|\bNC\b|\bND\b|no-?deriv|research[- ]only|data use agreement|\bDUA\b|"
    r"agreement|credential|restricted|proprietary|in copyright|not released|request", re.IGNORECASE)
OPEN = re.compile(r"\bCC[ -]?BY\b|\bCC0\b|creative commons attribution|public domain|open access|\bMIT\b|"
                  r"apache|\bODC", re.IGNORECASE)
# Only a web address becomes a link on the page, never a javascript: or data: one a record holds.
WEB_ADDRESS = re.compile(r"https?://", re.IGNORECASE)

PAIRING_TEXT = ("region", "xray", "ct", "subjects", "pose", "masks", "annotate")
PAIRING_KEYS = PAIRING_TEXT + ("spine", "pair_key", "priority")

TIERS = (
    ("A", "On the grid", "real spine X-rays with the same subject's CT, held now: the annotation starts here"),
    ("B", "Open or granted, not yet on the grid", "a download or a fetch away"),
    ("C", "Behind a letter, an agreement or the owner's hand", "asked, or still to ask"),
    ("D", "Refused, embargoed or never released", "kept so nobody asks twice"),
    ("E", "Real pairs of something other than the spine",
     "frames shipped with a CT or an exact pose: the registration code's truth, not spine labels"),
)
TIER_TITLES = {key: title for key, title, _ in TIERS}

# What a change event names when it moves; other edits (a next step, an obstacle) refresh the row
# without an event.
TRACKED = ("status", "stage", "route", "licence", "grid_path", "subjects", "xray_images", "videos",
           "run_frames", "ct_volumes", "bytes", "grid_bytes", "paired", "tier")


# Reading one record

def digest_of(record):
    """The sha256 of the record's content, so a reformatted file is the same record."""
    text = json.dumps(record, sort_keys=True, ensure_ascii=True, separators=(",", ":"))
    return hashlib.sha256(text.encode("ascii")).hexdigest()


def rules_of(files=RULES_FILES):
    """A fingerprint of the code that derives a row, so a change to it derives every row afresh."""
    digest = hashlib.sha256()
    for path in files:
        digest.update(Path(path).read_bytes())
    return digest.hexdigest()[:16]


def text_of(record, field, default=""):
    """A text field as text: a null, or a number where text belongs, reads as the default, so one
    odd field never stops the census; `check` names it."""
    value = record.get(field)
    return value if isinstance(value, str) else default


def number(value):
    """A count as a number, or None for anything that is not one (a bool, a note, a range)."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return value


def first_number(counts, keys):
    for key in keys:
        if key in counts and number(counts[key]) is not None:
            return number(counts[key]), key
    return None, None


def count_keys(group):
    """The names each standard count is read under, for a record of this group."""
    if group == "ct":
        return {"subjects": SUBJECT_KEYS, "xray_images": ("xray_images",), "videos": ("videos",),
                "run_frames": ("run_frames",), "ct_volumes": CT_KEYS}
    if group in RUN_GROUPS:
        return {"subjects": SUBJECT_KEYS, "xray_images": ("xray_images", "radiographs", "films", "spot_frames"),
                "videos": RUN_KEYS, "run_frames": RUN_FRAME_KEYS, "ct_volumes": CT_KEYS}
    return {"subjects": SUBJECT_KEYS, "xray_images": STILL_KEYS, "videos": RUN_KEYS,
            "run_frames": ("run_frames",), "ct_volumes": CT_KEYS}


def counts_of(record):
    """The standard counts, read under the names the records use, and the keys left unread."""
    counts = record.get("counts") or {}
    if not isinstance(counts, dict):
        return {key: None for key in STANDARD_KEYS}, ["counts"]
    found, used = {}, set()
    for name, keys in count_keys(record.get("group")).items():
        found[name], key = first_number(counts, keys)
        used.add(key)
    found["bytes"] = None
    for key, scale in BYTE_KEYS:
        if key in counts and number(counts[key]) is not None:
            # round, not int: 33.8 GB times 10**9 is 33799999999.999996 in floating point.
            found["bytes"] = round(number(counts[key]) * scale)
            used.add(key)
            break
    unread = sorted(key for key in counts if key not in used)
    return found, unread


def licence_kind(text):
    """Open, restricted or unknown. A restriction counts wherever the licence line notes it; an
    open licence counts only in the line's own words, outside its notes in parentheses, since a
    note may speak of another record's licence ("the held record of the same authors is CC BY")."""
    text = text if isinstance(text, str) else ""
    if RESTRICTED.search(text):
        return "restricted"
    if OPEN.search(re.sub(r"\([^)]*\)", " ", text)):
        return "open"
    return "unknown"


def grid_bytes(record):
    """What the landing pass measured on the grid: the record's measured bytes, else the
    promoter's result line."""
    measured = record.get("measured") or {}
    if isinstance(measured, dict) and number(measured.get("bytes")) is not None:
        return round(measured["bytes"])
    found = BYTES_IN_RESULT.search(text_of(record, "result"))
    if found and record.get("status") in ("fetched", "held", "fetching"):
        return int(found.group(1).replace(",", ""))
    return None


def tier_of(stage, pairing):
    if not pairing.get("spine"):
        return "E"
    if stage in ("on-grid", "held"):
        return "A"
    if stage in ("downloadable", "granted", "fetching"):
        return "B"
    if stage in ("refused", "later"):
        return "D"
    return "C"


def row_of(record):
    """Everything the census shows of one record, derived from the record alone."""
    stage = pipeline.stage_of(record)
    counts, unread = counts_of(record)
    entries = [entry for entry in record.get("history") or [] if isinstance(entry, dict)]
    history = sorted(entries, key=lambda entry: str(entry.get("date") or ""))
    pairing = record.get("pairing") if isinstance(record.get("pairing"), dict) else None
    group = text_of(record, "group")
    return {
        "id": text_of(record, "id"),
        "name": text_of(record, "name") or text_of(record, "id"),
        "group": group,
        "kind": KINDS.get(group, group),
        "route": text_of(record, "route"),
        "status": text_of(record, "status"),
        "stage": stage,
        "licence": text_of(record, "licence"),
        "licence_kind": licence_kind(record.get("licence")),
        "link": text_of(record, "link"),
        "what": text_of(record, "what"),
        "level_truth": text_of(record, "level_truth"),
        "grid_path": text_of(record, "grid_path", None),
        "on_grid": stage in ("on-grid", "held"),
        "grid_bytes": grid_bytes(record),
        **counts,
        "unread_counts": unread,
        "next": text_of(record, "next"),
        "since": str(history[0].get("date") or "") if history else "",
        "last_step": {"date": history[-1].get("date", ""), "step": history[-1].get("step", "")} if history else None,
        "paired": pairing is not None,
        "tier": tier_of(stage, pairing) if pairing else None,
        "pairing": pairing,
    }


# Folding the records into the last census

def shared_ids(records):
    """The ids two or more records carry; the census keys each dataset by its id."""
    tally = Counter(record.get("id", "") for record in records)
    return sorted(str(ident) for ident, count in tally.items() if count > 1)


def ledger_entry(ledger, ident):
    """The last census's entry for one record, or None where it holds none that reads."""
    entry = ledger.get(ident)
    return entry if isinstance(entry, dict) and isinstance(entry.get("row"), dict) else None


def fold(previous, records, today, rules=None):
    """The new census: the last one's rows carried for every record whose content did not change,
    rows derived afresh for the rest, and the log grown by what moved. Every row is derived afresh
    when the rules changed since; a row whose record did not change keeps its date of last change
    then, and the log says the rules changed, not that the record did."""
    rules = rules_of() if rules is None else rules
    twice = shared_ids(records)
    if twice:
        raise ValueError("one id in two or more records: " + ", ".join(twice))
    # Anything but a census, an error page a fetch wrote say, starts the census afresh.
    previous = previous if isinstance(previous, dict) and isinstance(previous.get("records"), dict) else None
    starting = previous is None
    rules_changed = not starting and previous.get("rules") != rules
    ledger = {} if starting else previous["records"]
    seen = {} if starting else dict(previous.get("seen") or {})
    events = [] if starting else list(previous.get("events") or [])
    folded = {}
    tally = {"new": 0, "changed": 0, "rederived": 0, "carried": 0, "removed": 0}
    for record in records:
        ident = record.get("id", "")
        digest = digest_of(record)
        before = ledger_entry(ledger, ident)
        unchanged = before is not None and before.get("digest") == digest
        if unchanged and not rules_changed:
            folded[ident] = before
            seen.setdefault(ident, before.get("first_seen", today))
            tally["carried"] += 1
            continue
        row = row_of(record)
        last_changed = today
        if before is None:
            # A record removed and written again keeps the date the census first saw it.
            first_seen = seen.get(ident) or ((row["since"] or today) if starting else today)
            tally["new"] += 1
            if not starting:
                events.append({"date": today, "id": ident, "kind": "added", "changes": {}})
        elif unchanged:
            first_seen = before.get("first_seen", today)
            last_changed = before.get("last_changed", today)
            tally["rederived"] += 1
        else:
            first_seen = before.get("first_seen", today)
            tally["changed"] += 1
            moved = {field: [before["row"].get(field), row.get(field)] for field in TRACKED
                     if before["row"].get(field) != row.get(field)}
            if moved:
                events.append({"date": today, "id": ident, "kind": "changed", "changes": moved})
        seen[ident] = first_seen
        folded[ident] = {"digest": digest, "first_seen": first_seen, "last_changed": last_changed, "row": row}
    for ident in sorted(set(ledger) - set(folded)):
        entry = ledger[ident] if isinstance(ledger[ident], dict) else {}
        seen.setdefault(ident, entry.get("first_seen", today))
        tally["removed"] += 1
        events.append({"date": today, "id": ident, "kind": "removed", "changes": {}})
    if starting:
        events.append({"date": today, "id": "", "kind": "started", "changes": {"records": [None, len(folded)]}})
    elif rules_changed:
        events.append({"date": today, "id": "", "kind": "rules", "changes": {"rules": [previous.get("rules"), rules]}})
    return {"rules": rules, "records": folded, "events": events, "seen": dict(sorted(seen.items()))}, tally


# What the census adds up

def rows_in_order(census):
    return sorted((entry["row"] for entry in census["records"].values()), key=pipeline.group_key)


def summed(rows, field):
    values = [row[field] for row in rows if row.get(field) is not None]
    return {"sum": sum(values), "counted": len(values), "of": len(rows)}


def size_on_grid(rows):
    values = [row["grid_bytes"] if row["grid_bytes"] is not None else row["bytes"] for row in rows]
    known = [value for value in values if value is not None]
    return {"sum": sum(known), "counted": len(known), "of": len(rows),
            "measured": sum(1 for row in rows if row["grid_bytes"] is not None)}


def totals(rows):
    held = [row for row in rows if row["on_grid"]]
    pairs = [row for row in rows if row["paired"]]
    spine_held = [row for row in pairs if row["tier"] == "A"]
    by_stage = {key: sum(1 for row in rows if row["stage"] == key) for key, _, _ in pipeline.STAGES}
    by_kind = {group: sum(1 for row in rows if row["group"] == group) for group in KINDS}
    return {
        "datasets": len(rows),
        "by_stage": by_stage,
        "by_kind": by_kind,
        "on_grid": len(held),
        "on_grid_size": size_on_grid(held),
        "on_grid_subjects": summed(held, "subjects"),
        "on_grid_xray_images": summed(held, "xray_images"),
        "on_grid_videos": summed(held, "videos"),
        "on_grid_run_frames": summed(held, "run_frames"),
        "on_grid_ct_volumes": summed(held, "ct_volumes"),
        "paired": {key: sum(1 for row in pairs if row["tier"] == key) for key, _, _ in TIERS},
        "paired_spine_subjects_on_grid": summed(spine_held, "subjects"),
    }


def gaps(rows):
    """What the records still lack, one line each: each is filled once, in the record."""
    found = []
    for row in rows:
        if row["on_grid"] and row["grid_bytes"] is None and row["bytes"] is None:
            found.append((row["id"], "on the grid with no size: write the landing pass's bytes into measured"))
        if all(row[key] is None for key in ("subjects", "xray_images", "videos", "run_frames", "ct_volumes")):
            found.append((row["id"], "no count the census can read: add subjects, xray_images, videos, run_frames"
                                     " or ct_volumes to counts"))
        if "to confirm" in row["licence"] or not row["licence"].strip():
            found.append((row["id"], "the licence is still to confirm on the source's page"))
        if row["paired"] and not str(row["pairing"].get("pair_key") or "").strip():
            found.append((row["id"], "a pair with no pair_key: how each X-ray is matched to its CT is not written"))
    return found


def tasks_of(issues, records):
    """The task of each record, and the open tasks whose record is not written yet."""
    tasks = pipeline.tasks_by_id(issues)
    known = {record.get("id") for record in records}
    pending = []
    for issue in issues:
        if "pull_request" in issue or issue.get("state") != "open":
            continue
        found = pipeline.RECORD_LINE.search(issue.get("body") or "")
        if not found or found.group(1) in known:
            continue
        labels = [label["name"] if isinstance(label, dict) else label for label in issue.get("labels", [])]
        pending.append({"number": issue["number"], "title": issue.get("title", ""), "url": issue.get("html_url", ""),
                        "id": found.group(1), "paired": "paired" in labels})
    return ({ident: task["number"] for ident, task in tasks.items() if ident in known},
            sorted(pending, key=lambda t: t["number"]))


def census_file(census, tasks, pending, generated, repo=DEFAULT_REPO):
    """The ledger as written. It names the repository, which the pages link to, so a rename
    changes the file and the pages are written again."""
    rows = rows_in_order(census)
    return {
        "rules": census["rules"],
        "repo": repo,
        "generated": generated,
        "totals": totals(rows),
        "tasks": dict(sorted(tasks.items())),
        "pending_tasks": pending,
        "records": dict(sorted(census["records"].items())),
        "seen": census["seen"],
        "events": census["events"],
    }


def same(old, new):
    """Two census files that differ in nothing but the day they were written. Everything the
    pages show comes from the file, and the code that draws them is part of the rules the file
    records, so two files alike draw alike pages."""
    strip = lambda data: {key: value for key, value in data.items() if key != "generated"}  # noqa: E731
    return strip(old) == strip(new)


# Writing it out

def amount(value):
    if value is None:
        return ""
    return f"{int(value):,}" if float(value).is_integer() else f"{value:,}"


def size_text(value):
    if value is None:
        return ""
    for unit, scale in (("TB", 10 ** 12), ("GB", 10 ** 9), ("MB", 10 ** 6), ("kB", 10 ** 3)):
        if value >= scale:
            return f"{value / scale:,.1f} {unit}"
    return f"{value} B"


def counted(total, unit=amount):
    text = unit(total["sum"])
    if total["counted"] < total["of"]:
        text += f" ({total['counted']} of {total['of']} sets counted)"
    return text


def task_link(ident, tasks, repo):
    number_ = tasks.get(ident)
    return (f"#{number_}", f"https://github.com/{repo}/issues/{number_}") if number_ else ("", "")


def task_markdown(ident, tasks, repo):
    """A link GitHub follows in a file, where a bare #N is plain text."""
    label, url = task_link(ident, tasks, repo)
    return f"[{label}]({url})" if url else ""


def priority_of(row):
    priority = row["pairing"].get("priority")
    return priority if isinstance(priority, int) and not isinstance(priority, bool) else 999


def paired_rows(rows, tier):
    chosen = [row for row in rows if row["tier"] == tier]
    return sorted(chosen, key=lambda row: (priority_of(row), row["name"].lower()))


def events_newest_first(events, limit=200):
    return list(reversed(events))[:limit]


def event_text(event, names):
    kind = event["kind"]
    if kind == "started":
        return f"the census began with {event['changes']['records'][1]} records"
    if kind == "rules":
        return "the census rules changed; every row was derived afresh"
    name = names.get(event["id"], event["id"])
    if kind == "added":
        return f"{name}: record added"
    if kind == "removed":
        return f"{name}: record removed"
    parts = []
    for field, (old, new) in sorted(event["changes"].items()):
        if field in ("bytes", "grid_bytes"):
            old, new = size_text(old), size_text(new)
        parts.append(f"{field} {old if old not in (None, '') else 'none'} to {new if new not in (None, '') else 'none'}")
    return f"{name}: " + "; ".join(parts)


def md_cell(text):
    return str(text if text is not None else "").replace("|", "/").replace("\n", " ")


def render_markdown(data, repo=DEFAULT_REPO):
    rows = sorted((entry["row"] for entry in data["records"].values()), key=pipeline.group_key)
    totals_ = data["totals"]
    tasks = data["tasks"]
    names = {row["id"]: row["name"] for row in rows}
    lines = [
        "# Census: every dataset, counted from its record",
        "",
        f"Written by tools/census.py on {data['generated']} from the {len(rows)} records under datasets/ of",
        f"https://github.com/{repo}; nobody edits it by hand. Each dataset is one record; the census reads",
        "the records alone, never a dataset's files, and folds in only the records that are new or changed",
        "since the last run. The page with filters is census.html beside this file, served by the docs site.",
        "",
        "## In numbers",
        "",
        "| | |",
        "|---|---|",
        f"| Datasets with a record | {totals_['datasets']} |",
        f"| On the grid (shared tree and the owner's root) | {totals_['on_grid']} |",
        f"| Size on the grid | {counted(totals_['on_grid_size'], size_text)} |",
        f"| Subjects on the grid | {counted(totals_['on_grid_subjects'])} |",
        f"| X-ray images on the grid | {counted(totals_['on_grid_xray_images'])} |",
        f"| X-ray videos and sweeps on the grid | {counted(totals_['on_grid_videos'])} |",
        f"| Frames inside those videos and sweeps | {counted(totals_['on_grid_run_frames'])} |",
        f"| CT volumes on the grid | {counted(totals_['on_grid_ct_volumes'])} |",
        f"| Real spine X-ray and CT pairs on the grid | {totals_['paired']['A']} sets, "
        f"{counted(totals_['paired_spine_subjects_on_grid'])} subjects |",
        "",
        "| Stage | Datasets |",
        "|---|---|",
    ]
    for key, title, _ in pipeline.STAGES:
        lines.append(f"| {title} | {totals_['by_stage'].get(key, 0)} |")
    lines += ["", "## Paired CT and X-ray", "",
              "Every record with a pairing block: real X-ray frames, films or projections with the same subject's",
              "CT or CBCT. The tier follows the record's status by itself.", ""]
    for key, title, blurb in TIERS:
        chosen = paired_rows(rows, key)
        lines += [f"### {key}. {title} ({len(chosen)})", "", f"{blurb[0].upper()}{blurb[1:]}.", ""]
        if not chosen:
            lines += ["None yet.", ""]
            continue
        lines += ["| Set | Region | X-rays | CT | Subjects | Pose | Masks shipped | What annotation adds | Pair key | Task |",
                  "|---|---|---|---|---|---|---|---|---|---|"]
        for row in chosen:
            pairing = row["pairing"]
            label = task_markdown(row["id"], tasks, repo)
            lines.append("| " + " | ".join(md_cell(value) for value in (
                row["name"], pairing.get("region"), pairing.get("xray"), pairing.get("ct"), pairing.get("subjects"),
                pairing.get("pose"), pairing.get("masks"), pairing.get("annotate"),
                pairing.get("pair_key") or "not written", label)) + " |")
        lines.append("")
    pending = [task for task in data["pending_tasks"] if task["paired"]]
    if pending:
        lines += ["### Pairs asked for, no record yet", ""]
        lines += [f"- [#{task['number']}]({task['url']}) {md_cell(task['title'])}" for task in pending]
        lines.append("")
    lines += ["## Every dataset", "",
              "| Dataset | Kind | Stage | Licence | Subjects | X-ray images | Videos and sweeps | Their frames "
              "| CT volumes | Size | Task |",
              "|---|---|---|---|---|---|---|---|---|---|---|"]
    for row in rows:
        label = task_markdown(row["id"], tasks, repo)
        size = row["grid_bytes"] if row["grid_bytes"] is not None else row["bytes"]
        lines.append("| " + " | ".join(md_cell(value) for value in (
            row["name"], row["kind"], pipeline.STAGE_TITLES.get(row["stage"], row["stage"]), row["licence_kind"],
            amount(row["subjects"]), amount(row["xray_images"]), amount(row["videos"]), amount(row["run_frames"]),
            amount(row["ct_volumes"]), size_text(size), label)) + " |")
    others = [task for task in data["pending_tasks"] if not task["paired"]]
    if others:
        lines += ["", "Tasks whose record is not written yet:", ""]
        lines += [f"- [#{task['number']}]({task['url']}) {md_cell(task['title'])}" for task in others]
    lines += ["", "## What the records still lack", ""]
    found = gaps(rows)
    lines += [f"- {md_cell(names.get(ident, ident))}: {text}" for ident, text in found] or ["Nothing."]
    lines += ["", "## Changes, newest first", ""]
    lines += [f"- {event['date']} {md_cell(event_text(event, names))}" for event in events_newest_first(data["events"])]
    return "\n".join(lines).rstrip() + "\n"


HTML_STYLE = """<style>
/* Layout: a figures strip, then the paired breakout by tier, every dataset with filters, the gaps
   and the log; one column, tables scroll inside their own frames. Tokens as the pipeline board's. */
:root { --bg: #f6f4ef; --fg: #1f2328; --muted: #6b665c; --card: #ffffff; --line: #d9d4c7; --accent: #8a4b12;
  --ok: #2d6a4f; --warn: #b7791f; --bad: #a23b3b; --info: #2f5d8a; --other: #6a5a8c; --chip: #efebe1; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --bg: #1c1b18; --fg: #e8e4da; --muted: #a39d90;
  --card: #262420; --line: #3b382f; --accent: #e0a165; --ok: #7bc7a0; --warn: #e3b55a; --bad: #e08484; --info: #8db6e0;
  --other: #b9a8dd; --chip: #302d27; color-scheme: dark; } }
:root[data-theme="dark"] { --bg: #1c1b18; --fg: #e8e4da; --muted: #a39d90; --card: #262420; --line: #3b382f;
  --accent: #e0a165; --ok: #7bc7a0; --warn: #e3b55a; --bad: #e08484; --info: #8db6e0; --other: #b9a8dd; --chip: #302d27;
  color-scheme: dark; }
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--fg); font: 14px/1.5 system-ui, -apple-system, "Segoe UI", sans-serif;
  padding-block: 20px 40px; padding-left: max(16px, env(safe-area-inset-left, 0px));
  padding-right: max(16px, env(safe-area-inset-right, 0px)); }
main { max-width: 1180px; margin: 0 auto; display: grid; gap: 28px; }
h1 { font-size: 22px; margin: 0 0 4px; text-wrap: balance; }
h2 { font-size: 17px; margin: 0 0 6px; text-wrap: balance; }
h3 { font-size: 14px; margin: 0; display: flex; gap: 8px; align-items: baseline; flex-wrap: wrap; }
p { margin: 0; max-width: 72ch; }
.lead, .note { color: var(--muted); }
section { display: grid; gap: 12px; min-width: 0; }
.figures { display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 10px; }
.figure { background: var(--card); border: 1px solid var(--line); border-radius: 8px; padding: 10px 12px; min-width: 0; }
.figure b { display: block; font-size: 22px; font-variant-numeric: tabular-nums; }
.figure span { color: var(--muted); font-size: 12px; }
.stages { display: flex; flex-wrap: wrap; gap: 6px; }
.chip { background: var(--chip); border: 1px solid var(--line); border-radius: 999px; padding: 2px 10px; font-size: 12px;
  font-variant-numeric: tabular-nums; }
.tier { display: grid; gap: 6px; min-width: 0; }
.tier-key { display: inline-grid; place-items: center; width: 22px; height: 22px; border-radius: 5px; color: var(--bg);
  font-weight: 700; font-size: 12px; }
.t-A { background: var(--ok); } .t-B { background: var(--info); } .t-C { background: var(--warn); }
.t-D { background: var(--bad); } .t-E { background: var(--other); }
.frame { overflow-x: auto; border: 1px solid var(--line); border-radius: 8px; background: var(--card); }
table { border-collapse: collapse; width: 100%; font-size: 13px; }
th, td { text-align: left; vertical-align: top; padding: 6px 8px; border-bottom: 1px solid var(--line); }
th { font-size: 11px; text-transform: uppercase; letter-spacing: 0.04em; color: var(--muted); font-weight: 600;
  white-space: nowrap; background: var(--card); }
tr:last-child td { border-bottom: none; }
td.num { text-align: right; font-variant-numeric: tabular-nums; white-space: nowrap; }
td.name { min-width: 180px; font-weight: 600; }
td.wide { min-width: 200px; }
.paired td { min-width: 120px; }
a { color: var(--accent); }
a:focus-visible, select:focus-visible, input:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
.pill { display: inline-block; padding: 0 7px; border-radius: 999px; font-size: 11px; border: 1px solid var(--line);
  white-space: nowrap; }
.k-open { color: var(--ok); } .k-restricted { color: var(--warn); } .k-unknown { color: var(--muted); }
.s-on-grid, .s-held { color: var(--ok); } .s-refused { color: var(--bad); } .s-needs-owner, .s-later { color: var(--warn); }
.filters { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }
.filters select, .filters input { font: inherit; padding: 6px 8px; border: 1px solid var(--line); border-radius: 6px;
  background: var(--card); color: var(--fg); }
.filters input { flex: 1 1 220px; min-width: 0; }
ul.plain { margin: 0; padding-left: 18px; display: grid; gap: 3px; }
.log li { font-variant-numeric: tabular-nums; }
.empty { color: var(--muted); font-style: italic; }
</style>"""

HTML_SCRIPT = """<script>
(function () {
  var rows = Array.prototype.slice.call(document.querySelectorAll('#every tbody tr'));
  var stage = document.getElementById('f-stage'), kind = document.getElementById('f-kind'),
      licence = document.getElementById('f-licence'), query = document.getElementById('f-q'),
      shown = document.getElementById('shown');
  function draw() {
    var q = query.value.toLowerCase(), n = 0;
    rows.forEach(function (row) {
      var ok = (!stage.value || row.dataset.stage === stage.value) && (!kind.value || row.dataset.kind === kind.value)
        && (!licence.value || row.dataset.licence === licence.value) && (!q || row.dataset.text.indexOf(q) >= 0);
      row.hidden = !ok; if (ok) n += 1;
    });
    shown.textContent = n + ' of ' + rows.length + ' shown';
  }
  [stage, kind, licence].forEach(function (el) { el.addEventListener('change', draw); });
  query.addEventListener('input', draw);
  draw();
})();
</script>"""


def esc(text):
    return html.escape(str(text if text is not None else ""))


def link_html(label, url):
    """A link only to a web address; any other address a record holds shows as its label alone."""
    url = url.strip() if isinstance(url, str) else ""
    if not WEB_ADDRESS.match(url):
        return esc(label)
    return f'<a href="{esc(url)}" target="_blank" rel="noopener">{esc(label)}</a>'


def figure_html(value, label):
    return f'<div class="figure"><b>{esc(value)}</b><span>{esc(label)}</span></div>'


def counted_note(total):
    return "" if total["counted"] == total["of"] else f", {total['counted']} of {total['of']} sets counted"


def figures_html(totals_):
    size = totals_["on_grid_size"]
    return "".join((
        figure_html(totals_["datasets"], "datasets with a record"),
        figure_html(totals_["on_grid"], "on the grid"),
        figure_html(size_text(size["sum"]), "on the grid" + counted_note(size)),
        figure_html(amount(totals_["on_grid_subjects"]["sum"]), "subjects on the grid" + counted_note(totals_["on_grid_subjects"])),
        figure_html(amount(totals_["on_grid_xray_images"]["sum"]),
                    "X-ray images on the grid" + counted_note(totals_["on_grid_xray_images"])),
        figure_html(amount(totals_["on_grid_videos"]["sum"]),
                    "X-ray videos and sweeps on the grid" + counted_note(totals_["on_grid_videos"])),
        figure_html(amount(totals_["on_grid_run_frames"]["sum"]),
                    "frames inside those" + counted_note(totals_["on_grid_run_frames"])),
        figure_html(amount(totals_["on_grid_ct_volumes"]["sum"]),
                    "CT volumes on the grid" + counted_note(totals_["on_grid_ct_volumes"])),
        figure_html(totals_["paired"]["A"], "real spine X-ray and CT pairs on the grid"),
    ))


def paired_html(rows, data, repo):
    parts = []
    for key, title, blurb in TIERS:
        chosen = paired_rows(rows, key)
        parts.append(f'<div class="tier"><h3><span class="tier-key t-{key}">{key}</span>{esc(title)}'
                     f' <span class="note">{len(chosen)} sets; {esc(blurb)}</span></h3>')
        if not chosen:
            parts.append('<p class="empty">None yet.</p></div>')
            continue
        body = []
        for row in chosen:
            pairing = row["pairing"]
            label, url = task_link(row["id"], data["tasks"], repo)
            stage = pipeline.STAGE_TITLES.get(row["stage"], row["stage"])
            body.append("<tr>" + "".join((
                f'<td class="name">{link_html(row["name"], row["link"])}</td>',
                f"<td>{esc(pairing.get('region'))}</td>", f"<td>{esc(pairing.get('xray'))}</td>",
                f"<td>{esc(pairing.get('ct'))}</td>", f"<td>{esc(pairing.get('subjects'))}</td>",
                f"<td>{esc(pairing.get('pose'))}</td>", f"<td>{esc(pairing.get('masks'))}</td>",
                f'<td class="wide">{esc(pairing.get("annotate"))}</td>',
                f"<td>{esc(pairing.get('pair_key') or 'not written')}</td>",
                f'<td><span class="pill s-{esc(row["stage"])}">{esc(stage)}</span></td>',
                f"<td>{link_html(label, url)}</td>",
            )) + "</tr>")
        parts.append('<div class="frame"><table class="paired"><thead><tr><th>Set</th><th>Region</th><th>X-rays</th>'
                     '<th>CT</th><th>Subjects</th><th>Pose</th><th>Masks shipped</th><th>What annotation adds</th>'
                     '<th>Pair key</th><th>Stage</th><th>Task</th></tr></thead><tbody>' + "".join(body)
                     + "</tbody></table></div></div>")
    pending = [task for task in data["pending_tasks"] if task["paired"]]
    if pending:
        parts.append('<div class="tier"><h3>Pairs asked for, no record yet</h3><ul class="plain">'
                     + "".join(f"<li>{link_html('#%d' % task['number'], task['url'])} {esc(task['title'])}</li>"
                               for task in pending) + "</ul></div>")
    return "".join(parts)


def every_html(rows, data, repo):
    body = []
    for row in rows:
        label, url = task_link(row["id"], data["tasks"], repo)
        size = row["grid_bytes"] if row["grid_bytes"] is not None else row["bytes"]
        text = " ".join((row["name"], row["id"], row["what"], row["licence"], row["level_truth"] or "")).lower()
        stage = pipeline.STAGE_TITLES.get(row["stage"], row["stage"])
        body.append(
            f'<tr data-stage="{esc(row["stage"])}" data-kind="{esc(row["group"])}" data-licence="{esc(row["licence_kind"])}"'
            f' data-text="{esc(text)}">'
            + "".join((
                f'<td class="name">{link_html(row["name"], row["link"])}</td>',
                f"<td>{esc(row['kind'])}</td>",
                f'<td><span class="pill s-{esc(row["stage"])}">{esc(stage)}</span></td>',
                f'<td><span class="k-{esc(row["licence_kind"])}">{esc(row["licence_kind"])}</span></td>',
                f'<td class="num">{esc(amount(row["subjects"]))}</td>',
                f'<td class="num">{esc(amount(row["xray_images"]))}</td>',
                f'<td class="num">{esc(amount(row["videos"]))}</td>',
                f'<td class="num">{esc(amount(row["run_frames"]))}</td>',
                f'<td class="num">{esc(amount(row["ct_volumes"]))}</td>',
                f'<td class="num">{esc(size_text(size))}</td>',
                f'<td class="wide">{esc(row["what"])}</td>',
                f"<td>{link_html(label, url)}</td>",
            )) + "</tr>")
    stages = "".join(f'<option value="{esc(key)}">{esc(title)}</option>' for key, title, _ in pipeline.STAGES)
    kinds = "".join(f'<option value="{esc(group)}">{esc(title)}</option>' for group, title in KINDS.items())
    filters = (f'<div class="filters"><select id="f-stage"><option value="">every stage</option>{stages}</select>'
               f'<select id="f-kind"><option value="">every kind</option>{kinds}</select>'
               '<select id="f-licence"><option value="">every licence</option><option value="open">open</option>'
               '<option value="restricted">restricted</option><option value="unknown">unknown</option></select>'
               '<input id="f-q" type="search" placeholder="search names, contents, licences">'
               '<span class="note" id="shown"></span></div>')
    table = ('<div class="frame"><table id="every"><thead><tr><th>Dataset</th><th>Kind</th><th>Stage</th><th>Licence</th>'
             '<th>Subjects</th><th>X-ray images</th><th>Videos and sweeps</th><th>Their frames</th><th>CT volumes</th>'
             '<th>Size</th><th>What it holds</th>'
             '<th>Task</th>'
             '</tr></thead><tbody>' + "".join(body) + "</tbody></table></div>")
    others = [task for task in data["pending_tasks"] if not task["paired"]]
    extra = ""
    if others:
        extra = ('<p class="note">Tasks whose record is not written yet:</p><ul class="plain">'
                 + "".join(f"<li>{link_html('#%d' % task['number'], task['url'])} {esc(task['title'])}</li>"
                           for task in others) + "</ul>")
    return filters + table + extra


def render_html(data, repo=DEFAULT_REPO):
    rows = sorted((entry["row"] for entry in data["records"].values()), key=pipeline.group_key)
    names = {row["id"]: row["name"] for row in rows}
    totals_ = data["totals"]
    stage_chips = "".join(f'<span class="chip">{esc(title)} {totals_["by_stage"].get(key, 0)}</span>'
                          for key, title, _ in pipeline.STAGES)
    found = gaps(rows)
    gap_list = ("<ul class=\"plain\">" + "".join(f"<li><b>{esc(names.get(ident, ident))}</b>: {esc(text)}</li>"
                                                  for ident, text in found) + "</ul>") if found else '<p class="empty">Nothing.</p>'
    log = "".join(f"<li>{esc(event['date'])} {esc(event_text(event, names))}</li>"
                  for event in events_newest_first(data["events"]))
    return "\n".join((
        "<!doctype html>",
        '<html lang="en">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">',
        "<title>Spine Data Census</title>",
        '<meta name="claude:viewport-fit-sides" content="cover">',
        HTML_STYLE,
        "</head>",
        "<body>",
        "<main>",
        "<header>",
        "<h1>Spine Data Census</h1>",
        f'<p class="lead">Every dataset of <a href="https://github.com/{esc(repo)}">{esc(repo)}</a> counted from its one '
        f"record, written on {esc(data['generated'])}. The census reads the records alone, never a dataset's files, and "
        "folds in only the records that are new or changed since its last run, so adding a dataset is adding its record. "
        "Counts are what each record states or what its landing pass measured; a figure counts only the sets whose "
        "record gives it.</p>",
        "</header>",
        f'<section aria-labelledby="h-figures"><h2 id="h-figures">In numbers</h2><div class="figures">{figures_html(totals_)}</div>'
        f'<div class="stages">{stage_chips}</div></section>',
        '<section aria-labelledby="h-paired"><h2 id="h-paired">Paired CT and X-ray</h2>'
        '<p class="note">Every record with a pairing block: real X-ray frames, films or projections with the same '
        "subject's CT or CBCT. The tier follows the record's status by itself: a set fetched tomorrow moves to A tomorrow. "
        "Tier A is where annotation starts; E holds the pairs whose shipped pose or CT checks the registration code.</p>"
        + paired_html(rows, data, repo) + "</section>",
        f'<section aria-labelledby="h-every"><h2 id="h-every">Every dataset</h2>{every_html(rows, data, repo)}</section>',
        '<section aria-labelledby="h-gaps"><h2 id="h-gaps">What the records still lack</h2>'
        '<p class="note">Each line is filled once, in the record, and leaves this list on the next run.</p>'
        f"{gap_list}</section>",
        f'<section aria-labelledby="h-log"><h2 id="h-log">Changes, newest first</h2><ul class="plain log">{log}</ul></section>',
        "</main>",
        HTML_SCRIPT,
        "</body>",
        "</html>",
    )) + "\n"


# The check

def pairing_problems(ident, pairing):
    if not isinstance(pairing, dict):
        return [f"{ident}: pairing must be an object"]
    found = []
    if not isinstance(pairing.get("spine"), bool):
        found.append(f"{ident}: pairing.spine must be true or false")
    for key in PAIRING_TEXT:
        if not isinstance(pairing.get(key), str) or not pairing[key].strip():
            found.append(f"{ident}: pairing.{key} must be a line of text")
    if "pair_key" in pairing and not isinstance(pairing["pair_key"], str):
        found.append(f"{ident}: pairing.pair_key must be text")
    priority = pairing.get("priority")
    if priority is not None and (isinstance(priority, bool) or not isinstance(priority, int) or priority < 1):
        found.append(f"{ident}: pairing.priority must be a whole number from 1")
    for key in sorted(set(pairing) - set(PAIRING_KEYS)):
        found.append(f"{ident}: pairing.{key} is not one of {PAIRING_KEYS}")
    return found


TEXT_FIELDS = ("name", "group", "what", "licence", "level_truth", "grid_path")


def problems(records):
    """What is wrong with the records' census fields, one line each; empty when nothing."""
    found = []
    for record in records:
        ident = record.get("id", "?")
        for field in TEXT_FIELDS:
            if field in record and record[field] is not None and not isinstance(record[field], str):
                found.append(f"{ident}: {field} must be text")
        if not text_of(record, "licence").strip():
            found.append(f"{ident}: licence must say what the source's terms are, or that they are to confirm")
        if record.get("link") is not None and not isinstance(record["link"], str):
            found.append(f"{ident}: link must be an address or null")
        if "pairing" in record:
            found.extend(pairing_problems(ident, record["pairing"]))
        counts = record.get("counts")
        if counts is not None and not isinstance(counts, dict):
            found.append(f"{ident}: counts must be an object")
        elif counts:
            for key in STANDARD_KEYS:
                if key in counts and number(counts[key]) is None:
                    found.append(f"{ident}: counts.{key} must be a number")
        measured = record.get("measured")
        if measured is not None and not isinstance(measured, dict):
            found.append(f"{ident}: measured must be an object")
    return found


def file_problems(folder=pipeline.RECORDS):
    """Records the census cannot key: a record whose id is not its file's name, and one id in two
    files. One dataset is one record, found by its id, and the census keeps one row per id."""
    found, files_of = [], {}
    for path in sorted(Path(folder).glob("*.json")):
        try:
            record = json.loads(path.read_text(encoding="ascii"))
        except (OSError, ValueError):
            found.append(f"{path.name}: does not read as an ASCII JSON record")
            continue
        ident = record.get("id") if isinstance(record, dict) else None
        if ident != path.stem:
            found.append(f"{path.name}: its id is {ident!r}, not the file's name {path.stem!r}")
        files_of.setdefault(str(ident), []).append(path.name)
    for ident, names in sorted(files_of.items()):
        if len(names) > 1:
            found.append(f"{', '.join(names)}: {len(names)} records with the one id {ident!r}")
    return found


def read_json_file(path):
    """A JSON file, or None where it is missing or unreadable, so a first run starts the census."""
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    render = sub.add_parser("render", help="fold the records into the last census and write the three files")
    render.add_argument("--out", required=True, help="the folder to write into")
    render.add_argument("--previous", help="the last census.json, from the branch census")
    render.add_argument("--issues", help="a JSON list of the repository's issues, from gh api")
    render.add_argument("--repo", default=DEFAULT_REPO)
    render.add_argument("--date", default=date.today().isoformat())
    compare = sub.add_parser("same", help="exit 0 when two census files differ only in their date")
    compare.add_argument("old")
    compare.add_argument("new")
    sub.add_parser("check", help="fail when a record's census fields do not hold together")
    args = parser.parse_args(argv)
    if args.command == "same":
        old, new = read_json_file(args.old), read_json_file(args.new)
        return 0 if old is not None and new is not None and same(old, new) else 1
    records = pipeline.load_records()
    if args.command == "check":
        found = file_problems() + problems(records)
        for line in found:
            print(line)
        print(f"census: {len(records)} records, {len(found)} problems")
        return 1 if found else 0
    previous = read_json_file(args.previous) if args.previous else None
    try:
        census, tally = fold(previous, records, args.date)
    except ValueError as error:
        print(f"census: {error}; nothing written", file=sys.stderr)
        return 1
    issues = json.loads(Path(args.issues).read_text(encoding="utf-8")) if args.issues else []
    tasks, pending = tasks_of(issues, records)
    data = census_file(census, tasks, pending, args.date, args.repo)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "census.json").write_text(json.dumps(data, indent=1, ensure_ascii=True) + "\n", encoding="ascii")
    (out / "CENSUS.md").write_text(render_markdown(data, args.repo), encoding="utf-8")
    # The docs site holds its pages to ASCII; a name with an accent becomes a character reference.
    (out / "census.html").write_bytes(render_html(data, args.repo).encode("ascii", "xmlcharrefreplace"))
    print("census: %d records, %d new, %d changed, %d derived afresh under new rules, %d carried unread, %d removed"
          % (len(records), tally["new"], tally["changed"], tally["rederived"], tally["carried"], tally["removed"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
