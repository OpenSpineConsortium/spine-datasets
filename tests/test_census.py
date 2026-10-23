"""The census (tools/census.py): the counts read under the records' own names, the tier a pair
takes from its status, the fold that carries an unchanged record without reading it again, the
CT page's regions and masks, the four files it writes, and the check that refuses census fields
that do not hold together."""

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


def made(volumes=20, where="/grid/harvest/ct_set", vertebrae="by level"):
    return {"origin": "made", "masks": "vertebra masks by level", "vertebrae": vertebrae,
            "by": "the harvest, automatic", "volumes": volumes, "where": where}


def shipped(volumes=20, where="/grid/ct_set", vertebrae="by level", masks="vertebra masks by level, refined by hand"):
    return {"origin": "release", "masks": masks, "vertebrae": vertebrae, "by": "the release's annotators",
            "volumes": volumes, "where": where}


def none_shipped():
    return {"origin": "release", "masks": "none: the release ships images alone", "vertebrae": "none",
            "by": "none", "volumes": None, "where": None}


def not_recorded(where=None):
    return {"origin": "release", "masks": "not recorded: the fetch took the images alone",
            "vertebrae": "not recorded", "by": "not recorded", "volumes": None, "where": where}


def ct_record(**fields):
    base = {"id": "ct_set", "name": "A CT set", "group": "ct", "counts": {"cts": 20, "subjects": 20},
            "regions": ["spine", "pelvis"], "segmentations": [shipped(), made()]}
    base.update(fields)
    return record(**base)


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
        self.assertEqual(counts, {"subjects": 42, "xray_images": 300, "videos": None, "run_frames": None,
                                  "ct_volumes": 40, "bytes": 1500000000})
        self.assertEqual(unread, ["devices"])

    def test_the_frames_inside_videos_are_counted_apart_from_still_images(self):
        counts, _ = census.counts_of(record(group="video", counts={"sequences": 1357, "images": 95308}))
        self.assertEqual((counts["videos"], counts["run_frames"], counts["xray_images"]), (1357, 95308, None))

    def test_a_sweep_set_counts_its_sweeps_and_their_projections(self):
        counts, _ = census.counts_of(record(group="projections", counts={"videos": 692, "run_frames": 375618}))
        self.assertEqual((counts["videos"], counts["run_frames"], counts["xray_images"]), (692, 375618, None))
        counts, _ = census.counts_of(record(group="projections", counts={"projections": 1000}))
        self.assertEqual((counts["run_frames"], counts["xray_images"]), (1000, None))

    def test_fluoroscopy_shots_are_still_images(self):
        counts, _ = census.counts_of(record(group="fluoro", counts={"frames": 299, "videos": 2}))
        self.assertEqual((counts["xray_images"], counts["videos"], counts["run_frames"]), (299, 2, None))

    def test_a_size_is_rounded_to_the_byte_not_cut(self):
        counts, _ = census.counts_of(record(counts={"size_gb": 33.8}))
        self.assertEqual(counts["bytes"], 33800000000)

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
        self.assertEqual(census.licence_kind(None), "unknown")
        self.assertEqual(census.licence_kind("Creative Commons Attribution 4.0 International"), "open")
        self.assertEqual(census.licence_kind("IEEE DataPort open access"), "open")

    def test_a_note_in_parentheses_never_makes_a_licence_open(self):
        self.assertEqual(census.licence_kind(
            "Zenodo, open; licence to confirm on the page (the held record of the same authors is CC BY 4.0)"),
            "unknown")
        self.assertEqual(census.licence_kind("CC BY 4.0 (to confirm on the page)"), "open")

    def test_a_restriction_counts_wherever_the_line_notes_it(self):
        self.assertEqual(census.licence_kind("Kaggle competition rules (non-commercial)"), "restricted")
        self.assertEqual(census.licence_kind(
            "CC BY 4.0 (the article's videos); native DICOM available on reasonable request"), "restricted")

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
        self.assertEqual(tally, {"new": 2, "changed": 0, "rederived": 0, "carried": 0, "removed": 0})
        self.assertEqual([event["kind"] for event in folded["events"]], ["started"])
        self.assertEqual(folded["records"]["second_set"]["first_seen"], "2026-09-30")
        self.assertEqual(folded["records"]["example_set"]["last_changed"], "2026-10-23")
        self.assertEqual(folded["seen"], {"example_set": "2026-10-01", "second_set": "2026-09-30"})

    def test_an_unchanged_record_is_carried_and_never_read_again(self):
        first, _ = census.fold(None, self.records(), "2026-10-23")
        with mock.patch.object(census, "row_of", side_effect=AssertionError("read again")):
            second, tally = census.fold(first, self.records(), "2026-10-24")
        self.assertEqual(tally, {"new": 0, "changed": 0, "rederived": 0, "carried": 2, "removed": 0})
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

    def test_a_record_removed_and_written_again_keeps_its_first_date(self):
        first, _ = census.fold(None, [record()], "2026-10-23")
        second, _ = census.fold(first, [], "2026-10-24")
        third, tally = census.fold(second, [record()], "2026-10-25")
        self.assertEqual(tally["new"], 1)
        self.assertEqual(third["records"]["example_set"]["first_seen"], "2026-10-01")
        self.assertEqual([event["kind"] for event in third["events"]], ["started", "removed", "added"])

    def test_one_id_in_two_records_is_refused(self):
        with self.assertRaisesRegex(ValueError, "example_set"):
            census.fold(None, [record(), record(name="the same id again")], "2026-10-23")

    def test_new_rules_derive_every_row_afresh_with_one_event(self):
        first, _ = census.fold(None, self.records(), "2026-10-23", rules="old")
        second, tally = census.fold(first, self.records(), "2026-10-24", rules="new")
        self.assertEqual((tally["rederived"], tally["changed"], tally["carried"]), (2, 0, 0))
        self.assertEqual(second["rules"], "new")
        self.assertEqual([event["kind"] for event in second["events"]], ["started", "rules"])
        # The records did not change, so neither does the date each last changed.
        self.assertEqual(second["records"]["example_set"]["last_changed"], "2026-10-23")

    def test_a_record_that_changes_with_the_rules_is_still_logged(self):
        first, _ = census.fold(None, [record()], "2026-10-23", rules="old")
        second, tally = census.fold(first, [record(status="granted")], "2026-10-24", rules="new")
        self.assertEqual(tally["changed"], 1)
        kinds = [(event["id"], event["kind"]) for event in second["events"]]
        self.assertEqual(kinds, [("", "started"), ("example_set", "changed"), ("", "rules")])
        self.assertEqual(second["records"]["example_set"]["last_changed"], "2026-10-24")

    def test_the_rules_are_the_code_of_the_census_and_the_pipeline(self):
        self.assertIn(Path(pipeline.__file__).resolve(), census.RULES_FILES)
        self.assertIn(Path(census.__file__).resolve(), census.RULES_FILES)
        with tempfile.TemporaryDirectory() as folder:
            one, two = Path(folder) / "one.py", Path(folder) / "two.py"
            one.write_text("A = 1\n")
            two.write_text("B = 2\n")
            before = census.rules_of((one, two))
            two.write_text("B = 3\n")
            self.assertNotEqual(census.rules_of((one, two)), before)

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
        return census.census_file(folded, tasks, pending, "2026-10-23", "o/r")

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
        # The pages link to the repository, so a new name is a census to write.
        self.assertFalse(census.same(data, dict(later, repo="o/renamed")))

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

    def test_nothing_a_record_or_a_task_says_runs_on_the_page(self):
        records = [record(name="<script>alert(1)</script>", what='"><img src=x onerror=alert(1)>',
                          link="javascript:alert(1)", pairing=pairing(region="<b>bold</b>"))]
        asked = issue(8, "Record: datasets/missing_pair.json", ["todo", "paired"])
        asked["title"] = "<script>alert(2)</script>"
        folded, _ = census.fold(None, records, "2026-10-23")
        tasks, pending = census.tasks_of([asked], records)
        text = census.render_html(census.census_file(folded, tasks, pending, "2026-10-23", "o/r"), "o/r")
        for unsafe in ("<script>alert", "<img", "javascript:", "<b>bold"):
            self.assertNotIn(unsafe, text)
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", text)

    def test_a_null_licence_or_a_number_for_a_name_stops_nothing(self):
        odd = record(licence=None, name=5, what=None)
        row = census.row_of(odd)
        self.assertEqual((row["name"], row["licence"], row["licence_kind"]), ("example_set", "", "unknown"))
        self.assertIn(("example_set", "the licence is still to confirm on the source's page"), census.gaps([row]))
        text = "\n".join(census.problems([odd]))
        self.assertIn("example_set: name must be text", text)
        self.assertIn("example_set: licence must say", text)


