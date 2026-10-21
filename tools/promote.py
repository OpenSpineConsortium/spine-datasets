"""The trusted copy: a merged manifest's files, fetched and checked, into the read-only shared tree.

Source: the thread "Automated dataset PR review", 2026-10-21 (issue #100), after a collaborator's
fetch job stopped because only the owner may write /rs/rs_grp_oschome/shared/datasets.

A collaborator never writes the shared tree. They open a pull request with the record and a
manifest, manifests/<id>.json, naming every file with its download link, its bytes and its
sha256, or the md5 a source such as Zenodo gives in its place; the required check reviews it
(tools/dataset_review.py); the owner, or a session on the owner's standing word, merges it.
This script then runs as the owner's own grid account, inside a Slurm job that grid/promote.sh
keeps queued, and for each manifest on the default branch that is not yet promoted:

1. checks where it came from: the last commit that touched it must belong to a pull request into
   the default branch merged by one of the owners named on the command line, and not from the
   promoter's own promote/ branches, so a manifest a collaborator merged alone, or pushed past
   review, is never acted on;
2. checks it again by the same rules the review used (valid_manifest, below);
3. leaves a terabyte free on the volume, downloads every file from its link (https only, never
   more than its stated size) into shared/<id>/.incoming-<job>, resuming what an earlier job
   left, and checks the bytes and the checksum of what landed, never of what was promised;
4. moves the checked tree to shared/<id>/raw in one rename, makes every file 0444 and every
   folder 0555, and writes PROMOTED.json beside it;
5. opens the record's update (status fetched, grid_path, a history entry) as a pull request from
   the branch promote/<id>, with auto-merge on for that exact commit only, so the required check
   reviews that change too and a push by anyone else is never merged by it.

X-ray groups go before CT, the owner's order of 2026-10-21. Nothing under the shared tree is ever
deleted or overwritten: a raw/ already there is adopted only when every file matches, and a
failure leaves .incoming-<job> for the next job to resume and says so in the job's log.

A stricter rule decides whether what runs as the owner may change: `self-update` copies this file
and grid/promote.sh from the default branch into the promoter's folder, and the space budget in
grid/promote.json is read, only where the last change to each came from a pull request an owner
opened and merged with no commit in it tied to anyone else's account; anything else keeps the copy on the grid, or the default
budget.

It runs on the grid's own python3, which on its EL7 nodes may be as old as 3.6, so it uses nothing
newer, and needs gh signed in as the owner and curl, both already there for hpcworker.

    python3 tools/promote.py once --repo OWNER/NAME --shared DIR --owners LOGIN[,LOGIN] [--job ID]
    python3 tools/promote.py self-update --repo OWNER/NAME --owners LOGIN[,LOGIN] --into DIR
"""

import argparse
import base64
import hashlib
import json
import os
import re
import subprocess
import sys
import time

DEFAULT_BRANCH = "main"
# X-ray groups first, CT after them (the owner, 2026-10-21), as tools/pipeline.py orders them.
GROUP_ORDER = ("fluoro", "video", "projections", "films", "ct", "future")
# The space one merge may take without the owner naming the set in grid/promote.json.
MAX_BYTES = 100 * 10 ** 9
ID_SHAPE = re.compile(r"^[a-z0-9_]+$")
SHA256_SHAPE = re.compile(r"^[0-9a-f]{64}$")
MD5_SHAPE = re.compile(r"^[0-9a-f]{32}$")
PATH_SHAPE = re.compile(r"^raw/[A-Za-z0-9._()+ -]+(/[A-Za-z0-9._()+ -]+)*$")
# Query names that make a link a credential: a token, a key or a signature for a presigned store.
CREDENTIAL_QUERY = re.compile(
    r"(^|[?&])(token|access_token|key|api_key|apikey|sig|signature|x-amz-[a-z-]+|x-goog-[a-z-]+|"
    r"expires|auth|authorization|password|se|sp|sv)=",
    re.IGNORECASE,
)
OPEN_LICENCE = re.compile(
    r"\b(CC[ -]?BY|CC0|CC[ -]?ZERO|PDDL|ODC[ -]?BY|ODbL|public domain|MIT|Apache)\b", re.IGNORECASE
)
RESTRICTED_LICENCE = re.compile(r"\b(NC|ND|non-?commercial|no ?deriv)", re.IGNORECASE)
TRUSTED_CODE = ("tools/promote.py", "grid/promote.sh")
BUDGET = "grid/promote.json"
# A source whose files are served from another host of its own; any other file must be on the
# source's own host exactly, so a shared suffix (s3.amazonaws.com, github.io) is never enough.
DOWNLOAD_HOSTS = {
    "figshare.com": ("ndownloader.figshare.com",),
    "data.mendeley.com": ("data.mendeley.com",),
    "zenodo.org": ("zenodo.org",),
}
# Space the promoter leaves free on the shared volume, as the owner's own fetch chain does.
RESERVE_BYTES = 10 ** 12
# A web or API commit is committed by GitHub's own web-flow on the person's behalf.
GITHUB_COMMITTER = "web-flow"


