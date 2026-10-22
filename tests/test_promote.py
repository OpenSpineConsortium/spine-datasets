"""The promoter (tools/promote.py): provenance, the read-only install, the X-ray-first order."""

import argparse
import hashlib
import json
import os
import shutil
import stat
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import promote  # noqa: E402

OWNER = "the-owner"
REPO = "Org/spine-datasets"


def entry_for(name, payload):
    return {"path": "raw/" + name, "url": "https://data.mendeley.com/f/" + name,
            "bytes": len(payload), "sha256": hashlib.sha256(payload).hexdigest()}


class FakeGitHub:
    """Answers the promoter's gh calls from dictionaries."""

    def __init__(self, files, merged_by, head="claude/9", committer=OWNER):
        self.files = files            # path -> text, on every ref
        self.merged_by = merged_by    # path -> login that merged its last change
        self.head = head              # the merged pull request's branch
        self.committer = committer    # the login GitHub ties its commits to
        self.calls = []

    def gh_json(self, args, data=None):
        url = args[-1] if args[0] == "api" and len(args) == 2 else ""
        self.calls.append(args)
        if url.startswith("repos/%s/contents/manifests?" % REPO):
            return [{"type": "file", "name": p.split("/")[1]} for p in self.files if p.startswith("manifests/")]
        if "/pulls/7/commits" in url:
            return [{"author": {"login": self.committer}, "committer": {"login": "web-flow"}}]
        if "/commits?" in url:
            path = url.split("path=")[1].split("&")[0]
            return [{"sha": "c-" + path}] if path in self.merged_by else []
        if "/commits/c-" in url:
            return [{"number": 7, "merged_at": "2026-10-21T00:00:00Z", "base": {"ref": "main"}, "_path": url}]
        if "/pulls/7" in url:
            last = [c for c in self.calls if "/commits/c-" in c[-1]][-1][-1]
            path = last.split("/commits/c-")[1].split("/pulls")[0]
            login = self.merged_by[path]
            return {"number": 7, "merged_by": {"login": login}, "user": {"login": login},
                    "head": {"ref": self.head}}
        raise AssertionError("unexpected call %s" % (args,))

    def file_at(self, repo, path, ref):
        text = self.files.get(path)
        return (text, "blob") if text is not None else (None, None)


class PromoterTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.shared = os.path.join(self.tmp.name, "shared")
        self.source = os.path.join(self.tmp.name, "source")
        os.makedirs(self.source)
        self.saved = (promote.gh_json, promote.file_at, promote.download, promote.open_record_update)
        self.opened = []
        promote.download = self.fake_download
        promote.open_record_update = lambda *args: self.opened.append(args[1]["id"]) or 99

    def tearDown(self):
        promote.gh_json, promote.file_at, promote.download, promote.open_record_update = self.saved
        for folder, _, files in os.walk(self.tmp.name):
            os.chmod(folder, 0o755)
        self.tmp.cleanup()

    def fake_download(self, url, dest, size):
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copyfile(os.path.join(self.source, url.rsplit("/", 1)[1]), dest)
        return 0

    def dataset(self, ident, group, payloads):
        entries = []
        for name, payload in payloads.items():
            with open(os.path.join(self.source, name), "wb") as handle:
                handle.write(payload)
            entries.append(entry_for(name, payload))
        rec = {"id": ident, "group": group, "licence": "CC BY 4.0", "link": "https://data.mendeley.com/d/" + ident,
               "status": "fetching", "history": []}
        man = {"id": ident, "source": rec["link"], "licence": "CC BY 4.0", "files": entries,
               "bytes_total": sum(e["bytes"] for e in entries)}
        return {"manifests/%s.json" % ident: json.dumps(man), "datasets/%s.json" % ident: json.dumps(rec)}

    def run_once(self, files, merged_by, **fake_settings):
        fake = FakeGitHub(files, merged_by, **fake_settings)
        promote.gh_json, promote.file_at = fake.gh_json, fake.file_at
        args = argparse.Namespace(repo=REPO, shared=self.shared, owners=OWNER, job="123", reserve=0)
        logs = []
        return promote.once(args, log=logs.append), logs

    def test_an_owner_merge_is_installed_read_only(self):
        files = self.dataset("demo_set", "films", {"a.zip": b"alpha", "b.zip": b"beta"})
        results, _ = self.run_once(files, {"manifests/demo_set.json": OWNER})
        self.assertEqual(results, {"demo_set": "promoted"})
        raw = os.path.join(self.shared, "demo_set", "raw")
        self.assertEqual(stat.S_IMODE(os.stat(os.path.join(raw, "a.zip")).st_mode), 0o444)
        self.assertEqual(stat.S_IMODE(os.stat(raw).st_mode), 0o555)
        note = json.loads(Path(self.shared, "demo_set", "PROMOTED.json").read_text())
        self.assertEqual(note["merged_by"], OWNER)
        self.assertEqual(self.opened, ["demo_set"])

    def test_a_merge_by_anyone_else_is_skipped(self):
        files = self.dataset("demo_set", "films", {"a.zip": b"alpha"})
        results, logs = self.run_once(files, {"manifests/demo_set.json": "a-collaborator"})
        self.assertEqual(results, {})
        self.assertFalse(os.path.exists(os.path.join(self.shared, "demo_set")))
        self.assertTrue(any("not merged by an owner" in line for line in logs))

    def test_a_file_that_does_not_check_is_not_installed(self):
        files = self.dataset("demo_set", "films", {"a.zip": b"alpha"})
        with open(os.path.join(self.source, "a.zip"), "wb") as handle:
            handle.write(b"tampered")
        results, _ = self.run_once(files, {"manifests/demo_set.json": OWNER})
        self.assertEqual(results, {"demo_set": "waiting"})
        self.assertFalse(os.path.exists(os.path.join(self.shared, "demo_set", "raw")))

    def test_a_raw_folder_that_differs_is_never_overwritten(self):
        files = self.dataset("demo_set", "films", {"a.zip": b"alpha"})
        os.makedirs(os.path.join(self.shared, "demo_set", "raw"))
        with open(os.path.join(self.shared, "demo_set", "raw", "a.zip"), "wb") as handle:
            handle.write(b"other")
        results, _ = self.run_once(files, {"manifests/demo_set.json": OWNER})
        self.assertEqual(results, {"demo_set": "conflict"})
        self.assertEqual(Path(self.shared, "demo_set", "raw", "a.zip").read_bytes(), b"other")

    def test_xray_goes_before_ct(self):
        files = self.dataset("aaa_ct", "ct", {"c.zip": b"ct"})
        files.update(self.dataset("zzz_films", "films", {"f.zip": b"film"}))
        results, _ = self.run_once(files, {"manifests/aaa_ct.json": OWNER, "manifests/zzz_films.json": OWNER})
        self.assertEqual(list(results), ["zzz_films", "aaa_ct"])

    def test_no_size_of_its_own_holds_a_set_back(self):
        # the owner, 2026-10-22: any size the volume has room for; a stale budget file changes nothing
        files = self.dataset("demo_set", "films", {"a.zip": b"alpha"})
        files["grid/promote.json"] = json.dumps({"max_bytes": 1, "approved_over_budget": []})
        results, _ = self.run_once(files, {"manifests/demo_set.json": OWNER, "grid/promote.json": OWNER})
        self.assertEqual(results, {"demo_set": "promoted"})

    def test_a_manifest_from_the_promoters_own_branch_is_skipped(self):
        files = self.dataset("demo_set", "films", {"a.zip": b"alpha"})
        results, _ = self.run_once(files, {"manifests/demo_set.json": OWNER}, head="promote/other_set")
        self.assertEqual(results, {})

    def test_no_room_on_the_volume_waits(self):
        files = self.dataset("demo_set", "films", {"a.zip": b"alpha"})
        fake = FakeGitHub(files, {"manifests/demo_set.json": OWNER})
        promote.gh_json, promote.file_at = fake.gh_json, fake.file_at
        args = argparse.Namespace(repo=REPO, shared=self.shared, owners=OWNER, job="1", reserve=10 ** 30)
        self.assertEqual(promote.once(args, log=lambda line: None), {"demo_set": "no-space"})

    def test_a_wrong_whole_file_is_fetched_afresh(self):
        files = self.dataset("demo_set", "films", {"a.zip": b"alpha"})
        incoming = os.path.join(self.shared, "demo_set", ".incoming-old", "raw")
        os.makedirs(incoming)
        with open(os.path.join(incoming, "a.zip"), "wb") as handle:
            handle.write(b"WRONG")
        results, _ = self.run_once(files, {"manifests/demo_set.json": OWNER})
        self.assertEqual(results, {"demo_set": "promoted"})
        self.assertEqual(os.listdir(os.path.join(self.shared, "demo_set", "raw")), ["a.zip"])