class CTTest(unittest.TestCase):
    def rows(self):
        records = [
            ct_record(status="held", grid_path="/grid/ct_set", measured={"bytes": 10 ** 9}),
            ct_record(id="second_ct", name="A second CT set", status="held", grid_path="/grid/second",
                      counts={"cts": 5}, regions=["chest"], segmentations=[not_recorded("/grid/second"), made(5)]),
            ct_record(id="asked_ct", name="An asked CT set", route="letter", status="requested", counts={"cts": 300},
                      regions=["chest", "abdomen"], segmentations=[none_shipped()]),
            ct_record(id="bare_ct", name="A bare CT set", status="fetched", grid_path="/grid/bare", counts={"cts": 3},
                      regions=None, segmentations=None),
            record(),
        ]
        for one in records:
            for key in ("regions", "segmentations"):
                if one.get(key, "") is None:
                    del one[key]
        return [census.row_of(one) for one in records]

    def test_a_record_holds_ct_by_its_regions_its_group_or_its_count(self):
        self.assertFalse(census.row_of(record())["ct"])
        self.assertTrue(census.row_of(record(group="ct"))["ct"])
        self.assertTrue(census.row_of(record(regions=["chest"]))["ct"])
        self.assertTrue(census.row_of(record(counts={"cts": 3}))["ct"])

    def test_regions_keep_the_census_order_and_drop_words_that_are_none_of_them(self):
        self.assertEqual(census.regions_of({"regions": ["spine", "legs", "chest"]}), ["chest", "spine"])
        self.assertEqual(census.regions_of({"regions": "spine"}), [])
        self.assertEqual(census.regions_of({}), [])

    def test_an_entry_says_masks_none_or_not_recorded(self):
        self.assertEqual(census.mask_kind(made()), "masks")
        self.assertEqual(census.mask_kind(none_shipped()), "none")
        self.assertEqual(census.mask_kind(not_recorded()), "unknown")
        self.assertEqual(census.mask_kind({"masks": 5}), "masks")

    def test_no_segmentations_written_is_unsurveyed_and_unlike_an_empty_list(self):
        self.assertIsNone(census.segmentations_of({}))
        self.assertEqual(census.segmentations_of({"segmentations": []}), [])
        self.assertEqual(census.segmentations_of({"segmentations": [made(), "a note"]}), [made()])

    def test_a_set_with_two_entries_for_the_same_cts_counts_them_once(self):
        row = census.row_of(ct_record(segmentations=[made(10), made(7, where="/grid/other"), made(None)]))
        unsized = census.row_of(ct_record(id="unsized", segmentations=[made(None)]))
        covered = census.masks_covered([row, unsized], census.made_masks_on_grid)
        self.assertEqual(covered, {"sum": 10, "counted": 1, "of": 2})

    def test_masks_with_no_grid_folder_are_not_on_the_grid(self):
        self.assertFalse(census.made_masks_on_grid(made(where=None)))
        self.assertFalse(census.made_masks_on_grid(made(where="  ")))
        self.assertFalse(census.level_masks_on_grid(shipped(vertebrae="together")))
        self.assertFalse(census.level_masks_on_grid(not_recorded("/grid/ct_set")))
        self.assertTrue(census.level_masks_on_grid(shipped()))

    def test_the_ct_totals(self):
        ct = census.ct_totals(self.rows())
        self.assertEqual((ct["sets"], ct["on_grid"], ct["surveyed"], ct["no_regions"]), (4, 3, 3, 1))
        self.assertEqual(ct["on_grid_ct_volumes"], {"sum": 28, "counted": 3, "of": 3})
        self.assertEqual(ct["by_region"]["chest"], {"sets": 2, "on_grid": 1,
                                                    "ct_volumes": {"sum": 5, "counted": 1, "of": 1}})
        self.assertEqual(ct["by_region"]["head and neck"]["sets"], 0)
        self.assertEqual(ct["level_masks_on_grid"], {"sum": 20, "counted": 1, "of": 1})
        self.assertEqual(ct["made_masks_on_grid"], {"sum": 25, "counted": 2, "of": 2})
        self.assertEqual(ct["by_stage"]["held"], 2)

    def test_the_ct_gaps_name_what_each_ct_record_lacks(self):
        found = census.ct_gaps(self.rows())
        self.assertIn(("bare_ct", "no regions: write the body regions its CT covers into regions"), found)
        self.assertTrue(any(ident == "bare_ct" and "not surveyed" in text for ident, text in found))
        self.assertTrue(any(ident == "second_ct" and "not recorded yet" in text for ident, text in found))
        # A set asked for, whose source ships none, lacks nothing on this page.
        self.assertFalse(any(ident in ("asked_ct", "ct_set") for ident, _ in found))

    def test_the_mask_filter_words(self):
        rows = {row["id"]: row for row in self.rows()}
        self.assertEqual(census.mask_words(rows["ct_set"]), "|level|level-grid|made|release|")
        self.assertEqual(census.mask_words(rows["second_ct"]), "|level|level-grid|made|unknown|")
        self.assertEqual(census.mask_words(rows["asked_ct"]), "|none|")
        self.assertEqual(census.mask_words(rows["bare_ct"]), "|unsurveyed|")

    def test_on_the_grid_first_then_the_most_cts(self):
        order = [row["id"] for row in census.ct_in_order(self.rows())]
        self.assertEqual(order, ["ct_set", "second_ct", "bare_ct", "asked_ct"])

    def data(self):
        records = [ct_record(status="held", grid_path="/grid/ct_set"),
                   ct_record(id="odd_ct", name="<script>alert(1)</script>", regions=["chest"],
                             segmentations=[made(where="<img src=x onerror=alert(1)>")])]
        folded, _ = census.fold(None, records, "2026-10-23")
        tasks, pending = census.tasks_of([issue(7, "Record: datasets/ct_set.json", ["todo"])], records)
        return census.census_file(folded, tasks, pending, "2026-10-23", "o/r")

    def test_the_ct_page(self):
        text = census.render_ct_html(self.data(), "o/r")
        self.assertIn("<title>Spine CT Census</title>", text)
        for filter_id in ("f-region", "f-stage", "f-licence", "f-masks", "f-q"):
            self.assertIn(f'id="{filter_id}"', text)
        self.assertIn('data-regions="|pelvis|spine|"', text)
        self.assertIn('data-masks="|level|level-grid|made|release|"', text)
        self.assertIn("/grid/harvest/ct_set", text)
        self.assertIn('href="census.html"', text)
        self.assertIn("https://github.com/o/r/issues/7", text)
        for unsafe in ("<script>alert", "<img"):
            self.assertNotIn(unsafe, text)
        self.assertTrue(text.isascii())

    def test_the_whole_census_links_the_ct_page_and_its_markdown_holds_the_ct_section(self):
        data = self.data()
        self.assertIn('href="census-ct.html"', census.render_html(data, "o/r"))
        markdown = census.render_markdown(data, "o/r")
        self.assertIn("## CT, by region and masks", markdown)
        self.assertIn("| A CT set | Held by the owner | 20 | pelvis, spine |", markdown)
        self.assertIn("from the source: vertebrae by level, on the grid; made on the grid: vertebrae by level,"
                      " on the grid", markdown)


