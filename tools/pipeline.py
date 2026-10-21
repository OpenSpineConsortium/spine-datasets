"""The pipeline board: where every dataset stands between the registry and the grid.

Source: the SchwingNet thread "SchwingNet video demo plan", 2026-10-21, the owner's ask for "an
interactive scrum board listing all the datasets that have been attained, those which have been
contacted, those that can be downloaded online, and every step along the way".

The records under datasets/ are the one source: each carries its route, its status, a dated
history of the steps taken (researched, asked, granted, fetching, fetched, refused, handed back,
or a note), the obstacles in the way and the next step. The tasks, read from a JSON snapshot of
the repository's issues, add who holds each dataset and the link to its task. From those this
script writes two views of the same board: PIPELINE.md, which GitHub renders, one column per
stage with a card per dataset that opens to its steps; and pipeline.html, the interactive one,
with filters, a search box and cards that open, served by the docs site. The stage is derived
here from the status and the route, never stored twice, so the record and the board cannot
disagree.

    python3 tools/pipeline.py render --out DIR [--issues issues.json] [--repo OWNER/NAME]
    python3 tools/pipeline.py check

The standard library alone; no token, no network: the workflow fetches the issues with gh and
hands the file in.
"""

import argparse
import html
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RECORDS = ROOT / "datasets"
LETTERS = ROOT / "letters"
DEFAULT_REPO = "OpenSpineConsortium/spine-datasets"

ROUTES = ("letter", "form", "account", "agreement", "download", "owner-only")
STATUSES = ("todo", "requested", "granted", "fetching", "fetched", "refused", "needs-owner")
STEPS = ("researched", "asked", "granted", "fetching", "fetched", "refused", "handed-back", "note")
OWNER_ROUTES = ("account", "agreement", "owner-only")
# X-ray sets come before CT everywhere (the owner, 2026-10-21): the columns, the page and the
# fetch order follow this order of groups, and the id inside a group.
GROUP_ORDER = ("fluoro", "video", "projections", "films", "ct", "future")

# The columns, in the order a dataset moves through them; the last three are where it leaves
# the line (handed to the owner, refused, or waiting on time).
STAGES = (
    ("downloadable", "Downloadable now", "open on its page; a grid job fetches it"),
    ("to-ask", "To ask", "a letter, a form or an application not yet sent"),
    ("asked", "Asked, waiting", "sent; the answer is pending"),
    ("granted", "Granted, fetch pending", "the source said yes; the fetch is next"),
    ("fetching", "Fetching", "a grid job is submitted or running"),
    ("on-grid", "On the grid", "under /rs/rs_grp_oschome/shared/datasets/<id>/raw with checksums"),
    ("needs-owner", "Needs the owner", "a signature, a fee, an account or a budget decision"),
    ("refused", "Refused", "the source said no, or the terms cannot be met"),
    ("later", "Later", "embargoed, or nothing can be done yet"),
)
STAGE_TITLES = {key: title for key, title, _ in STAGES}


def load_records(folder=RECORDS):
    """Every record under datasets/, by id, in a stable order."""
    records = []
    for path in sorted(folder.glob("*.json")):
        with path.open(encoding="ascii") as handle:
            records.append(json.load(handle))
    return sorted(records, key=group_key)


def group_key(record):
    """X-ray groups first, CT after them, as the owner ordered on 2026-10-21."""
    group = record.get("group", "")
    rank = GROUP_ORDER.index(group) if group in GROUP_ORDER else len(GROUP_ORDER)
    return (rank, record.get("id", ""))


def letter_ids(folder=LETTERS):
    return {path.stem for path in folder.glob("*.md") if path.stem != "TEMPLATE"}


def stage_of(record):
    """Which column a record stands in, from its status and its route."""
    status = record.get("status", "todo")
    if status in ("requested",):
        return "asked"
    if status in ("granted", "fetching", "refused", "needs-owner"):
        return status
    if status == "fetched":
        return "on-grid"
    if record.get("reach") == "embargoed":
        return "later"
    if record.get("route") == "download":
        return "downloadable"
    return "to-ask"


RECORD_LINE = re.compile(r"Record: datasets/([a-z0-9_]+)\.json")