class SelfUpdate(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.saved = (promote.gh_json, promote.file_at)

    def tearDown(self):
        promote.gh_json, promote.file_at = self.saved
        self.tmp.cleanup()

    def update(self, committer):
        files = {path: "new " + path for path in promote.TRUSTED_CODE}
        fake = FakeGitHub(files, {path: OWNER for path in files}, committer=committer)
        promote.gh_json, promote.file_at = fake.gh_json, fake.file_at
        args = argparse.Namespace(repo=REPO, owners=OWNER, into=self.tmp.name)
        return promote.self_update(args, log=lambda line: None)

    def test_the_owners_own_pull_request_updates_the_code(self):
        self.assertTrue(self.update(OWNER))
        self.assertEqual(Path(self.tmp.name, "promote.py").read_text(), "new tools/promote.py")

    def test_a_commit_by_anyone_else_keeps_the_old_code(self):
        self.assertFalse(self.update("a-collaborator"))
        self.assertEqual(os.listdir(self.tmp.name), [])


class Hosts(unittest.TestCase):
    def test_a_shared_suffix_is_not_the_same_site(self):
        self.assertFalse(promote.same_site("attacker.s3.amazonaws.com", "data.s3.amazonaws.com"))
        self.assertTrue(promote.same_site("ndownloader.figshare.com", "figshare.com"))
        self.assertTrue(promote.same_site("zenodo.org", "zenodo.org"))

    def test_a_restricted_licence_needs_a_grant(self):
        rec = {"licence": "CC BY-NC 4.0", "status": "fetching", "history": []}
        self.assertTrue(promote.licence_problems(rec))


class RecordUpdate(unittest.TestCase):
    def test_the_record_moves_to_fetched(self):
        rec = {"id": "demo_set", "status": "fetching", "history": [], "obstacles": ["x"], "next": "y"}
        man = {"id": "demo_set", "files": [{}], "bytes_total": 5}
        text = promote.updated_record(rec, man, "/rs/shared/datasets", "42")
        after = json.loads(text)
        self.assertEqual(after["status"], "fetched")
        self.assertEqual(after["grid_path"], "/rs/shared/datasets/demo_set/raw")
        self.assertEqual(after["history"][-1]["step"], "fetched")
        self.assertEqual(after["obstacles"], [])
        text.encode("ascii")


if __name__ == "__main__":
    unittest.main()
