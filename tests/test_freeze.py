"""The freeze (tools/freeze.py): one tree hash for every name and byte, folders' totals read back
without the data, a verify that names what moved, a requeued freeze that carries on, and the
public copy and its check against the record."""

import gzip
import hashlib
import json
import os
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import freeze  # noqa: E402


def write(top, path, data):
    full = os.path.join(top, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "wb") as handle:
        handle.write(data)


class FreezeTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.top = os.path.join(self.tmp.name, "demo_set")
        write(self.top, "raw/sub-01/a.nii.gz", b"alpha")
        write(self.top, "raw/sub-01/b.dcm", b"beta-beta")
        write(self.top, "raw/sub-02/c.dcm", b"c")
        write(self.top, "README.txt", b"read me")

    def tearDown(self):
        for folder, _, files in os.walk(self.tmp.name):
            os.chmod(folder, 0o755)
            for name in files:
                os.chmod(os.path.join(folder, name), 0o644)
        self.tmp.cleanup()

    def test_the_totals_and_the_tree_hash(self):
        summary = freeze.freeze(self.top, "demo_set")
        self.assertEqual(summary["files"], 4)
        self.assertEqual(summary["bytes"], 5 + 9 + 1 + 7)
        with gzip.open(os.path.join(self.top, freeze.FILE_LIST), "rb") as handle:
            listing = handle.read()
        self.assertEqual(hashlib.sha256(listing).hexdigest(), summary["tree_sha256"])
        self.assertEqual(listing.decode().splitlines()[0].split("\t")[2], "README.txt")
        raw = [row for row in summary["folders"] if row["path"] == "raw"][0]
        self.assertEqual((raw["files"], raw["bytes"]), (3, 15))
        self.assertEqual(summary["extensions"][".nii.gz"], {"files": 1, "bytes": 5})
        self.assertEqual(summary["shape"], [{"depth": 1, "folders": 1, "files": 1},
                                            {"depth": 2, "folders": 2, "files": 0},
                                            {"depth": 3, "folders": 0, "files": 3}])
        self.assertEqual(stat.S_IMODE(os.stat(os.path.join(self.top, freeze.SUMMARY)).st_mode), 0o444)

    def test_one_tree_gives_one_hash_wherever_it_is(self):
        first = freeze.freeze(self.top, "demo_set")
        other = os.path.join(self.tmp.name, "copy")
        for path in ("raw/sub-01/a.nii.gz", "raw/sub-01/b.dcm", "raw/sub-02/c.dcm", "README.txt"):
            write(other, path, Path(self.top, path).read_bytes())
        second = freeze.freeze(other, "demo_set", workers=2)
        self.assertEqual(first["tree_sha256"], second["tree_sha256"])
        self.assertEqual(Path(self.top, freeze.FILE_LIST).read_bytes(), Path(other, freeze.FILE_LIST).read_bytes())

    def test_a_subtree_keeps_its_hash_when_moved(self):
        summary = freeze.freeze(self.top, "demo_set", depth=3)
        moved = os.path.join(self.tmp.name, "moved")
        write(moved, "x/a.nii.gz", b"alpha")
        write(moved, "x/b.dcm", b"beta-beta")
        again = freeze.freeze(moved, "moved_set", depth=1)
        one = [row for row in summary["folders"] if row["path"] == "raw/sub-01"][0]
        self.assertEqual(one["tree_sha256"], again["folders"][0]["tree_sha256"])

    def test_a_rename_or_one_changed_byte_changes_the_hash(self):
        before = freeze.freeze(self.top, "demo_set")["tree_sha256"]
        write(self.top, "raw/sub-02/c.dcm", b"C")
        changed = freeze.freeze(self.top, "demo_set")["tree_sha256"]
        os.rename(os.path.join(self.top, "README.txt"), os.path.join(self.top, "README.md"))
        renamed = freeze.freeze(self.top, "demo_set")["tree_sha256"]
        self.assertEqual(len({before, changed, renamed}), 3)

    def test_what_is_written_beside_the_data_is_not_the_data(self):
        write(self.top, "PROMOTED.json", b"{}")
        write(self.top, ".incoming-7/raw/partial.zip", b"half")
        summary = freeze.freeze(self.top, "demo_set")
        again = freeze.freeze(self.top, "demo_set")
        self.assertEqual(summary["files"], 4)
        self.assertEqual(summary["tree_sha256"], again["tree_sha256"])

    def test_a_link_is_listed_not_followed(self):
        os.symlink("/etc", os.path.join(self.top, "raw", "outside"))
        summary = freeze.freeze(self.top, "demo_set")
        self.assertEqual((summary["files"], summary["links"], summary["bytes"]), (5, 1, 22))

    def test_verify_names_what_moved(self):
        freeze.freeze(self.top, "demo_set")
        self.assertEqual(freeze.verify(self.top), [])
        os.chmod(os.path.join(self.top, "raw", "sub-02"), 0o755)
        write(self.top, "raw/sub-02/c.dcm", b"x")
        write(self.top, "raw/sub-02/new.dcm", b"new")
        os.remove(os.path.join(self.top, "raw", "sub-01", "b.dcm"))
        self.assertEqual(freeze.verify(self.top, quick=True),
                         ["missing: raw/sub-01/b.dcm", "added: raw/sub-02/new.dcm"])
        self.assertEqual(freeze.verify(self.top),
                         ["missing: raw/sub-01/b.dcm", "added: raw/sub-02/new.dcm", "changed: raw/sub-02/c.dcm"])

    def test_the_freeze_can_be_written_elsewhere(self):
        out = os.path.join(self.tmp.name, "out")
        os.makedirs(out)
        os.chmod(self.top, 0o555)
        summary = freeze.freeze(self.top, "demo_set", out=out)
        self.assertEqual(summary["files"], 4)
        self.assertEqual(freeze.verify(self.top, out=out), [])

    def test_a_requeued_freeze_carries_on_from_its_checkpoint(self):
        found = freeze.walk(self.top)
        partial = freeze.hashed(self.top, found[:2])
        self.assertEqual(len(partial), 2)
        read = []
        original = freeze.hash_one
        freeze.hash_one = lambda item: read.append(item[0]) or original(item)
        try:
            summary = freeze.freeze(self.top, "demo_set")
        finally:
            freeze.hash_one = original
        self.assertEqual(sorted(read), sorted(path for path, _a, _i in found[2:]))
        self.assertFalse(os.path.exists(os.path.join(self.top, freeze.CHECKPOINT)))
        self.assertEqual(summary["tree_sha256"], freeze.freeze(self.top, "demo_set")["tree_sha256"])

    def test_what_a_caller_has_just_hashed_is_not_read_again(self):
        known = {"raw/sub-02/c.dcm": (hashlib.sha256(b"c").hexdigest(), 1)}
        read = []
        original = freeze.hash_one
        freeze.hash_one = lambda item: read.append(item[0]) or original(item)
        try:
            freeze.freeze(self.top, "demo_set", known=known)
        finally:
            freeze.hash_one = original
        self.assertNotIn("raw/sub-02/c.dcm", read)
        self.assertEqual(len(read), 3)

    def test_show_reads_any_folder_from_the_list(self):
        summary = freeze.freeze(self.top, "demo_set")
        rows = freeze.show_rows(summary, freeze.read_file_list(self.top), "raw", 1)
        self.assertEqual(rows, [("raw", 3, 15), ("raw/sub-01", 2, 14), ("raw/sub-02", 1, 1)])

    def test_the_measured_block(self):
        summary = freeze.freeze(self.top, "demo_set")
        block = freeze.measured_of(summary)
        self.assertEqual(set(block), {"bytes", "files", "tree_sha256", "frozen", "by"})


