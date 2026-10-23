"""The pipeline board (tools/pipeline.py): the stage of a record, the tasks read from the issues,
the two renderings, and the check that refuses a record whose pipeline fields do not hold
together."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import pipeline  # noqa: E402


def record(**fields):
    base = {
        "id": "example_set",
        "name": "An example set",
        "group": "films",
        "what": "ten films",
        "licence": "CC BY 4.0",
        "link": "https://example.org/set",
        "route": "download",
        "status": "todo",
        "history": [],
        "obstacles": [],
        "next": "a grid job",
    }
    base.update(fields)
    return base


def issue(number, body, labels=(), state="open"):
    return {
        "number": number,
        "html_url": f"https://github.com/o/r/issues/{number}",
        "body": body,
        "state": state,
        "labels": [{"name": name} for name in labels],
    }


class StageTest(unittest.TestCase):
    def test_status_and_route_give_the_stage(self):
        self.assertEqual(pipeline.stage_of(record(route="download")), "downloadable")
        self.assertEqual(pipeline.stage_of(record(route="letter")), "to-ask")
        self.assertEqual(pipeline.stage_of(record(status="requested")), "asked")
        self.assertEqual(pipeline.stage_of(record(status="granted")), "granted")
        self.assertEqual(pipeline.stage_of(record(status="fetching")), "fetching")
        self.assertEqual(pipeline.stage_of(record(status="fetched")), "on-grid")
        self.assertEqual(pipeline.stage_of(record(status="refused")), "refused")
        self.assertEqual(pipeline.stage_of(record(status="needs-owner")), "needs-owner")
        self.assertEqual(pipeline.stage_of(record(reach="embargoed")), "later")
        self.assertEqual(pipeline.stage_of(record(status="held", reach="embargoed")), "held")

    def test_every_stage_has_a_column(self):
        keys = {key for key, _, _ in pipeline.STAGES}
        for status in pipeline.STATUSES:
            self.assertIn(pipeline.stage_of(record(status=status)), keys)


class TasksTest(unittest.TestCase):
    def test_tasks_are_found_by_the_record_line(self):
        issues = [
            issue(7, "Obtain it.\n\nRecord: datasets/example_set.json", ["todo"]),
            issue(8, "no record line here"),
            issue(9, "Record: datasets/other_set.json", ["claimed", "worker:someone"]),
            issue(10, "Record: datasets/third_set.json", ["todo", "worker:someone"]),
            dict(issue(11, "Record: datasets/example_set.json"), pull_request={}),
        ]
        tasks = pipeline.tasks_by_id(issues)
        self.assertEqual(set(tasks), {"example_set", "other_set", "third_set"})
        self.assertEqual(tasks["example_set"]["number"], 7)
        self.assertEqual(tasks["other_set"]["holder"], "someone")
        self.assertEqual(tasks["third_set"]["holder"], "")
        self.assertEqual(tasks["third_set"]["given_to"], "someone")

    def test_holder_text(self):
        self.assertEqual(pipeline.holder_text(record(), {"holder": "a", "given_to": ""}), "a")
        self.assertEqual(pipeline.holder_text(record(), {"holder": "", "given_to": "b"}), "given to b")
        self.assertEqual(pipeline.holder_text(record(route="account"), None), "the owner")
        self.assertEqual(pipeline.holder_text(record(), None), "")


class RenderTest(unittest.TestCase):
    def items(self):
        records = [
            record(),
            record(id="asked_set", name="An asked set", route="letter", status="requested",
                   history=[{"date": "2026-10-01", "step": "asked", "note": "letter sent"}],
                   obstacles=["no answer yet"], next="wait"),
        ]
        issues = [issue(7, "Record: datasets/example_set.json", ["todo"])]
        return pipeline.cards(records, issues, "o/r", letters={"asked_set"})

    def test_markdown_names_every_dataset_and_its_links(self):
        text = pipeline.render_markdown(self.items(), "2026-10-21", "o/r")
        self.assertIn("An example set", text)
        self.assertIn("An asked set", text)
        self.assertIn("https://github.com/o/r/issues/7", text)
        self.assertIn("letters/asked_set.md", text)
        self.assertIn("no answer yet", text)
        self.assertIn("2026-10-21", text)

    def test_html_carries_the_data_and_no_script_breaks(self):
        text = pipeline.render_html(self.items(), "2026-10-21", "o/r")
        self.assertIn('<script id="data" type="application/json">', text)
        self.assertIn("An asked set", text)
        self.assertNotIn("</script>", json.dumps("x</script>y").replace("</", "<\\/"))
        self.assertTrue(text.isascii(), "the page is ASCII, since the docs site holds it to that")

    def test_render_command_writes_both_files(self):
        with tempfile.TemporaryDirectory() as folder:
            issues = Path(folder) / "issues.json"
            issues.write_text("[]", encoding="utf-8")
            run = subprocess.run(
                [sys.executable, str(ROOT / "tools" / "pipeline.py"), "render", "--out", folder,
                 "--issues", str(issues), "--date", "2026-10-21"],
                capture_output=True, text=True, check=False)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertTrue((Path(folder) / "PIPELINE.md").exists())
            self.assertTrue((Path(folder) / "pipeline.html").exists())


class CheckTest(unittest.TestCase):
    def test_the_repository_records_pass(self):
        self.assertEqual(pipeline.problems(pipeline.load_records()), [])

    def test_a_bad_record_is_named(self):
        bad = record(route="phone", status="done", history=[{"date": "yesterday"}], obstacles="x", next=None)
        found = pipeline.problems([bad], letters=set())
        text = "\n".join(found)
        self.assertIn("route 'phone'", text)
        self.assertIn("status 'done'", text)
        self.assertIn("needs a date", text)
        self.assertIn("obstacles must be a list", text)
        self.assertIn("next must be a string", text)

    def test_a_status_needs_a_dated_step_and_a_letter_to_send_needs_its_text(self):
        found = pipeline.problems([record(status="requested")], letters=set())
        self.assertTrue(any("no history entry" in line for line in found))
        found = pipeline.problems([record(route="letter")], letters=set())
        self.assertTrue(any("no letters/example_set.md" in line for line in found))
        self.assertEqual(pipeline.problems([record(route="letter")], letters={"example_set"}), [])

    def test_held_says_when_and_where(self):
        found = pipeline.problems([record(status="held")], letters=set())
        self.assertTrue(any("no history entry" in line for line in found))
        self.assertTrue(any("status held with no grid_path" in line for line in found))
        held = record(status="held", grid_path="/rs/rs_grp_oschome/go2432/data/example_set",
                      history=[{"date": "2026-10-23", "step": "held", "note": "on the grid"}])
        self.assertEqual(pipeline.problems([held], letters=set()), [])


if __name__ == "__main__":
    unittest.main()