class CTCheckTest(unittest.TestCase):
    def found(self, **fields):
        return "\n".join(census.problems([ct_record(**fields)]))

    def test_good_regions_and_masks_pass(self):
        self.assertEqual(census.problems([ct_record()]), [])
        self.assertEqual(census.problems([ct_record(segmentations=[none_shipped()])]), [])
        self.assertEqual(census.problems([ct_record(segmentations=[not_recorded("/grid/ct_set"), made(None, None)])]),
                         [])

    def test_bad_regions_are_named(self):
        self.assertIn("ct_set: regions must be a list of one or more of", self.found(regions="spine"))
        self.assertIn("ct_set: regions must be a list of one or more of", self.found(regions=[]))
        self.assertIn("ct_set: regions holds 'legs', which is none of", self.found(regions=["spine", "legs"]))
        self.assertIn("ct_set: regions names one region twice", self.found(regions=["spine", "spine"]))

    def test_a_list_of_entries_is_required(self):
        self.assertIn("ct_set: segmentations must be a list of one or more entries", self.found(segmentations=[]))
        self.assertIn("ct_set: segmentations entry 1 must be an object", self.found(segmentations=["masks"]))

    def test_a_bad_entry_is_named_by_its_place(self):
        bad = dict(made(), origin="found", vertebrae="some", masks="", by=None, volumes=-1, where="", colour="red")
        text = self.found(segmentations=[made(), bad])
        for line in ("segmentations entry 2: colour is not one of", "segmentations entry 2: origin must be one of",
                     "segmentations entry 2: vertebrae must be one of", "segmentations entry 2: masks must be a line",
                     "segmentations entry 2: by must be a line", "segmentations entry 2: volumes must be a whole",
                     "segmentations entry 2: where must be a grid folder"):
            self.assertIn(line, text)
        self.assertNotIn("segmentations entry 1", text)
        self.assertIn("volumes must be a whole", self.found(segmentations=[made(True)]))

    def test_an_entry_that_names_no_masks_speaks_of_the_source(self):
        self.assertIn("are the source's: origin release", self.found(segmentations=[dict(none_shipped(), origin="made")]))
        self.assertIn("an entry that says none has vertebrae none and where null",
                      self.found(segmentations=[dict(none_shipped(), vertebrae="by level")]))
        self.assertIn("an entry that says none has vertebrae none and where null",
                      self.found(segmentations=[dict(none_shipped(), where="/grid/ct_set")]))
        self.assertIn("an entry that says not recorded has vertebrae not recorded",
                      self.found(segmentations=[dict(not_recorded(), vertebrae="none")]))


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

    def test_the_repository_files_pass(self):
        self.assertEqual(census.file_problems(), [])

    def test_one_id_in_two_files_and_an_id_unlike_its_files_name_are_refused(self):
        with tempfile.TemporaryDirectory() as folder:
            folder = Path(folder)
            (folder / "example_set.json").write_text(json.dumps(record()), encoding="ascii")
            (folder / "copy_of_set.json").write_text(json.dumps(record()), encoding="ascii")
            found = census.file_problems(folder)
        self.assertIn("copy_of_set.json: its id is 'example_set', not the file's name 'copy_of_set'", found)
        self.assertIn("copy_of_set.json, example_set.json: 2 records with the one id 'example_set'", found)


class CommandTest(unittest.TestCase):
    def run_census(self, *args):
        return subprocess.run([sys.executable, str(ROOT / "tools" / "census.py"), *args],
                              capture_output=True, text=True, check=False)

    def test_render_twice_carries_every_record_and_same_says_so(self):
        with tempfile.TemporaryDirectory() as folder:
            first, second = Path(folder) / "first", Path(folder) / "second"
            run = self.run_census("render", "--out", str(first), "--date", "2026-10-23")
            self.assertEqual(run.returncode, 0, run.stderr)
            for name in ("census.json", "CENSUS.md", "census.html", "census-ct.html"):
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