class RepositoryCopy(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = self.tmp.name
        data = os.path.join(self.root, "data")
        write(data, "raw/patient-0001/a.dcm", b"a")
        self.summary = freeze.freeze(data, "demo_set")
        os.makedirs(os.path.join(self.root, "frozen"))
        os.makedirs(os.path.join(self.root, "datasets"))
        self.copy = freeze.public_copy(self.summary)
        Path(self.root, "frozen", "demo_set.json").write_bytes(freeze.summary_bytes(self.copy))

    def tearDown(self):
        for folder, _, files in os.walk(self.tmp.name):
            os.chmod(folder, 0o755)
            for name in files:
                os.chmod(os.path.join(folder, name), 0o644)
        self.tmp.cleanup()

    def record(self, measured):
        Path(self.root, "datasets", "demo_set.json").write_text(json.dumps({"id": "demo_set", "measured": measured}))

    def test_the_public_copy_names_nothing_below_the_top(self):
        text = Path(self.root, "frozen", "demo_set.json").read_text()
        self.assertNotIn("patient-0001", text)
        self.assertNotIn(self.root, text)
        self.assertEqual([row["path"] for row in self.copy["folders"]], ["raw"])

    def test_a_name_with_a_dot_shows_no_end_and_many_top_folders_no_names(self):
        data = os.path.join(self.root, "many")
        for number in range(freeze.MAX_PUBLIC_FOLDERS + 1):
            write(data, "subject-%02d/Jane.Doe" % number, b"x")
        copy = freeze.public_copy(freeze.freeze(data, "many_set"))
        self.assertEqual(copy["folders"], [])
        self.assertEqual(copy["extensions"], {"(other)": {"files": 13, "bytes": 13}})
        self.assertEqual(freeze.summary_problems(copy, "many_set"), [])

    def test_the_record_must_agree_with_its_freeze(self):
        self.record(freeze.measured_of(self.summary))
        self.assertEqual(freeze.check_repository(self.root), [])
        self.record(dict(freeze.measured_of(self.summary), bytes=2))
        self.assertTrue(any("measured.bytes" in p for p in freeze.check_repository(self.root)))

    def test_a_copy_with_names_or_no_record_fails(self):
        self.record(freeze.measured_of(self.summary))
        Path(self.root, "frozen", "demo_set.json").write_bytes(freeze.summary_bytes(self.summary))
        self.assertTrue(any("public copy" in p for p in freeze.check_repository(self.root)))
        os.remove(os.path.join(self.root, "datasets", "demo_set.json"))
        self.assertTrue(any("no record" in p for p in freeze.check_repository(self.root)))

    def test_only_copies_that_pass_are_bundled_and_applied(self):
        back = os.path.join(self.root, "back")
        os.makedirs(back)
        Path(back, "demo_set.json").write_bytes(freeze.summary_bytes(self.copy))
        Path(back, "leaky_set.json").write_bytes(freeze.summary_bytes(dict(self.summary, id="leaky_set")))
        tree = freeze.bundle(back)["tree"]
        self.assertEqual([entry["path"] for entry in tree], ["frozen/demo_set.json"])
        self.assertNotIn("patient-0001", json.dumps(tree))
        os.remove(os.path.join(self.root, "frozen", "demo_set.json"))
        self.record({"bytes": 5, "note": "the landing pass"})
        self.assertEqual(freeze.apply_copies(back, self.root), ["demo_set"])
        measured = json.loads(Path(self.root, "datasets", "demo_set.json").read_text())["measured"]
        self.assertEqual(measured["note"], "the landing pass")
        self.assertEqual(measured["tree_sha256"], self.summary["tree_sha256"])
        self.assertEqual(freeze.check_repository(self.root), [])



class GridScript(unittest.TestCase):
    """grid/freeze.sh queues jobs through hpcworker, here a stand-in that prints what it was asked."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.home = os.path.join(self.tmp.name, "home")
        os.makedirs(os.path.join(self.home, "code"))
        root = Path(__file__).resolve().parent.parent
        for name in ("tools/freeze.py", "grid/freeze.sh"):
            Path(self.home, "code", os.path.basename(name)).write_bytes((root / name).read_bytes())
        plan = "".join("%s\t%s\t%s\n" % (ident, os.path.join(self.tmp.name, ident), size)
                       for ident, size in (("big", 800 * 10 ** 9), ("near", 102 * 10 ** 9), ("small", 3 * 10 ** 9),
                                           ("unknown", "-")))
        Path(self.home, "code", "freeze-plan.tsv").write_text(plan)
        for ident in ("big", "near", "small", "unknown"):
            write(self.tmp.name, ident + "/f.dcm", ident.encode())
        self.hpcw = os.path.join(self.tmp.name, "hpcw")
        Path(self.hpcw).write_text('echo "HPCW $*"\n')

    def tearDown(self):
        self.tmp.cleanup()

    def script(self, *args, job=None):
        env = dict(os.environ, FREEZE_HOME=self.home, HPCWORKER=self.hpcw, USER="someone")
        if job:
            env["SLURM_JOB_ID"] = job
        return subprocess.run(["bash", os.path.join(self.home, "code", "freeze.sh")] + list(args),
                              env=env, capture_output=True, text=True, check=True).stdout

    def shares(self, out):
        return [line.split(" run ")[1] for line in out.splitlines() if line.startswith("HPCW ")]

    def test_the_pilot_is_the_set_nearest_100_gb_and_start_takes_four_jobs(self):
        pilot = self.shares(self.script("pilot"))
        self.assertEqual([Path(p).read_text().split("\t")[0] for p in pilot], ["near"])
        start = self.shares(self.script("start"))
        self.assertEqual(len(start), 4)
        self.assertNotIn(pilot[0], start)
        self.assertEqual(Path(pilot[0]).read_text().split("\t")[0], "near")

    def test_a_job_freezes_its_share_and_start_skips_what_is_frozen(self):
        share = self.shares(self.script("pilot"))[0]
        self.script("run", share, job="7")
        measured = json.loads(Path(self.home, "measured", "near.json").read_text())
        self.assertEqual(measured["files"], 1)
        listed = " ".join(Path(p).read_text() for p in self.shares(self.script("start")))
        self.assertNotIn("near\t", listed)

    def test_report_sends_one_commit_of_the_public_copies(self):
        self.script("run", self.shares(self.script("pilot"))[0], job="7")
        bin_dir = os.path.join(self.tmp.name, "bin")
        os.makedirs(bin_dir)
        calls = os.path.join(self.tmp.name, "gh-calls")
        Path(bin_dir, "gh").write_text(
            '#!/bin/bash\necho "$*" >> %s\n'
            'case "$*" in *git/trees*) cat "${@: -3:1}" > %s.tree; echo %s;; *git/commits*) echo %s;;\n'
            '  *"git/ref/heads/"*) exit 1;; *) echo ok;; esac\n' % (calls, calls, "a" * 40, "b" * 40))
        os.chmod(os.path.join(bin_dir, "gh"), 0o755)
        env = dict(os.environ, FREEZE_HOME=self.home, HPCWORKER=self.hpcw, USER="someone",
                   PATH=bin_dir + os.pathsep + os.environ["PATH"])
        out = subprocess.run(["bash", os.path.join(self.home, "code", "freeze.sh"), "report"],
                             env=env, capture_output=True, text=True, check=True).stdout
        self.assertIn("reported 1 frozen sets to freeze-report at bbbbbbbbbbbb", out)
        tree = json.loads(Path(calls + ".tree").read_text())["tree"]
        self.assertEqual([entry["path"] for entry in tree], ["frozen/near.json"])
        self.assertIn("-X POST repos/OpenSpineConsortium/spine-datasets/git/refs -f ref=refs/heads/freeze-report",
                      Path(calls).read_text())


if __name__ == "__main__":
    unittest.main()
