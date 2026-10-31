"""The retirement plan (tools/retire.py): it lists the images of a frozen set and keeps its
labels and metadata, and lists nothing when the folder, the freeze or the files are not the ones
the merged request names."""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import freeze  # noqa: E402
import retire  # noqa: E402


def write(top, path, data):
    full = os.path.join(top, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "wb") as handle:
        handle.write(data)


class RetireTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = os.path.realpath(self.tmp.name) + "/data/"
        self.top = self.root + "demo_set"
        write(self.top, "imagesTr/case_001.nii.gz", b"image-one")
        write(self.top, "imagesTr/case_002.nii.gz", b"image-two-")
        write(self.top, "labelsTr/case_001.nii.gz", b"lab")
        write(self.top, "dataset.json", b"{}")
        self.tree = freeze.freeze(self.top, "demo_set")["tree_sha256"]
        self.roots, retire.ROOTS = retire.ROOTS, (self.root,)
        self.out = os.path.join(self.tmp.name, "plans")

    def tearDown(self):
        retire.ROOTS = self.roots
        for folder, _, files in os.walk(self.tmp.name):
            os.chmod(folder, 0o755)
            for name in files:
                os.chmod(os.path.join(folder, name), 0o644)
        self.tmp.cleanup()

    def deleted(self):
        with open(os.path.join(self.out, "demo_set.delete"), "rb") as handle:
            return [p for p in handle.read().decode().split("\0") if p]

    def test_images_go_and_labels_stay(self):
        counts = retire.write_plan(self.top, "demo_set", self.tree, self.out)
        self.assertEqual(counts["problems"], [])
        self.assertEqual(self.deleted(), ["imagesTr/case_001.nii.gz", "imagesTr/case_002.nii.gz"])
        self.assertEqual((counts["files_to_delete"], counts["bytes_to_delete"]), (2, 19))
        self.assertEqual((counts["files_kept"], counts["bytes_kept"]), (2, 5))
        self.assertTrue(os.path.exists(os.path.join(self.top, "imagesTr/case_001.nii.gz")))

    def assert_refused(self, folder, tree, words):
        counts = retire.write_plan(folder, "demo_set", tree, self.out)
        self.assertTrue(any(words in problem for problem in counts["problems"]), counts["problems"])
        self.assertEqual(self.deleted(), [])
        self.assertNotIn(self.tmp.name, json.dumps(counts))

    def test_another_freeze_is_refused(self):
        self.assert_refused(self.top, "0" * 64, "not the one the request names")

    def test_a_file_added_since_the_freeze_is_refused(self):
        write(self.top, "imagesTr/case_003.nii.gz", b"new")
        self.assert_refused(self.top, self.tree, "1 files added")

    def test_a_folder_outside_the_roots_is_refused(self):
        self.assert_refused(os.path.realpath(self.tmp.name), self.tree, "none of the data roots")

    def test_the_root_itself_is_refused(self):
        self.assert_refused(self.root.rstrip("/") + "/", self.tree, "plain absolute path")

    def test_a_link_on_the_path_is_refused(self):
        os.symlink(self.top, self.root + "alias")
        self.assert_refused(self.root + "alias", self.tree, "link on its path")

    def test_a_root_reached_through_a_link_still_plans(self):
        mount = os.path.realpath(self.tmp.name) + "/mount"
        os.symlink(os.path.realpath(self.tmp.name), mount)
        retire.ROOTS = (mount + "/data/",)
        counts = retire.write_plan(mount + "/data/demo_set", "demo_set", self.tree, self.out)
        self.assertEqual(counts["problems"], [])
        self.assertEqual(counts["files_to_delete"], 2)

    def test_a_link_below_a_linked_root_is_refused(self):
        mount = os.path.realpath(self.tmp.name) + "/mount"
        os.symlink(os.path.realpath(self.tmp.name), mount)
        os.symlink(self.top, self.root + "alias")
        retire.ROOTS = (mount + "/data/",)
        self.assert_refused(mount + "/data/alias", self.tree, "link on its path")

    def retired(self):
        return retire.retire(self.top, "demo_set", self.tree, self.out, "20261024T210000Z")

    def test_delete_removes_what_the_plan_listed_and_keeps_the_rest(self):
        retire.write_plan(self.top, "demo_set", self.tree, self.out)
        record = self.retired()
        self.assertEqual(record["problems"], [])
        self.assertTrue(record["complete"])
        self.assertEqual((record["files_deleted_now"], record["bytes_deleted_now"]), (2, 19))
        self.assertFalse(os.path.exists(os.path.join(self.top, "imagesTr")))
        for kept in ("labelsTr/case_001.nii.gz", "dataset.json", "FROZEN.json", "FROZEN.files.tsv.gz", "RETIRED.json"):
            self.assertTrue(os.path.exists(os.path.join(self.top, kept)), kept)
        self.assertEqual([e["path"] for e in retire.bundle(self.out)["tree"]],
                         ["storage/retire/demo_set.json", "storage/retired/demo_set.json"])

    def test_delete_opens_a_read_only_folder_of_the_set(self):
        retire.write_plan(self.top, "demo_set", self.tree, self.out)
        images = os.path.join(self.top, "imagesTr")
        os.chmod(images, 0o555)
        record = self.retired()
        self.assertEqual(record["failure_reasons"], {})
        self.assertTrue(record["complete"])
        self.assertFalse(os.path.exists(images))

    def test_only_a_folder_lacking_the_write_bit_is_opened(self):
        labels = os.path.join(self.top, "labelsTr")
        os.chmod(labels, 0o555)
        self.assertTrue(retire.open_for_writing(self.top, "labelsTr"))
        self.assertEqual(os.stat(labels).st_mode & 0o777, 0o755)
        self.assertFalse(retire.open_for_writing(self.top, "labelsTr"))
        self.assertFalse(retire.open_for_writing(self.top, "dataset.json"))
        self.assertFalse(retire.open_for_writing(self.top, "no_such_folder"))

    def test_a_retirement_cut_short_carries_on(self):
        retire.write_plan(self.top, "demo_set", self.tree, self.out)
        os.unlink(os.path.join(self.top, "imagesTr/case_001.nii.gz"))
        record = self.retired()
        self.assertEqual(record["problems"], [])
        self.assertEqual(record["files_deleted_now"], 1)
        self.assertTrue(record["complete"])
        self.assertEqual(self.retired()["files_deleted_now"], 0)

    def test_delete_refuses_without_a_plan_or_with_a_kept_file_gone(self):
        self.assertEqual(self.retired()["problems"], ["the set has no plan to carry out"])
        retire.write_plan(self.top, "demo_set", self.tree, self.out)
        os.unlink(os.path.join(self.top, "labelsTr/case_001.nii.gz"))
        self.assertIn("1 files missing since the freeze", self.retired()["problems"])
        self.assertTrue(os.path.exists(os.path.join(self.top, "imagesTr/case_001.nii.gz")))

    def test_delete_refuses_a_list_the_checks_do_not_give(self):
        retire.write_plan(self.top, "demo_set", self.tree, self.out)
        with open(os.path.join(self.out, "demo_set.delete"), "ab") as handle:
            handle.write(b"labelsTr/case_001.nii.gz\0")
        self.assertEqual(self.retired()["problems"], ["the checks give another list than the plan's"])
        self.assertTrue(os.path.exists(os.path.join(self.top, "labelsTr/case_001.nii.gz")))

    def test_delete_refuses_a_plan_with_problems(self):
        retire.write_plan(self.top, "demo_set", "0" * 64, self.out)
        self.assertEqual(self.retired()["problems"], ["the plan is not this set's at this tree hash"])

    def test_the_bundle_carries_counts_alone(self):
        retire.write_plan(self.top, "demo_set", self.tree, self.out)
        body = retire.bundle(self.out)
        self.assertEqual([entry["path"] for entry in body["tree"]], ["storage/retire/demo_set.json"])
        self.assertNotIn("case_001", body["tree"][0]["content"])

    def test_actions_read_the_request(self):
        request = os.path.join(self.tmp.name, "request.json")
        with open(request, "w") as handle:
            json.dump({"format": "spine-datasets/storage-request 1", "actions": [
                {"kind": "retire", "id": "demo_set", "place": None, "folder": self.top, "tree_sha256": self.tree},
                {"kind": "fetch", "id": "other", "place": None}]}, handle)
        rows = retire.read_actions(request)
        self.assertEqual(rows[0], ["retire", "demo_set", "-", self.top, self.tree])
        self.assertEqual(rows[1], ["fetch", "other", "-", "-", "-"])


