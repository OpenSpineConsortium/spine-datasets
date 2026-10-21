"""The automated review of dataset pull requests (tools/dataset_review.py)."""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import dataset_review  # noqa: E402
import promote  # noqa: E402

SHA = "a" * 64
GIT_QUIET = {
    "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.org", "GIT_COMMITTER_NAME": "t",
    "GIT_COMMITTER_EMAIL": "t@example.org", "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1",
}


def record(**changes):
    base = {
        "id": "demo_set", "name": "Demo", "group": "films", "licence": "CC BY 4.0",
        "link": "https://data.mendeley.com/datasets/abc", "route": "download", "status": "fetching",
        "history": [{"date": "2026-10-21", "step": "researched", "note": "found"}],
        "obstacles": [], "next": "", "grid_path": None, "result": "",
    }
    base.update(changes)
    return base


def manifest(**changes):
    base = {
        "id": "demo_set", "source": "https://data.mendeley.com/datasets/abc", "licence": "CC BY 4.0",
        "date": "2026-10-21", "bytes_total": 10,
        "files": [{"path": "raw/a.zip", "url": "https://data.mendeley.com/public-files/datasets/abc/files/1/file_downloaded",
                   "bytes": 10, "sha256": SHA}],
    }
    base.update(changes)
    return base


class ManifestRules(unittest.TestCase):
    def test_a_good_manifest_holds(self):
        self.assertEqual(promote.valid_manifest(manifest(), record(), "demo_set"), [])

    def test_licence_still_to_confirm_is_refused(self):
        rec = record(licence="CC BY 4.0 (to confirm on the page)")
        problems = promote.valid_manifest(manifest(licence=rec["licence"]), rec, "demo_set")
        self.assertTrue(any("to confirm" in problem for problem in problems))

    def test_closed_licence_needs_a_grant(self):
        rec = record(licence="by agreement")
        self.assertTrue(promote.valid_manifest(manifest(licence="by agreement"), rec, "demo_set"))
        rec["history"].append({"date": "2026-10-21", "step": "granted", "note": "yes"})
        self.assertEqual(promote.valid_manifest(manifest(licence="by agreement"), rec, "demo_set"), [])

    def test_source_must_be_the_records_link(self):
        problems = promote.valid_manifest(manifest(source="https://example.org/x"), record(), "demo_set")
        self.assertTrue(any("source" in problem for problem in problems))

    def test_file_rules(self):
        bad = manifest(bytes_total=10, files=[
            {"path": "raw/../etc/x", "url": "https://evil.example.org/x", "bytes": 10, "sha256": "zz"},
        ])
        text = " ".join(promote.valid_manifest(bad, record(), "demo_set"))
        for words in ("'..'", "evil.example.org", "sha256"):
            self.assertIn(words, text)

    def test_signed_links_are_refused(self):
        signed = manifest()
        signed["files"][0]["url"] += "?X-Amz-Signature=abc"
        self.assertTrue(any("token" in p for p in promote.valid_manifest(signed, record(), "demo_set")))

    def test_md5_may_stand_in_for_sha256(self):
        entry = {"path": "raw/a.zip", "url": "https://zenodo.org/api/records/1/files/a.zip/content",
                 "bytes": 10, "md5": "b" * 32}
        rec = record(link="https://zenodo.org/records/1")
        man = manifest(source=rec["link"], files=[entry])
        self.assertEqual(promote.valid_manifest(man, rec, "demo_set"), [])

    def test_sizes_must_add_up(self):
        problems = promote.valid_manifest(manifest(bytes_total=11), record(), "demo_set")
        self.assertTrue(any("bytes_total" in problem for problem in problems))


class MendeleyManifest(unittest.TestCase):
    def test_built_from_the_public_file_list(self):
        listing = [{"filename": "a.zip", "content_details": {
            "sha256_hash": SHA, "size": 10,
            "download_url": "https://data.mendeley.com/public-files/datasets/abc/files/1/file_downloaded"}}]
        built = dataset_review.build_manifest(record(), dataset_review.mendeley_files(listing), "2026-10-21")
        self.assertEqual(promote.valid_manifest(built, record(), "demo_set"), [])


