"""Open the tasks of tasks/TASKS.md as GitHub issues, once each, labelled todo.

Source: the SchwingNet thread "SchwingNet video demo plan", 2026-10-21, derived from
tasks/TASKS.md, whose blocks this script reads (a heading "## Obtain ..." is a title, the lines
under it the body). It uses the standard library alone and GitHub's REST API with the token in the
environment variable GITHUB_TOKEN, which is never printed and never taken from the command line.
It is idempotent: a title that already exists among the repository's issues, open or closed, is
skipped, so running it twice opens nothing twice. --dry-run prints what it would open and sends
nothing.

    GITHUB_TOKEN=... python3 tasks/open_tasks.py --repo OpenSpineConsortium/spine-datasets --dry-run
    GITHUB_TOKEN=... python3 tasks/open_tasks.py --repo OpenSpineConsortium/spine-datasets

The token is set in the shell's environment (for example `read -s GITHUB_TOKEN; export
GITHUB_TOKEN`), so it appears in no command line and no shell history.
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://api.github.com"
LABEL = "todo"


def parse_tasks(text: str) -> list[tuple[str, str]]:
    """The (title, body) pairs of TASKS.md: each "## " heading starts one, the text to the next ends it."""
    tasks: list[tuple[str, str]] = []
    title = None
    body: list[str] = []
    for line in text.splitlines():
        if line.startswith("## "):
            if title is not None:
                tasks.append((title, "\n".join(body).strip()))
            title = line[3:].strip()
            body = []
        elif title is not None:
            body.append(line)
    if title is not None:
        tasks.append((title, "\n".join(body).strip()))
    return tasks


def request(method: str, url: str, token: str, data: dict | None = None):
    """One call to the API with the token in the header, the answer as JSON (an empty body as None)."""
    payload = None if data is None else json.dumps(data).encode()
    req = urllib.request.Request(url, data=payload, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    if payload is not None:
        req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req) as answer:
        raw = answer.read()
    return json.loads(raw) if raw else None


def existing_titles(repo: str, token: str) -> set[str]:
    """Every issue title the repository has, open or closed, pull requests left out."""
    titles: set[str] = set()
    page = 1
    while True:
        query = urllib.parse.urlencode({"state": "all", "per_page": 100, "page": page})
        issues = request("GET", f"{API}/repos/{repo}/issues?{query}", token)
        if not issues:
            return titles
        for issue in issues:
            if "pull_request" not in issue:
                titles.add(issue["title"].strip())
        page += 1


def ensure_label(repo: str, token: str) -> None:
    """The label todo exists before an issue carries it; the template makes it too, so a 422 is fine."""
    try:
        request("POST", f"{API}/repos/{repo}/labels", token,
                {"name": LABEL, "color": "0e8a16", "description": "the queue"})
    except urllib.error.HTTPError as error:
        if error.code != 422:
            raise


def open_issue(repo: str, token: str, title: str, body: str) -> int:
    answer = request("POST", f"{API}/repos/{repo}/issues", token,
                     {"title": title, "body": body, "labels": [LABEL]})
    return int(answer["number"])


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--repo", required=True, help="owner/name of the repository")
    parser.add_argument("--tasks", default=str(Path(__file__).with_name("TASKS.md")),
                        help="the TASKS.md to read (default: beside this script)")
    parser.add_argument("--dry-run", action="store_true", help="print what would be opened; send nothing")
    args = parser.parse_args(argv)

    tasks = parse_tasks(Path(args.tasks).read_text())
    if not tasks:
        print("no task found in", args.tasks, file=sys.stderr)
        return 1

    if args.dry_run:
        for number, (title, body) in enumerate(tasks, 1):
            print(f"[{number}/{len(tasks)}] would open: {title} ({len(body.splitlines())} body lines, label {LABEL})")
        return 0

    token = os.environ.get("GITHUB_TOKEN", "")
    if not token:
        print("GITHUB_TOKEN is not set in the environment; nothing opened", file=sys.stderr)
        return 2

    have = existing_titles(args.repo, token)
    ensure_label(args.repo, token)
    opened = skipped = 0
    for title, body in tasks:
        if title in have:
            skipped += 1
            print(f"skip (exists): {title}")
            continue
        number = open_issue(args.repo, token, title, body)
        have.add(title)
        opened += 1
        print(f"opened #{number}: {title}")
    print(f"{opened} opened, {skipped} skipped")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