def tasks_by_id(issues):
    """The task issue of each record, found by the record line in the task's body."""
    tasks = {}
    for issue in issues:
        if "pull_request" in issue:
            continue
        found = RECORD_LINE.search(issue.get("body") or "")
        if not found:
            continue
        labels = [label["name"] if isinstance(label, dict) else label for label in issue.get("labels", [])]
        workers = [name.split(":", 1)[1] for name in labels if name.startswith("worker:")]
        tasks[found.group(1)] = {
            "number": issue["number"],
            "url": issue.get("html_url", ""),
            "state": issue.get("state", "open"),
            "labels": labels,
            "holder": workers[0] if workers and "claimed" in labels else "",
            "given_to": workers[0] if workers and "claimed" not in labels else "",
        }
    return tasks


def holder_text(record, task):
    if task and task.get("holder"):
        return task["holder"]
    if task and task.get("given_to"):
        return "given to " + task["given_to"]
    if record.get("route") in OWNER_ROUTES:
        return "the owner"
    return ""


def card(record, task, letters, repo):
    """Everything a card shows, as plain values."""
    ident = record["id"]
    blob = f"https://github.com/{repo}/blob/main"
    links = [("record", f"{blob}/datasets/{ident}.json")]
    if task:
        links.insert(0, ("task #%d" % task["number"], task["url"]))
    if ident in letters:
        links.append(("letter", f"{blob}/letters/{ident}.md"))
    if record.get("link"):
        links.append(("source", record["link"]))
    history = sorted(record.get("history", []), key=lambda entry: entry.get("date", ""))
    return {
        "id": ident,
        "name": record.get("name", ident),
        "group": record.get("group", ""),
        "route": record.get("route", ""),
        "status": record.get("status", ""),
        "stage": stage_of(record),
        "holder": holder_text(record, task),
        "task_state": task["state"] if task else "",
        "what": record.get("what", ""),
        "licence": record.get("licence", ""),
        "next": record.get("next", ""),
        "obstacles": list(record.get("obstacles", [])),
        "history": history,
        "last": history[-1] if history else None,
        "links": links,
    }


def cards(records, issues, repo=DEFAULT_REPO, letters=None):
    tasks = tasks_by_id(issues)
    letters = letter_ids() if letters is None else letters
    return [card(record, tasks.get(record["id"]), letters, repo) for record in records]


def by_stage(items):
    columns = {key: [] for key, _, _ in STAGES}
    for item in items:
        columns[item["stage"]].append(item)
    return columns


def render_markdown(items, generated, repo=DEFAULT_REPO):
    """The board GitHub renders: a section per stage, a card per dataset that opens."""
    columns = by_stage(items)
    lines = [
        "# Pipeline: where every dataset stands",
        "",
        f"Written by tools/pipeline.py on {generated} from the records under datasets/ and the tasks of",
        f"https://github.com/{repo}; nobody edits it by hand. A dataset moves left to right: a record's",
        "status and route put it in its column, its history is the steps taken so far, its obstacles are",
        "what stands in the way, and its next step is what whoever holds it does next. The interactive",
        "board is pipeline.html beside this file, served by the docs site. Inside each stage the X-ray",
        "sets (fluoroscopy, video, projections, films) come before CT, the owner's order of 2026-10-21.",
        "",
        "| Stage | Datasets |",
        "|---|---|",
    ]
    for key, title, blurb in STAGES:
        lines.append(f"| [{title}](#{key}) | {len(columns[key])} |")
    lines.append("")
    for key, title, blurb in STAGES:
        lines.append(f'<a id="{key}"></a>')
        lines.append("")
        lines.append(f"## {title} ({len(columns[key])})")
        lines.append("")
        lines.append(f"{blurb[0].upper()}{blurb[1:]}.")
        lines.append("")
        for item in columns[key]:
            lines.extend(card_markdown(item))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def card_markdown(item):
    summary = f"<b>{html.escape(item['name'])}</b> ({item['group']}, {item['route']}"
    if item["holder"]:
        summary += f", {html.escape(item['holder'])}"
    summary += ")"
    body = [f"<details><summary>{summary}</summary>", ""]
    body.append(f"- What: {item['what']}")
    body.append(f"- Licence: {item['licence']}")
    body.append(f"- Status: {item['status']}" + (f"; task {item['task_state']}" if item["task_state"] else ""))
    if item["history"]:
        body.append("- Steps so far:")
        for entry in item["history"]:
            body.append(f"  - {entry.get('date', '')} {entry.get('step', '')}: {entry.get('note', '')}")
    if item["obstacles"]:
        body.append("- Obstacles:")
        for obstacle in item["obstacles"]:
            body.append(f"  - {obstacle}")
    body.append(f"- Next: {item['next'] or 'not written yet'}")
    body.append("- Links: " + ", ".join(f"[{label}]({url})" for label, url in item["links"]))
    body.append("")
    body.append("</details>")
    body.append("")
    return body