# The rules a manifest is held to, shared with tools/dataset_review.py so the review and the
# promoter can never disagree about what a valid manifest is.

def host_of(url):
    match = re.match(r"^https://([^/?#@]+)(/|$)", url or "")
    return match.group(1).lower() if match else ""


def same_site(host, source_host):
    """The file's host is the source's own, or one the source is known to serve its files from."""
    if not host or not source_host:
        return False
    bare = source_host[4:] if source_host.startswith("www.") else source_host
    return host in (source_host, bare) or host in DOWNLOAD_HOSTS.get(bare, ())


def licence_problems(record):
    """Why the record's licence does not yet allow a fetch, or nothing."""
    licence = record.get("licence") or ""
    if re.search(r"to confirm", licence, re.IGNORECASE):
        return ["the licence still reads 'to confirm': read the page and write its licence line"]
    if OPEN_LICENCE.search(licence) and not RESTRICTED_LICENCE.search(licence):
        return []
    steps = [entry.get("step") for entry in record.get("history", [])]
    if record.get("status") in ("fetching", "fetched") and "granted" in steps:
        return []
    return ["the licence '%s' is not an open licence without restrictions and the history records no grant"
            % licence]


def valid_manifest(manifest, record, ident):
    """Every problem with a manifest, as one-line strings; an empty list means it holds."""
    problems = []
    if not ID_SHAPE.match(ident or ""):
        return ["the id '%s' is not lower-case letters, digits and underscores" % ident]
    if manifest.get("id") != ident:
        problems.append("its id is '%s', not the file's name '%s'" % (manifest.get("id"), ident))
    if record is None:
        return problems + ["there is no record datasets/%s.json" % ident]
    if manifest.get("source") != record.get("link"):
        problems.append("its source is not the record's link exactly")
    if manifest.get("licence") != record.get("licence"):
        problems.append("its licence is not the record's licence exactly")
    problems += licence_problems(record)
    if record.get("status") not in ("fetching", "fetched"):
        problems.append("the record's status is '%s', not fetching or fetched" % record.get("status"))
    files = manifest.get("files")
    if not isinstance(files, list) or not files:
        return problems + ["it names no files"]
    source_host = host_of(record.get("link"))
    seen = set()
    total = 0
    for number, entry in enumerate(files, 1):
        problems += file_problems(entry, number, source_host, seen)
        if isinstance(entry, dict) and isinstance(entry.get("bytes"), int):
            total += entry["bytes"]
    if manifest.get("bytes_total") != total:
        problems.append("bytes_total is %s but the files add up to %d" % (manifest.get("bytes_total"), total))
    return problems


def file_problems(entry, number, source_host, seen):
    if not isinstance(entry, dict):
        return ["file %d is not an object" % number]
    problems = []
    path = entry.get("path") or ""
    where = "file %d (%s)" % (number, path)
    if not PATH_SHAPE.match(path) or "/../" in "/" + path + "/" or "/./" in "/" + path + "/":
        problems.append("%s: the path must be raw/<name> with plain names and no '..'" % where)
    if path in seen:
        problems.append("%s: named twice" % where)
    seen.add(path)
    url = entry.get("url") or ""
    if not host_of(url):
        problems.append("%s: the url must be https:// with no user or password in it" % where)
    elif not same_site(host_of(url), source_host):
        problems.append("%s: the url's host %s is not the source's (%s)" % (where, host_of(url), source_host))
    if CREDENTIAL_QUERY.search(url.split("?", 1)[1] if "?" in url else ""):
        problems.append("%s: the url carries a token, key or signature; links must be public" % where)
    size = entry.get("bytes")
    if not isinstance(size, int) or isinstance(size, bool) or size <= 0:
        problems.append("%s: bytes must be a positive whole number" % where)
    if "sha256" in entry or "md5" not in entry:
        if not SHA256_SHAPE.match(entry.get("sha256") or ""):
            problems.append("%s: sha256 must be 64 lower-case hex digits" % where)
    elif not MD5_SHAPE.match(entry.get("md5") or ""):
        problems.append("%s: md5, where the source gives no sha256, must be 32 lower-case hex digits" % where)
    return problems


