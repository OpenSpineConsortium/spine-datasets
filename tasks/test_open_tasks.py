"""The parser of tasks/open_tasks.py against tasks/TASKS.md and against a small text of its own.

Run with `python3 -m unittest tasks/test_open_tasks.py` from the repository root (or
`python3 -m unittest discover tasks`). No network, no token.
"""

import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))  # so the test runs from the repository root too

import open_tasks  # the path above makes the module importable

TASKS = HERE / "TASKS.md"
BANNED = ("neural network", "machine learning", "deep learning", " model ", " ai ", " training",
          " train ", "detector", "classifier")


class ParseTasks(unittest.TestCase):
    def test_small_text(self):
        text = "# head\n\nintro\n\n## Obtain A\n\nline one\nline two\n\n## Obtain B\nonly\n"
        self.assertEqual(open_tasks.parse_tasks(text),
                         [("Obtain A", "line one\nline two"), ("Obtain B", "only")])

    def test_no_heading_gives_nothing(self):
        self.assertEqual(open_tasks.parse_tasks("just prose\n"), [])

    def test_tasks_md(self):
        tasks = open_tasks.parse_tasks(TASKS.read_text())
        self.assertEqual(len(tasks), 90)
        titles = [title for title, _ in tasks]
        self.assertEqual(len(set(titles)), len(titles), "a title opens one issue, so no two are equal")
        for title, body in tasks:
            self.assertTrue(title.startswith("Obtain "), title)
            lines = body.splitlines()
            self.assertLessEqual(len(lines), 12, title)
            self.assertTrue(any(line.startswith("Files likely touched: datasets/") for line in lines), title)
            self.assertTrue(any(line.startswith("Link: ") for line in lines), title)
            self.assertTrue(any(line.startswith("Priority: group ") for line in lines), title)

    def test_tasks_md_names_every_record(self):
        ids = {path.stem for path in (HERE.parent / "datasets").glob("*.json")}
        touched = set()
        for _, body in open_tasks.parse_tasks(TASKS.read_text()):
            for line in body.splitlines():
                if line.startswith("Files likely touched: datasets/"):
                    touched.add(line.split("datasets/")[1].split(".json")[0])
        self.assertEqual(ids, touched)

    def test_issue_text_keeps_the_confidentiality_rule(self):
        text = TASKS.read_text().lower().replace("stoic2021-training", "stoic2021")
        for word in BANNED:
            self.assertNotIn(word, text, word)


if __name__ == "__main__":
    unittest.main()