class Words(unittest.TestCase):
    def test_banned_words_are_found(self):
        word = "mod" + "el"
        self.assertEqual(dataset_review.banned_words("the %s works" % word), [word])
        self.assertEqual(dataset_review.banned_words("A" + "I methods"), ["A" + "I"])
        self.assertEqual(dataset_review.banned_words("AIMI, constraint, modelling clay"[:12]), [])


class Diff(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        for folder in ("datasets", "manifests", "letters"):
            (self.root / folder).mkdir()
        self.write("datasets/demo_set.json", record(status="todo"))
        self.git("init", "-q", "-b", "main")
        self.git("add", "-A")
        self.git("commit", "-qm", "base")
        self.git("checkout", "-qb", "work")

    def tearDown(self):
        self.tmp.cleanup()

    def git(self, *args):
        env = dict(os.environ, **GIT_QUIET)
        subprocess.run(["git", *args], cwd=self.root, check=True, env=env, capture_output=True)

    def write(self, path, value):
        text = value if isinstance(value, str) else json.dumps(value, indent=1) + "\n"
        (self.root / path).write_text(text, encoding="ascii")

    def review(self, pull=None):
        self.git("add", "-A")
        self.git("commit", "-qm", "change")
        return dataset_review.check_tree(self.root, dataset_review.review_diff("main", root=self.root, pull=pull))

    def levels(self, report):
        return [level for level, _ in report.lines]

    def test_a_clean_fetch_pull_request_passes(self):
        rec = record()
        rec["history"].append({"date": "2026-10-21", "step": "fetching", "note": "manifest ready"})
        self.write("datasets/demo_set.json", rec)
        self.write("manifests/demo_set.json", manifest())
        report = self.review()
        self.assertFalse(report.failed(), report.text())

    def test_a_banned_word_in_a_letter_fails(self):
        self.write("letters/demo_set.md", "We will " + "tra" + "in on it.\n")
        self.assertTrue(self.review().failed())

    def test_history_only_grows(self):
        self.write("datasets/demo_set.json", record(status="todo", history=[]))
        self.assertTrue(self.review().failed())

    def test_a_data_file_fails(self):
        self.write("datasets/scan.png", "not really an image")
        self.assertTrue(self.review().failed())

    def test_binding_language_is_flagged_not_failed(self):
        self.write("letters/demo_set.md", "Dr Schwing signed the agreement.\n")
        report = self.review()
        self.assertIn("FLAG", self.levels(report))
        self.assertFalse(report.failed())

    def test_a_publishers_file_name_is_not_the_projects_words(self):
        rec = record()
        self.write("datasets/demo_set.json", rec)
        man = manifest()
        man["files"][0]["path"] = "raw/" + "tra" + "in.zip"
        man["files"][0]["url"] = "https://data.mendeley.com/public-files/" + "tra" + "in.zip"
        self.write("manifests/demo_set.json", man)
        report = self.review()
        self.assertFalse(report.failed(), report.text())

    def test_the_promoters_code_changes_only_by_the_owners_pull_request(self):
        (self.root / "tools").mkdir()
        self.write("tools/promote.py", "# changed\n")
        pull = {"user": {"login": "a-collaborator"}, "head": {"ref": "claude/5"}, "title": "t", "body": ""}
        self.assertTrue(self.review(pull).failed())

    def test_the_promoters_branch_changes_only_its_record(self):
        self.write("letters/other.md", "a note\n")
        pull = {"user": {"login": dataset_review.OWNERS[0]}, "head": {"ref": "promote/demo_set"},
                "title": "t", "body": ""}
        self.assertTrue(self.review(pull).failed())

    def test_fetched_needs_the_shared_path_and_a_manifest(self):
        self.write("datasets/demo_set.json", record(status="fetched", grid_path="/home/someone/raw"))
        self.assertTrue(self.review().failed())


if __name__ == "__main__":
    unittest.main()