def group_rank(record):
    group = (record or {}).get("group", "")
    return GROUP_ORDER.index(group) if group in GROUP_ORDER else len(GROUP_ORDER)


# GitHub, through the owner's own gh sign-in on the grid.

def gh(args, data=None):
    """gh's answer as text; raises RuntimeError with gh's own words when it fails.

    Bytes in and out, decoded as UTF-8 here, since Python 3.6 under the grid's C locale would
    otherwise decode GitHub's answers as ASCII and fail on the first accented name."""
    process = subprocess.Popen(["gh"] + list(args), stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    out, err = process.communicate(data.encode("utf-8") if data is not None else None)
    out, err = out.decode("utf-8", "replace"), err.decode("utf-8", "replace")
    if process.returncode != 0:
        raise RuntimeError("gh %s: %s" % (" ".join(args[:2]), err.strip() or out.strip()))
    return out


def gh_json(args, data=None):
    return json.loads(gh(args, data) or "null")


def file_at(repo, path, ref):
    """A file's text and blob sha at a ref, or (None, None) where it does not exist."""
    try:
        meta = gh_json(["api", "repos/%s/contents/%s?ref=%s" % (repo, path, ref)])
    except RuntimeError as error:
        if "404" in str(error) or "Not Found" in str(error):
            return None, None
        raise
    # the raw form, since the contents API leaves content empty for a file over 1 MB
    text = gh(["api", "-H", "Accept: application/vnd.github.raw", "repos/%s/contents/%s?ref=%s" % (repo, path, ref)])
    return text, meta["sha"]


def merged_by_owner(repo, path, owners, strict=False):
    """The commit and pull request that last changed path on the default branch, when an owner merged it.

    Never a pull request from a promote/ branch, the promoter's own, which only ever updates a
    record: anyone who may write can push to such a branch before its auto-merge lands. With
    strict, for what runs as the owner (the promoter's code and its space budget), an owner must
    also have opened the pull request, and no commit in it may be tied to anyone else's account."""
    commits = gh_json(["api", "repos/%s/commits?sha=%s&path=%s&per_page=1" % (repo, DEFAULT_BRANCH, path)])
    if not commits:
        return None
    sha = commits[0]["sha"]
    for pull in gh_json(["api", "repos/%s/commits/%s/pulls" % (repo, sha)]) or []:
        if not pull.get("merged_at") or pull.get("base", {}).get("ref") != DEFAULT_BRANCH:
            continue
        detail = gh_json(["api", "repos/%s/pulls/%d" % (repo, pull["number"])])
        login = (detail.get("merged_by") or {}).get("login", "")
        if login not in owners or detail.get("head", {}).get("ref", "").startswith("promote/"):
            continue
        if strict and not written_by_owners(repo, detail, owners):
            continue
        return {"commit": sha, "pull": pull["number"], "merged_by": login}
    return None


def written_by_owners(repo, detail, owners):
    if (detail.get("user") or {}).get("login") not in owners:
        return False
    commits = gh_json(["api", "repos/%s/pulls/%d/commits?per_page=100" % (repo, detail["number"])]) or []
    # A commit GitHub ties to an account must be an owner's; one it ties to none, as a session's
    # commits made under its own name are, is the owner's pull request's.
    allowed = set(owners) | {GITHUB_COMMITTER}
    for commit in commits:
        for role in ("author", "committer"):
            login = (commit.get(role) or {}).get("login")
            if login and login not in allowed:
                return False
    return len(commits) < 100


def manifest_ids(repo):
    listing = gh_json(["api", "repos/%s/contents/manifests?ref=%s" % (repo, DEFAULT_BRANCH)]) or []
    return sorted(item["name"][:-5] for item in listing
                  if item.get("type") == "file" and item["name"].endswith(".json"))


# The shared tree.

def digest_of(path, name="sha256"):
    digest = hashlib.new(name)
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def file_matches(path, entry):
    name = "sha256" if "sha256" in entry else "md5"
    return (os.path.isfile(path) and not os.path.islink(path)
            and os.path.getsize(path) == entry["bytes"] and digest_of(path, name) == entry[name])


def download(url, dest, size):
    """curl, resuming what an earlier job left; https only, redirects included, no globbing, and
    never more than the manifest's size; returns curl's exit code."""
    parent = os.path.dirname(dest)
    if not os.path.isdir(parent):
        os.makedirs(parent)
    command = ["curl", "-fsSL", "-g", "--proto", "=https", "--proto-redir", "=https", "--max-filesize", str(size),
               "--retry", "5", "--retry-delay", "10", "-C", "-", "-o", dest, url]
    return subprocess.call(command)


def fetch_into(incoming, manifest, log):
    """Every file downloaded and checked under incoming; returns the files that did not check.

    A file that is whole but wrong, or that a server would not resume, is removed so the next try
    starts it afresh; a partial one after a broken transfer is kept for curl to resume."""
    bad = []
    for entry in manifest["files"]:
        dest = os.path.join(incoming, entry["path"])
        if file_matches(dest, entry):
            continue
        if os.path.exists(dest) and os.path.getsize(dest) >= entry["bytes"]:
            os.remove(dest)
        code = download(entry["url"], dest, entry["bytes"])
        if file_matches(dest, entry):
            continue
        log("%s: %s did not check (curl exit %s)" % (manifest["id"], entry["path"], code))
        bad.append(entry["path"])
        if os.path.exists(dest) and (code in (0, 33, 63) or os.path.getsize(dest) >= entry["bytes"]):
            os.remove(dest)
    return bad


def tree_matches(raw_parent, manifest):
    return all(file_matches(os.path.join(raw_parent, entry["path"]), entry) for entry in manifest["files"])


def make_read_only(top):
    for folder, folders, files in os.walk(top, topdown=False):
        for name in files:
            os.chmod(os.path.join(folder, name), 0o444)
        os.chmod(folder, 0o555)


def write_promoted(home, manifest, origin, job):
    note = {
        "id": manifest["id"],
        "date": time.strftime("%Y-%m-%d", time.gmtime()),
        "job_id": job,
        "manifest_commit": origin["commit"],
        "pull_request": origin["pull"],
        "merged_by": origin["merged_by"],
        "bytes_total": manifest["bytes_total"],
        "files": [{"path": e["path"], "bytes": e["bytes"], "sha256": digest_of(os.path.join(home, e["path"]))}
                  for e in manifest["files"]],
    }
    path = os.path.join(home, "PROMOTED.json")
    with open(path + ".tmp", "w") as handle:
        json.dump(note, handle, indent=1, sort_keys=True)
        handle.write("\n")
    os.rename(path + ".tmp", path)
    os.chmod(path, 0o444)
    return note


def free_bytes(folder):
    stats = os.statvfs(folder)
    return stats.f_bavail * stats.f_frsize


def install(shared, manifest, origin, job, log, reserve=RESERVE_BYTES):
    """Fetch, check and install one manifest; returns 'promoted', 'waiting', 'no-space' or 'conflict'."""
    home = os.path.join(shared, manifest["id"])
    raw = os.path.join(home, "raw")
    for folder in (shared, home):
        if not os.path.isdir(folder):
            os.makedirs(folder)
            os.chmod(folder, 0o755)
    if os.path.exists(raw):
        if not tree_matches(home, manifest):
            log("%s: raw/ is already there and does not match the manifest; nothing changed" % manifest["id"])
            return "conflict"
    else:
        if free_bytes(home) < manifest["bytes_total"] + reserve:
            log("%s: %d bytes would leave less than %d free on the shared volume; waiting"
                % (manifest["id"], manifest["bytes_total"], reserve))
            return "no-space"
        incoming = os.path.join(home, ".incoming-%s" % job)
        leftover = [os.path.join(home, name) for name in os.listdir(home) if name.startswith(".incoming-")]
        if leftover and not os.path.exists(incoming):
            os.rename(max(leftover, key=os.path.getmtime), incoming)
        if fetch_into(incoming, manifest, log):
            return "waiting"
        os.rename(os.path.join(incoming, "raw"), raw)
        try:
            os.rmdir(incoming)
        except OSError:
            pass
    make_read_only(raw)
    write_promoted(home, manifest, origin, job)
    return "promoted"


# The record's update, as a pull request the required check reviews.

def updated_record(record, manifest, shared, job):
    record = json.loads(json.dumps(record))
    path = "%s/%s/raw" % (shared.rstrip("/"), manifest["id"])
    today = time.strftime("%Y-%m-%d", time.gmtime())
    line = "%s: on the grid at %s, %d files, %d bytes, sha256-checked, promoter job %s" % (
        today, path, len(manifest["files"]), manifest["bytes_total"], job)
    record["status"] = "fetched"
    record["grid_path"] = path
    record["result"] = line
    record.setdefault("history", []).append({"date": today, "step": "fetched", "note": line[12:]})
    record["obstacles"] = []
    record["next"] = ""
    return json.dumps(record, indent=1, ensure_ascii=True) + "\n"


def task_number(repo, ident):
    query = "repo:%s is:issue \"Record: datasets/%s.json\"" % (repo, ident)
    found = gh_json(["api", "-X", "GET", "search/issues", "-f", "q=" + query])
    items = (found or {}).get("items") or []
    return items[0]["number"] if items else None


def open_record_update(repo, manifest, shared, job, origin):
    ident = manifest["id"]
    branch = "promote/%s" % ident
    text, blob = file_at(repo, "datasets/%s.json" % ident, DEFAULT_BRANCH)
    if text is None or json.loads(text).get("status") == "fetched":
        return None
    head = gh_json(["api", "repos/%s/git/ref/heads/%s" % (repo, DEFAULT_BRANCH)])["object"]["sha"]
    try:
        gh(["api", "-X", "POST", "repos/%s/git/refs" % repo, "-f", "ref=refs/heads/" + branch, "-f", "sha=" + head])
    except RuntimeError as error:
        if "already exists" not in str(error):
            raise
        owner = repo.split("/")[0]
        if not gh_json(["api", "repos/%s/pulls?state=open&head=%s:%s" % (repo, owner, branch)]):
            raise RuntimeError("%s exists with no open pull request; the owner looks at it" % branch)
        return None
    body = updated_record(json.loads(text), manifest, shared, job)
    written = gh_json(["api", "-X", "PUT", "repos/%s/contents/datasets/%s.json" % (repo, ident), "--input", "-"],
                      json.dumps({
                          "message": "Record %s as on the grid (promoter job %s)" % (ident, job),
                          "content": base64.b64encode(body.encode("ascii")).decode("ascii"),
                          "sha": blob, "branch": branch,
                      }))
    task = task_number(repo, ident)
    lines = [
        "The promoter checked every file of manifests/%s.json (from #%d, merged by %s) and installed it read-only."
        % (ident, origin["pull"], origin["merged_by"]),
        "",
        "This updates the record to fetched with its grid path.",
    ]
    if task:
        lines += ["", "Closes #%d" % task]
    pull = gh_json(["api", "-X", "POST", "repos/%s/pulls" % repo, "--input", "-"], json.dumps({
        "title": "Record %s as on the grid" % ident, "head": branch, "base": DEFAULT_BRANCH,
        "body": "\n".join(lines),
    }))
    try:
        enable_auto_merge(pull["node_id"], written["commit"]["sha"])
    except RuntimeError as error:
        print("auto-merge not set on #%d: %s" % (pull["number"], error))
    return pull["number"]


def enable_auto_merge(pull_id, head_sha):
    """Auto-merge for the exact commit the promoter wrote, so a push by anyone else is never merged by it."""
    query = ("mutation($id: ID!, $oid: GitObjectID!) { enablePullRequestAutoMerge(input: "
             "{pullRequestId: $id, expectedHeadOid: $oid, mergeMethod: SQUASH}) { clientMutationId } }")
    gh(["api", "graphql", "-f", "query=" + query, "-f", "id=" + pull_id, "-f", "oid=" + head_sha])


# The commands.

def load_budget(repo, owners, log):
    """The space budget, as an owner wrote it; the default where anyone else last changed it."""
    origin = merged_by_owner(repo, BUDGET, owners, strict=True)
    if origin is None:
        if file_at(repo, BUDGET, DEFAULT_BRANCH)[0] is not None:
            log("%s was last changed outside an owner's own pull request; using the default budget" % BUDGET)
        return MAX_BYTES, set()
    settings = json.loads(file_at(repo, BUDGET, origin["commit"])[0])
    return settings.get("max_bytes", MAX_BYTES), set(settings.get("approved_over_budget", []))


def candidates(repo, shared, owners, log):
    """The manifests to act on now, X-ray first, each with its record and its origin."""
    found = []
    for ident in manifest_ids(repo):
        if not ID_SHAPE.match(ident) or os.path.exists(os.path.join(shared, ident, "PROMOTED.json")):
            continue
        try:
            item = candidate(repo, ident, owners, log)
        except (RuntimeError, ValueError, KeyError) as error:
            log("%s: skipped this pass: %s" % (ident, error))
            continue
        if item:
            found.append(item)
    return [item[2:] for item in sorted(found, key=lambda item: item[:2])]


def candidate(repo, ident, owners, log):
    origin = merged_by_owner(repo, "manifests/%s.json" % ident, owners)
    if origin is None:
        log("%s: the manifest's last change was not merged by an owner; skipped" % ident)
        return None
    text, _ = file_at(repo, "manifests/%s.json" % ident, origin["commit"])
    record_text, _ = file_at(repo, "datasets/%s.json" % ident, origin["commit"])
    manifest = json.loads(text)
    record = json.loads(record_text) if record_text else None
    problems = valid_manifest(manifest, record, ident)
    if problems:
        log("%s: %s" % (ident, "; ".join(problems)))
        return None
    return (group_rank(record), ident, manifest, record, origin)


def ascii_log(line):
    print(line.encode("ascii", "backslashreplace").decode("ascii"))
    sys.stdout.flush()


def once(args, log=ascii_log):
    owners = set(args.owners.split(","))
    max_bytes, approved = load_budget(args.repo, owners, log)
    results = {}
    finish_record_updates(args, log)
    for manifest, record, origin in candidates(args.repo, args.shared, owners, log):
        ident = manifest["id"]
        if manifest["bytes_total"] > max_bytes and ident not in approved:
            log("%s: %d bytes is over the budget of %d; the owner names it in grid/promote.json"
                % (ident, manifest["bytes_total"], max_bytes))
            results[ident] = "over-budget"
            continue
        outcome = install(args.shared, manifest, origin, args.job, log, args.reserve)
        results[ident] = outcome
        log("%s: %s" % (ident, outcome))
        if outcome == "promoted":
            report_record_update(args, manifest, origin, log)
    return results


def report_record_update(args, manifest, origin, log):
    try:
        number = open_record_update(args.repo, manifest, args.shared, args.job, origin)
    except RuntimeError as error:
        log("%s: the record update was not opened, the next job tries again: %s" % (manifest["id"], error))
        return
    if number:
        log("%s: record update opened as #%d" % (manifest["id"], number))


def finish_record_updates(args, log):
    """A set promoted by an earlier job whose record update was not opened gets it now."""
    if not os.path.isdir(args.shared):
        return
    for ident in sorted(os.listdir(args.shared)):
        note_path = os.path.join(args.shared, ident, "PROMOTED.json")
        if not ID_SHAPE.match(ident) or not os.path.isfile(note_path):
            continue
        try:
            with open(note_path) as handle:
                note = json.load(handle)
            text, _ = file_at(args.repo, "manifests/%s.json" % ident, note["manifest_commit"])
        except (RuntimeError, ValueError, KeyError) as error:
            log("%s: the record update waits: %s" % (ident, error))
            continue
        if text is None:
            continue
        origin = {"commit": note["manifest_commit"], "pull": note["pull_request"], "merged_by": note["merged_by"]}
        report_record_update(args, json.loads(text), origin, log)


def self_update(args, log=ascii_log):
    """Copy the promoter's own files from the default branch, only from an owner's own pull request."""
    owners = set(args.owners.split(","))
    fresh = {}
    for path in TRUSTED_CODE:
        origin = merged_by_owner(args.repo, path, owners, strict=True)
        if origin is None:
            log("self-update: %s was last changed outside an owner's merge; keeping the copy here" % path)
            return False
        fresh[path] = file_at(args.repo, path, origin["commit"])[0]
    for path, text in fresh.items():
        dest = os.path.join(args.into, os.path.basename(path))
        with open(dest + ".tmp", "w") as handle:
            handle.write(text)
        os.chmod(dest + ".tmp", 0o755 if dest.endswith(".sh") else 0o644)
        os.rename(dest + ".tmp", dest)
    return True


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command")
    run = sub.add_parser("once", help="promote every merged manifest not yet promoted")
    run.add_argument("--repo", required=True)
    run.add_argument("--shared", required=True)
    run.add_argument("--owners", required=True)
    run.add_argument("--job", default=os.environ.get("SLURM_JOB_ID", "local"))
    run.add_argument("--reserve", type=int, default=RESERVE_BYTES, help="bytes left free on the shared volume")
    update = sub.add_parser("self-update", help="take the promoter's code from an owner's merge")
    update.add_argument("--repo", required=True)
    update.add_argument("--owners", required=True)
    update.add_argument("--into", required=True)
    args = parser.parse_args(argv)
    if args.command == "once":
        once(args)
        return 0
    if args.command == "self-update":
        return 0 if self_update(args) else 1
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
