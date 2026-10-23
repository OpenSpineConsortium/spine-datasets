"""The census (tools/census.py): the counts read under the records' own names, the tier a pair
takes from its status, the fold that carries an unchanged record without reading it again, the
three files it writes, and the check that refuses census fields that do not hold together."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import census  # noqa: E402
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
        "counts": {"films": 10},
        "history": [{"date": "2026-10-01", "step": "researched", "note": "found"}],
        "obstacles": [],
        "next": "a grid job",
    }
    base.update(fields)
    return base


def pairing(**fields):
    base = {"spine": True, "region": "lumbar", "xray": "ten frames", "ct": "one CT each", "subjects": "ten people",
            "pose": "stored", "masks": "none", "annotate": "body masks", "pair_key": "the case number"}
    base.update(fields)
    return base


def issue(number, body, labels=(), state="open"):
    return {
        "number": number,
        "html_url": f"https://github.com/o/r/issues/{number}",
        "title": f"Task {number}",
        "body": body,
        "state": state,
        "labels": [{"name": name} for name in labels],
    }


class CountsTest(unittest.TestCase):
    def test_the_records_own_names_are_read_as_the_standard_keys(self):
        counts, unread = census.counts_of(record(counts={"patients": 42, "films": 300, "cts": 40, "size_gb": 1.5,
                                                         "devices": 7}))
        self.assertEqual(counts, {"subjects": 42, "xray_images": 300, "videos": None, "ct_volumes": 40,
                                  "bytes": 1500000000})
        self.assertEqual(unread, ["devices"])

    def test_the_standard_key_wins_over_an_alias(self):
        counts, _ = census.counts_of(record(counts={"xray_images": 5, "frames": 900}))
        self.assertEqual(counts["xray_images"], 5)

    def test_a_ct_sets_images_are_slices_not_xrays(self):
        counts, unread = census.counts_of(record(group="ct", counts={"images": 50000, "cts": 100}))
        self.assertIsNone(counts["xray_images"])
        self.assertEqual(counts["ct_volumes"], 100)
        self.assertIn("images", unread)

    def test_videos_count_once_whatever_their_frames(self):
        counts, _ = census.counts_of(record(group="video", counts={"clips": 4}))
        self.assertEqual(counts["videos"], 4)

    def test_a_note_or_a_flag_is_no_count(self):
        counts, _ = census.counts_of(record(counts={"subjects": "about 50", "films": True}))
        self.assertIsNone(counts["subjects"])
        self.assertIsNone(counts["xray_images"])

    def test_the_licence_kind(self):
        self.assertEqual(census.licence_kind("CC BY 4.0"), "open")
        self.assertEqual(census.licence_kind("CC BY-NC 4.0"), "restricted")
        self.assertEqual(census.licence_kind("PhysioNet Credentialed Health Data License"), "restricted")
        self.assertEqual(census.licence_kind("not recorded"), "unknown")
        self.assertEqual(census.licence_kind(""), "unknown")

    def test_the_size_on_the_grid_is_what_the_landing_pass_measured(self):
        self.assertEqual(census.grid_bytes(record(measured={"bytes": 123})), 123)
        landed = record(status="fetched", result="2026-10-21: on the grid, 1 files, 3076112179 bytes, sha256-checked")
        self.assertEqual(census.grid_bytes(landed), 3076112179)
        self.assertIsNone(census.grid_bytes(record(result="a plan to fetch 10 bytes")))


class TierTest(unittest.TestCase):
    def tier(self, **fields):
        return census.row_of(record(pairing=pairing(), **fields))["tier"]

    def test_a_pair_takes_its_tier_from_its_status(self):
        self.assertEqual(self.tier(status="fetched"), "A")
        self.assertEqual(self.tier(status="held", grid_path="/data/set"), "A")
        self.assertEqual(self.tier(), "B")
        self.assertEqual(self.tier(status="granted"), "B")
        self.assertEqual(self.tier(route="letter", status="requested"), "C")
        self.assertEqual(self.tier(route="agreement", status="needs-owner"), "C")
        self.assertEqual(self.tier(status="refused"), "D")
        self.assertEqual(self.tier(reach="embargoed"), "D")

    def test_a_pair_of_something_else_is_tier_e_whatever_its_status(self):
        row = census.row_of(record(status="fetched", pairing=pairing(spine=False)))
        self.assertEqual(row["tier"], "E")

    def test_a_record_with_no_pairing_has_no_tier(self):
        row = census.row_of(record())
        self.assertFalse(row["paired"])
        self.assertIsNone(row["tier"])

    def test_held_is_on_the_grid(self):
        row = census.row_of(record(status="held", grid_path="/data/set"))
        self.assertEqual(row["stage"], "held")
        self.assertTrue(row["on_grid"])


class FoldTest(unittest.TestCase):
    def records(self):
        return [record(), record(id="second_set", name="A second set", group="ct", counts={"cts": 5},
                                 history=[{"date": "2026-09-30", "step": "researched", "note": "found"}])]

    def test_the_first_run_starts_the_census(self):
        folded, tally = census.fold(None, self.records(), "2026-10-23")
        self.assertEqual(tally, {"new": 2, "changed": 0, "carried": 0, "removed": 0})
        self.assertEqual([event["kind"] for event in folded["events"]], ["started"])
        self.assertEqual(folded["records"]["second_set"]["first_seen"], "2026-09-30")
        self.assertEqual(folded["records"]["example_set"]["last_changed"], "2026-10-23")

    def test_an_unchanged_record_is_carried_and_never_read_again(self):
        first, _ = census.fold(None, self.records(), "2026-10-23")
        with mock.patch.object(census, "row_of", side_effect=AssertionError("read again")):
            second, tally = census.fold(first, self.records(), "2026-10-24")
        self.assertEqual(tally, {"new": 0, "changed": 0, "carried": 2, "removed": 0})
        self.assertEqual(second["records"], first["records"])
        self.assertEqual(second["events"], first["events"])

    def test_a_reformatted_record_is_the_same_record(self):
        one = record()
        reordered = dict(reversed(list(one.items())))
        self.assertEqual(census.digest_of(one), census.digest_of(reordered))

    def test_a_changed_record_is_read_again_and_the_log_says_what_moved(self):
        first, _ = census.fold(None, [record(pairing=pairing())], "2026-10-23")
        moved = record(pairing=pairing(), status="fetched", counts={"films": 12},
                       history=record()["history"] + [{"date": "2026-10-24", "step": "fetched", "note": "landed"}])
        second, tally = census.fold(first, [moved], "2026-10-24")
        self.assertEqual(tally["changed"], 1)
        entry = second["records"]["example_set"]
        self.assertEqual(entry["first_seen"], "2026-10-01")
        self.assertEqual(entry["last_changed"], "2026-10-24")
        event = second["events"][-1]
        self.assertEqual((event["date"], event["id"], event["kind"]), ("2026-10-24", "example_set", "changed"))
        self.assertEqual(event["changes"]["status"], ["todo", "fetched"])
        self.assertEqual(event["changes"]["xray_images"], [10, 12])
        self.assertEqual(event["changes"]["tier"], ["B", "A"])

    def test_an_edit_that_moves_nothing_tracked_refreshes_the_row_quietly(self):
        first, _ = census.fold(None, [record()], "2026-10-23")
        second, tally = census.fold(first, [record(next="a letter")], "2026-10-24")
        self.assertEqual(tally["changed"], 1)
        self.assertEqual(second["records"]["example_set"]["row"]["next"], "a letter")
        self.assertEqual(len(second["events"]), 1)

    def test_records_added_and_removed_are_logged(self):
        first, _ = census.fold(None, [record()], "2026-10-23")
        newer = [record(id="third_set", name="A third set")]
        second, tally = census.fold(first, newer, "2026-10-24")
        self.assertEqual((tally["new"], tally["removed"]), (1, 1))
        kinds = [(event["id"], event["kind"]) for event in second["events"][1:]]
        self.assertEqual(kinds, [("third_set", "added"), ("example_set", "removed")])
        self.assertEqual(second["records"]["third_set"]["first_seen"], "2026-10-24")
        self.assertNotIn("example_set", second["records"])

    def test_new_rules_derive_every_row_afresh_with_one_event(self):
        first, _ = census.fold(None, self.records(), "2026-10-23")
        first["rules"] = census.RULES - 1
        second, tally = census.fold(first, self.records(), "2026-10-24")
        self.assertEqual(tally["changed"], 2)
        self.assertEqual(second["rules"], census.RULES)
        self.assertEqual([event["kind"] for event in second["events"]], ["started", "rules"])

    def test_anything_but_a_census_starts_afresh(self):
        folded, tally = census.fold({"message": "Not Found"}, self.records(), "2026-10-23")
        self.assertEqual(tally["new"], 2)
        self.assertEqual([event["kind"] for event in folded["events"]], ["started"])


class FileTest(unittest.TestCase):
    def data(self):
        records = [
            record(status="held", grid_path="/data/a", pairing=pairing(priority=1), measured={"bytes": 2 * 10 ** 9},
                   counts={"subjects": 10, "films": 10, "cts": 10}),
            record(id="wanted_set", name="A wanted set", route="letter", status="requested",
                   pairing=pairing(pair_key="")),
            record(id="phantom_set", name="A phantom set", status="fetched", grid_path="/data/c",
                   pairing=pairing(spine=False)),
            record(id="plain_set", name="A plain set", licence="to confirm on the page", counts={}),
        ]
        issues = [
            issue(7, "Record: datasets/example_set.json", ["todo"]),
            issue(8, "Record: datasets/missing_pair.json", ["todo", "paired"]),
            issue(9, "Record: datasets/missing_set.json", ["todo"]),
            issue(10, "Record: datasets/closed_set.json", ["todo"], state="closed"),
        ]
        folded, _ = census.fold(None, records, "2026-10-23")
        tasks, pending = census.tasks_of(issues, records)
        return census.census_file(folded, tasks, pending, "2026-10-23")

    def test_the_totals(self):
        totals = self.data()["totals"]
        self.assertEqual(totals["datasets"], 4)
        self.assertEqual(totals["on_grid"], 2)
        self.assertEqual(totals["by_stage"]["held"], 1)
        self.assertEqual(totals["paired"], {"A": 1, "B": 0, "C": 1, "D": 0, "E": 1})
        self.assertEqual(totals["paired_spine_subjects_on_grid"]["sum"], 10)
        self.assertEqual(totals["on_grid_size"]["measured"], 1)

    def test_tasks_and_pending_tasks(self):
        data = self.data()
        self.assertEqual(data["tasks"], {"example_set": 7})
        self.assertEqual([(task["number"], task["paired"]) for task in data["pending_tasks"]], [(8, True), (9, False)])

    def test_the_gaps_name_what_each_record_lacks(self):
        rows = census.rows_in_order({"records": self.data()["records"]})
        found = census.gaps(rows)
        self.assertIn(("phantom_set", "on the grid with no size: write the landing pass's bytes into measured"), found)
        self.assertTrue(any(ident == "plain_set" and "no count" in text for ident, text in found))
        self.assertTrue(any(ident == "plain_set" and "licence" in text for ident, text in found))
        self.assertTrue(any(ident == "wanted_set" and "pair_key" in text for ident, text in found))

    def test_same_ignores_only_the_day(self):
        data = self.data()
        later = dict(data, generated="2026-10-24")
        self.assertTrue(census.same(data, later))
        self.assertFalse(census.same(data, dict(later, tasks={})))

    def test_markdown(self):
        text = census.render_markdown(self.data(), "o/r")
        self.assertIn("## Paired CT and X-ray", text)
        self.assertIn("### A. On the grid (1)", text)
        self.assertIn("[#8](https://github.com/o/r/issues/8)", text)
        self.assertIn("the census began with 4 records", text)
        self.assertIn("https://github.com/o/r/issues/7", text)

    def test_html(self):
        text = census.render_html(self.data(), "o/r")
        self.assertIn("<title>Spine Data Census</title>", text)
        self.assertIn('id="f-stage"', text)
        self.assertIn('data-stage="held"', text)
        self.assertIn("A phantom set", text)
        self.assertNotIn("<script>alert", census.render_html(
            {**self.data(), "generated": "<script>alert(1)</script>"}, "o/r"))
        self.assertTrue(text.isascii())


class CheckTest(unittest.TestCase):
    def test_the_repository_records_pass(self):
        self.assertEqual(census.problems(pipeline.load_records()), [])

    def test_a_bad_pairing_and_bad_counts_are_named(self):
        bad = record(pairing={"spine": "yes", "region": "", "priority": 0, "colour": "red"},
                     counts={"subjects": "ten"}, measured=[1])
        text = "\n".join(census.problems([bad]))
        self.assertIn("pairing.spine must be true or false", text)
        self.assertIn("pairing.region must be a line of text", text)
        self.assertIn("pairing.priority must be a whole number from 1", text)
        self.assertIn("pairing.colour is not one of", text)
        self.assertIn("counts.subjects must be a number", text)
        self.assertIn("measured must be an object", text)

    def test_a_good_pairing_passes(self):
        self.assertEqual(census.problems([record(pairing=pairing(priority=2))]), [])


class CommandTest(unittest.TestCase):
    def run_census(self, *args):
        return subprocess.run([sys.executable, str(ROOT / "tools" / "census.py"), *args],
                              capture_output=True, text=True, check=False)

    def test_render_twice_carries_every_record_and_same_says_so(self):
        with tempfile.TemporaryDirectory() as folder:
            first, second = Path(folder) / "first", Path(folder) / "second"
            run = self.run_census("render", "--out", str(first), "--date", "2026-10-23")
            self.assertEqual(run.returncode, 0, run.stderr)
            for name in ("census.json", "CENSUS.md", "census.html"):
                self.assertTrue((first / name).exists(), name)
            run = self.run_census("render", "--out", str(second), "--previous", str(first / "census.json"),
                                  "--date", "2026-10-24")
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertIn(" 0 new, 0 changed,", run.stdout)
            same = self.run_census("same", str(first / "census.json"), str(second / "census.json"))
            self.assertEqual(same.returncode, 0)
            ledger = json.loads((second / "census.json").read_text(encoding="ascii"))
            self.assertEqual(ledger["generated"], "2026-10-24")


if __name__ == "__main__":
    unittest.main()