HTML_HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Dataset pipeline</title>
<style>
:root { --bg: #f6f4ef; --fg: #1f2328; --muted: #6b665c; --card: #ffffff; --line: #d9d4c7; --accent: #8a4b12; --ok: #2d6a4f; --warn: #b7791f; --bad: #a23b3b; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --bg: #1c1b18; --fg: #e8e4da; --muted: #a39d90; --card: #262420; --line: #3b382f; --accent: #e0a165; --ok: #7bc7a0; --warn: #e3b55a; --bad: #e08484; color-scheme: dark; } }
:root[data-theme="dark"] { --bg: #1c1b18; --fg: #e8e4da; --muted: #a39d90; --card: #262420; --line: #3b382f; --accent: #e0a165; --ok: #7bc7a0; --warn: #e3b55a; --bad: #e08484; color-scheme: dark; }
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--fg); font: 14px/1.45 system-ui, -apple-system, "Segoe UI", sans-serif; padding-block: 16px; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); }
h1 { font-size: 20px; margin: 0 0 4px; }
p.lead { margin: 0 0 12px; color: var(--muted); max-width: 70ch; }
.filters { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 12px; align-items: center; }
.filters select, .filters input { font: inherit; padding: 6px 8px; border: 1px solid var(--line); border-radius: 6px; background: var(--card); color: var(--fg); }
.filters input { min-width: 220px; flex: 1 1 220px; }
.counts { color: var(--muted); }
.board { display: flex; gap: 10px; overflow-x: auto; padding-bottom: 12px; align-items: flex-start; }
.column { flex: 0 0 260px; background: var(--card); border: 1px solid var(--line); border-radius: 8px; padding: 8px; min-width: 0; }
.column h2 { font-size: 14px; margin: 0 0 2px; display: flex; justify-content: space-between; }
.column h2 span { color: var(--muted); font-weight: normal; }
.column p { margin: 0 0 8px; color: var(--muted); font-size: 12px; }
.card { overflow-wrap: anywhere; border: 1px solid var(--line); border-left: 4px solid var(--accent); border-radius: 6px; padding: 6px 8px; margin-bottom: 6px; cursor: pointer; background: var(--bg); }
.card:hover, .card.open { outline: 2px solid var(--accent); }
.card .name { font-weight: 600; }
.card .meta { color: var(--muted); font-size: 12px; }
.card .next { font-size: 12px; margin-top: 2px; }
.card[data-stage="on-grid"] { border-left-color: var(--ok); }
.card[data-stage="needs-owner"], .card[data-stage="later"] { border-left-color: var(--warn); }
.card[data-stage="refused"] { border-left-color: var(--bad); }
.detail { position: fixed; right: 0; top: 0; bottom: 0; width: min(480px, 100%); background: var(--card); border-left: 1px solid var(--line); padding: 16px; overflow-y: auto; box-shadow: -4px 0 16px rgba(0,0,0,0.15); }
.detail[hidden] { display: none; }
.detail h3 { margin: 0 64px 6px 0; font-size: 16px; overflow-wrap: anywhere; }
.detail dd { overflow-wrap: anywhere; }
.detail .close { position: absolute; right: 12px; top: 12px; font: inherit; background: none; border: 1px solid var(--line); border-radius: 6px; color: var(--fg); padding: 2px 8px; cursor: pointer; }
.detail dt { font-weight: 600; margin-top: 10px; }
.detail dd { margin: 2px 0 0; }
.detail ul { margin: 2px 0 0; padding-left: 18px; }
.detail a { color: var(--accent); }
.hidden { display: none; }
</style>
</head>
<body>
"""

HTML_SCRIPT = """
<script>
(function () {
  var data = JSON.parse(document.getElementById('data').textContent);
  var stages = data.stages, items = data.items;
  var byId = {};
  items.forEach(function (it) { byId[it.id] = it; });
  var filters = { stage: '', group: '', route: '', holder: '', q: '' };
  function options(select, values, label) {
    select.innerHTML = '<option value="">' + label + '</option>' + values.map(function (v) {
      return '<option value="' + esc(v) + '">' + esc(v) + '</option>'; }).join('');
  }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }
  function uniq(key) { var seen = {}; items.forEach(function (it) { if (it[key]) seen[it[key]] = 1; }); return Object.keys(seen).sort(); }
  function visible(it) {
    if (filters.stage && it.stage !== filters.stage) return false;
    if (filters.group && it.group !== filters.group) return false;
    if (filters.route && it.route !== filters.route) return false;
    if (filters.holder && it.holder !== filters.holder) return false;
    if (filters.q) {
      var hay = (it.name + ' ' + it.what + ' ' + it.next + ' ' + it.obstacles.join(' ') + ' ' + it.id).toLowerCase();
      if (hay.indexOf(filters.q.toLowerCase()) < 0) return false;
    }
    return true;
  }
  function draw() {
    var board = document.getElementById('board');
    board.innerHTML = '';
    var shown = 0;
    stages.forEach(function (st) {
      if (filters.stage && st.key !== filters.stage) return;
      var col = document.createElement('div'); col.className = 'column';
      var cards = items.filter(function (it) { return it.stage === st.key && visible(it); });
      shown += cards.length;
      col.innerHTML = '<h2>' + esc(st.title) + ' <span>' + cards.length + '</span></h2><p>' + esc(st.blurb) + '</p>';
      cards.forEach(function (it) {
        var c = document.createElement('div'); c.className = 'card'; c.dataset.stage = it.stage; c.dataset.id = it.id;
        var meta = [it.group, it.route]; if (it.holder) meta.push(it.holder);
        c.innerHTML = '<div class="name">' + esc(it.name) + '</div><div class="meta">' + esc(meta.join(' / ')) + '</div>'
          + (it.next ? '<div class="next">Next: ' + esc(it.next) + '</div>' : '');
        c.addEventListener('click', function () { open(it.id); });
        col.appendChild(c);
      });
      board.appendChild(col);
    });
    document.getElementById('counts').textContent = shown + ' of ' + items.length + ' datasets shown';
  }
  function open(id) {
    var it = byId[id], d = document.getElementById('detail');
    var h = '<button class="close" id="close">Close</button><h3>' + esc(it.name) + '</h3>';
    h += '<div class="meta">' + esc([it.group, it.route, it.status, it.holder].filter(Boolean).join(' / ')) + '</div><dl>';
    h += '<dt>What</dt><dd>' + esc(it.what) + '</dd>';
    h += '<dt>Licence</dt><dd>' + esc(it.licence) + '</dd>';
    h += '<dt>Steps so far</dt><dd>' + (it.history.length ? '<ul>' + it.history.map(function (e) {
      return '<li>' + esc(e.date) + ' ' + esc(e.step) + ': ' + esc(e.note) + '</li>'; }).join('') + '</ul>' : 'none recorded') + '</dd>';
    h += '<dt>Obstacles</dt><dd>' + (it.obstacles.length ? '<ul>' + it.obstacles.map(function (o) { return '<li>' + esc(o) + '</li>'; }).join('') + '</ul>' : 'none recorded') + '</dd>';
    h += '<dt>Next step</dt><dd>' + esc(it.next || 'not written yet') + '</dd>';
    h += '<dt>Links</dt><dd>' + it.links.map(function (l) { return '<a href="' + esc(l[1]) + '" target="_blank" rel="noopener">' + esc(l[0]) + '</a>'; }).join(' | ') + '</dd></dl>';
    d.innerHTML = h; d.hidden = false;
    document.querySelectorAll('.card').forEach(function (c) { c.classList.toggle('open', c.dataset.id === id); });
    document.getElementById('close').addEventListener('click', function () { d.hidden = true; document.querySelectorAll('.card.open').forEach(function (c) { c.classList.remove('open'); }); });
  }
  var sel = { stage: document.getElementById('f-stage'), group: document.getElementById('f-group'), route: document.getElementById('f-route'), holder: document.getElementById('f-holder') };
  sel.stage.innerHTML = '<option value="">every stage</option>' + stages.map(function (s) { return '<option value="' + esc(s.key) + '">' + esc(s.title) + '</option>'; }).join('');
  options(sel.group, uniq('group'), 'every group');
  options(sel.route, uniq('route'), 'every route');
  options(sel.holder, uniq('holder'), 'every holder');
  Object.keys(sel).forEach(function (k) { sel[k].addEventListener('change', function () { filters[k] = sel[k].value; draw(); }); });
  document.getElementById('f-q').addEventListener('input', function (e) { filters.q = e.target.value; draw(); });
  draw();
  var wanted = location.hash.replace('#', '');
  if (wanted && byId[wanted]) open(wanted);
})();
</script>
</body>
</html>
"""


def render_html(items, generated, repo=DEFAULT_REPO):
    """The interactive board: the same cards, filters, a search box, a detail panel."""
    data = {"stages": [{"key": key, "title": title, "blurb": blurb} for key, title, blurb in STAGES],
            "items": items, "generated": generated}
    payload = json.dumps(data).replace("</", "<\\/")
    body = [
        HTML_HEAD,
        "<h1>Dataset pipeline</h1>",
        f'<p class="lead">Where every dataset of <a href="https://github.com/{repo}">{html.escape(repo)}</a> stands between the registry and the grid, written on {html.escape(generated)} from the records and the tasks. Press a card for its steps, obstacles, next step and links; the columns run from left to right, and inside each column the X-ray sets (fluoroscopy, video, projections, films) come before CT, as the owner ordered on 2026-10-21.</p>',
        '<div class="filters"><select id="f-stage"></select><select id="f-group"></select><select id="f-route"></select><select id="f-holder"></select><input id="f-q" type="search" placeholder="search names, notes, next steps"><span class="counts" id="counts"></span></div>',
        '<div class="board" id="board"></div>',
        '<aside class="detail" id="detail" hidden></aside>',
        f'<script id="data" type="application/json">{payload}</script>',
        HTML_SCRIPT,
    ]
    return "\n".join(body)


def problems(records, letters=None):
    """What is wrong with the records' pipeline fields, one line each; empty when nothing."""
    letters = letter_ids() if letters is None else letters
    found = []
    for record in records:
        ident = record.get("id", "?")
        if record.get("route") not in ROUTES:
            found.append(f"{ident}: route {record.get('route')!r} is not one of {ROUTES}")
        if record.get("status") not in STATUSES:
            found.append(f"{ident}: status {record.get('status')!r} is not one of {STATUSES}")
        if not isinstance(record.get("history"), list):
            found.append(f"{ident}: history must be a list")
        else:
            for entry in record["history"]:
                if not isinstance(entry, dict) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(entry.get("date", ""))):
                    found.append(f"{ident}: a history entry needs a date YYYY-MM-DD")
                elif entry.get("step") not in STEPS:
                    found.append(f"{ident}: history step {entry.get('step')!r} is not one of {STEPS}")
                elif not str(entry.get("note", "")).strip():
                    found.append(f"{ident}: the history entry of {entry['date']} has no note")
        if not isinstance(record.get("obstacles"), list) or not all(isinstance(o, str) for o in record.get("obstacles", [])):
            found.append(f"{ident}: obstacles must be a list of strings")
        if not isinstance(record.get("next"), str):
            found.append(f"{ident}: next must be a string")
        if record.get("status") in ("requested", "granted", "fetching", "fetched", "refused", "needs-owner") and not record.get("history"):
            found.append(f"{ident}: status {record['status']} with no history entry saying when")
        if record.get("route") in ("letter", "form") and record.get("status") == "todo" and ident not in letters:
            found.append(f"{ident}: route {record['route']} still to send with no letters/{ident}.md")
    return found


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    render = sub.add_parser("render", help="write PIPELINE.md and pipeline.html")
    render.add_argument("--out", required=True, help="the folder to write into")
    render.add_argument("--issues", help="a JSON list of the repository's issues, from gh api")
    render.add_argument("--repo", default=DEFAULT_REPO)
    render.add_argument("--date", default=date.today().isoformat())
    sub.add_parser("check", help="fail when a record's pipeline fields do not hold together")
    args = parser.parse_args(argv)
    records = load_records()
    if args.command == "check":
        found = problems(records)
        for line in found:
            print(line)
        print(f"pipeline: {len(records)} records, {len(found)} problems")
        return 1 if found else 0
    issues = []
    if args.issues:
        issues = json.loads(Path(args.issues).read_text(encoding="utf-8"))
    items = cards(records, issues, args.repo)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "PIPELINE.md").write_text(render_markdown(items, args.date, args.repo), encoding="utf-8")
    (out / "pipeline.html").write_text(render_html(items, args.date, args.repo), encoding="utf-8")
    columns = by_stage(items)
    print("pipeline: " + ", ".join(f"{STAGE_TITLES[key]} {len(columns[key])}" for key, _, _ in STAGES))
    return 0


if __name__ == "__main__":
    sys.exit(main())
