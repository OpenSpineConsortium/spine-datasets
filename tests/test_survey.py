"""tools/survey.py sizes a volume by folder and puts each folder in one kind; the folders here
carry no ceph.dir.rbytes, so every size is the files summed, as on a disk that is not CephFS."""

import gzip
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import survey  # noqa: E402


def put(path, size):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as handle:
        handle.write(b"x" * size)


class SurveyTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = os.path.join(self.tmp.name, "volume")
        r = self.root
        put(os.path.join(r, "go2432/data/known/imagesTr/a.nii.gz"), 600)
        put(os.path.join(r, "go2432/data/known/labelsTr/a.nii.gz"), 400)
        lines = b"0\t600\timagesTr/a.nii.gz\n0\t400\tlabelsTr/a.nii.gz\n"
        with gzip.open(os.path.join(r, "go2432/data/known", survey.FILE_LIST), "wb") as handle:
            handle.write(lines)
        put(os.path.join(r, "go2432/data/stray_set/case1.nii.gz"), 900)
        put(os.path.join(r, "go2432/data/tiny/x"), 5)
        put(os.path.join(r, "go2432/totalseg_out/b.nii.gz"), 700)
        put(os.path.join(r, "go2432/smoke/run1/epoch3.pt"), 800)
        put(os.path.join(r, "go2432/hpcworker/jobs/log.out"), 300)
        put(os.path.join(r, "go2432/notes/n.txt"), 200)
        put(os.path.join(r, "someone_else/private/secret.bin"), 1000)
        self.datasets = {os.path.join(r, "go2432/data/known"): "known_set"}

    def tearDown(self):
        self.tmp.cleanup()

    def table(self):
        return survey.Survey(self.root, self.datasets, floor=100, max_depth=4).run()

    def row(self, table, path):
        found = [row for row in table["rows"] if row["path"] == path and not row.get("folded")]
        self.assertEqual(len(found), 1, path)
        return found[0]

    def test_each_folder_lands_in_one_kind(self):
        table = self.table()
        known = self.row(table, "go2432/data/known")
        self.assertEqual((known["kind"], known["id"]), ("dataset", "known_set"))
        self.assertEqual(known["mask_bytes"], 400)
        self.assertEqual(known["image_bytes"], 600)
        self.assertEqual(self.row(table, "go2432/data/stray_set")["kind"], "untracked data")
        self.assertEqual(self.row(table, "go2432/totalseg_out")["kind"], "masks")
        self.assertEqual(self.row(table, "go2432/smoke/run1")["kind"], "runs and outputs")
        self.assertEqual(self.row(table, "go2432/hpcworker/jobs")["kind"], "jobs and logs")
        self.assertEqual(self.row(table, "go2432/notes")["kind"], "other")
        self.assertEqual(table["masks_in_datasets_bytes"], 400)

    def test_the_rows_add_up_to_the_volume_and_name_no_other_account(self):
        table = self.table()
        self.assertGreater(table["volume_bytes"], 0)
        self.assertEqual(sum(row["bytes"] for row in table["rows"]), table["volume_bytes"])
        self.assertEqual(table["volume_how"], "summed")
        others = [row for row in table["rows"] if row["kind"] == "other accounts"]
        self.assertEqual(others[0]["folders"], 1)
        self.assertEqual(others[0]["bytes"], 1000)
        self.assertNotIn("someone_else", json.dumps(table))

    def test_small_folders_fold_into_their_parent(self):
        table = self.table()
        folded = [row for row in table["rows"] if row.get("folded") and row["path"] == "go2432/data"]
        self.assertEqual(folded[0]["bytes"], 5)
        self.assertEqual(folded[0]["kind"], "untracked data")

    def test_the_command_writes_the_table_and_prints_the_kinds(self):
        plan = os.path.join(self.tmp.name, "plan.tsv")
        Path(plan).write_text("known_set\t%s\t1000\n" % os.path.join(self.root, "go2432/data/known"))
        out = os.path.join(self.tmp.name, "survey.json")
        run = subprocess.run([sys.executable, str(Path(survey.__file__)), "run", "--plan", plan, "--out", out,
                              "--root", self.root, "--floor-gb", "0.0000001"],
                             capture_output=True, text=True, check=True)
        self.assertIn("masks inside datasets", run.stdout)
        table = json.loads(Path(out).read_text())
        self.assertEqual(table["format"], survey.FORMAT)
        self.assertIn("untracked data", table["kinds"])


class GridWords(unittest.TestCase):
    """grid/storage.sh survey queues one read-only job, measure runs it, report carries it back."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.home = os.path.join(self.tmp.name, "home")
        os.makedirs(os.path.join(self.home, "code"))
        root = Path(__file__).resolve().parent.parent
        for name in ("tools/retire.py", "tools/freeze.py", "tools/survey.py", "grid/storage.sh"):
            Path(self.home, "code", os.path.basename(name)).write_bytes((root / name).read_bytes())
        self.volume = os.path.join(self.tmp.name, "volume")
        put(os.path.join(self.volume, "go2432/data/stray/a"), 50)
        Path(self.home, "code", "freeze-plan.tsv").write_text("")
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
                   SURVEY_ROOT=self.volume, SURVEY_FLOOR_GB="0.00000001", PATH=self.bin + os.pathsep + os.environ["PATH"])
        if job:
            env["SLURM_JOB_ID"] = job
        return subprocess.run(["bash", os.path.join(self.home, "code", "storage.sh")] + list(args),
                              env=env, capture_output=True, text=True, check=check)

    def test_survey_queues_one_job_and_report_carries_its_table(self):
        out = self.script("survey").stdout
        queued = [line for line in out.splitlines() if line.startswith("HPCW ")]
        self.assertEqual(len(queued), 1)
        self.assertTrue(queued[0].endswith("storage.sh measure"))
        self.assertNotEqual(self.script("measure", check=False).returncode, 0)
        self.script("measure", job="11")
        self.assertIn("survey:", self.script("status").stdout)
        self.assertIn("reported to storage-report", self.script("report").stdout)
        tree = json.loads(Path(self.calls + ".tree").read_text())["tree"]
        self.assertEqual([entry["path"] for entry in tree], ["storage/survey.json"])
        table = json.loads(tree[0]["content"])
        self.assertEqual(table["kinds"]["untracked data"], 50)

    def test_survey_refuses_without_its_code(self):
        os.remove(os.path.join(self.home, "code", "survey.py"))
        out = self.script("survey", check=False)
        self.assertEqual(out.returncode, 2)
        self.assertNotIn("HPCW ", out.stdout)


if __name__ == "__main__":
    unittest.main()