class GridScript(unittest.TestCase):
    """grid/storage.sh queues one planning job per merged request through hpcworker, here a
    stand-in that prints what it was asked, and carries the plans' counts back."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.home = os.path.join(self.tmp.name, "home")
        os.makedirs(os.path.join(self.home, "code", "requests"))
        root = Path(__file__).resolve().parent.parent
        for name in ("tools/retire.py", "tools/freeze.py", "grid/storage.sh"):
            Path(self.home, "code", os.path.basename(name)).write_bytes((root / name).read_bytes())
        self.stamp = "20261024T210000Z"
        Path(self.home, "code", "requests", self.stamp + ".json").write_text(json.dumps({
            "format": "spine-datasets/storage-request 1", "actions": [
                {"kind": "retire", "id": "old_set", "folder": os.path.join(self.tmp.name, "old_set"),
                 "tree_sha256": "0" * 64},
                {"kind": "fetch", "id": "new_set"}]}))
        self.hpcw = os.path.join(self.tmp.name, "hpcw")
        Path(self.hpcw).write_text('echo "HPCW $*"\n')
        self.bin = os.path.join(self.tmp.name, "bin")
        os.makedirs(self.bin)
        self.calls = os.path.join(self.tmp.name, "gh-calls")
        Path(self.bin, "gh").write_text(
            '#!/bin/bash\ncase "$*" in *git/trees*) cat "${@: -3:1}" > %s.tree; echo %s;; *git/commits*) echo %s;;\n'
            '  *"git/ref/heads/"*) exit 1;; *) echo ok;; esac\n' % (self.calls, "a" * 40, "b" * 40))
        os.chmod(os.path.join(self.bin, "gh"), 0o755)

    def tearDown(self):
        self.tmp.cleanup()

    def script(self, *args, job=None, check=True):
        env = dict(os.environ, STORAGE_DIR=self.home, HPCWORKER=self.hpcw, USER="someone",
                   PATH=self.bin + os.pathsep + os.environ["PATH"])
        if job:
            env["SLURM_JOB_ID"] = job
        return subprocess.run(["bash", os.path.join(self.home, "code", "storage.sh")] + list(args),
                              env=env, capture_output=True, text=True, check=check)

    def test_apply_queues_one_job_once_and_names_the_fetch_word(self):
        out = self.script("apply", self.stamp).stdout
        queued = [line for line in out.splitlines() if line.startswith("HPCW ")]
        self.assertEqual(len(queued), 1)
        self.assertTrue(queued[0].endswith("storage.sh plan " + self.stamp))
        self.assertIn("schwingnet-fetch-new_set", out)
        again = self.script("apply", self.stamp).stdout
        self.assertNotIn("HPCW ", again)
        self.assertNotEqual(self.script("apply", "../x", check=False).returncode, 0)

    def test_apply_plans_again_once_a_written_plan_was_refused(self):
        self.script("apply", self.stamp)
        self.script("plan", self.stamp, job="9", check=False)
        again = self.script("apply", self.stamp).stdout
        self.assertIn("planning it again", again)
        self.assertEqual(len([line for line in again.splitlines() if line.startswith("HPCW ")]), 1)

    def test_apply_does_not_plan_again_once_every_plan_lists_files(self):
        self.script("apply", self.stamp)
        plans = Path(self.home, "plans")
        (plans / "old_set.json").write_text('{"problems": []}')
        (plans / "old_set.delete").write_bytes(b"imagesTr/a.nii.gz\0")
        self.assertNotIn("HPCW ", self.script("apply", self.stamp).stdout)

    def test_the_job_writes_a_plan_and_report_carries_its_counts(self):
        job = self.script("plan", self.stamp, job="9", check=False)
        self.assertEqual(job.returncode, 1)
        counts = json.loads(Path(self.home, "plans", "old_set.json").read_text())
        self.assertEqual(counts["files_to_delete"], 0)
        self.assertTrue(counts["problems"])
        self.assertIn("reported to storage-report", self.script("report").stdout)
        tree = json.loads(Path(self.calls + ".tree").read_text())["tree"]
        self.assertEqual([entry["path"] for entry in tree], ["storage/retire/old_set.json"])

    def test_retire_queues_nothing_while_no_plan_lists_files(self):
        self.script("plan", self.stamp, job="9", check=False)
        out = self.script("retire", self.stamp, check=False)
        self.assertEqual(out.returncode, 1)
        self.assertNotIn("HPCW ", out.stdout)
        self.assertIn("old_set: no plan that lists files", out.stdout)

    def test_retire_queues_one_delete_job_once_a_plan_lists_files(self):
        plans = Path(self.home, "plans")
        plans.mkdir()
        (plans / "old_set.json").write_text('{"problems": []}')
        (plans / "old_set.delete").write_bytes(b"imagesTr/a.nii.gz\0")
        out = self.script("retire", self.stamp).stdout
        queued = [line for line in out.splitlines() if line.startswith("HPCW ")]
        self.assertEqual(len(queued), 1)
        self.assertTrue(queued[0].endswith("storage.sh delete " + self.stamp))
        job = self.script("delete", self.stamp, job="10", check=False)
        self.assertEqual(job.returncode, 1)
        self.assertIn("old_set: not retired", job.stdout)


if __name__ == "__main__":
    unittest.main()
