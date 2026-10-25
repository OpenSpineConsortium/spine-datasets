"""tools/accounting.py: every record has a task, every folder of the data root a record or a task."""

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import accounting  # noqa: E402


class Accounting(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.datasets = self.tmp / "datasets"
        self.datasets.mkdir()
        self.ledger = self.tmp / "folders.json"

    def write(self, rid, **fields):
        (self.datasets / f"{rid}.json").write_text(json.dumps(dict(id=rid, status="held", **fields)), encoding="utf-8")

    def folders(self, **entries):
        self.ledger.write_text(json.dumps({"folders": entries}), encoding="utf-8")

    def problems(self):
        return accounting.problems(self.datasets, self.ledger)

    def test_a_record_with_no_task_is_a_problem(self):
        self.write("a", task=12)
        self.write("b")
        self.write("c", task="12")
        self.write("d", task=True)
        self.assertEqual(len(self.problems()), 3)
        self.assertIn("datasets/b.json", self.problems()[0])

    def test_a_folder_names_records_that_exist_or_carries_its_own_task(self):
        self.write("a", task=12)
        self.folders(bank={"kind": "records", "records": ["a"], "what": "the set"},
                     ready={"kind": "derived", "task": 300, "what": "frames built from a"})
        self.assertEqual(self.problems(), [])

    def test_a_folder_that_accounts_for_nothing_is_a_problem(self):
        self.write("a", task=12)
        self.folders(gone={"kind": "records", "records": ["missing"], "what": "x"},
                     loose={"kind": "derived", "what": "x"},
                     odd={"kind": "other", "task": 3, "what": "x"},
                     mute={"kind": "working", "task": 4, "what": " "})
        found = " ".join(self.problems())
        for word in ("no record datasets/missing.json", "loose: a folder no record holds", "odd: kind", "mute: says nothing"):
            self.assertIn(word, found)

    def test_no_ledger_checks_the_records_alone(self):
        self.write("a", task=1)
        self.assertEqual(self.problems(), [])

    def test_the_repository_is_accounted_for(self):
        self.assertEqual(accounting.problems(), [], "every record needs its task, every grid folder a record or a task")


if __name__ == "__main__":
    unittest.main()
