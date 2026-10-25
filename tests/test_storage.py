"""The storage planner (tools/storage.py): where each set lives and what it takes, and a trial
combination refused whenever it would pass a cap or name a set that cannot go ahead."""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import storage  # noqa: E402

TB = 10 ** 12
TREE = "a" * 64


def record(ident, status="held", reach="get", grid_path="/rs/rs_grp_oschome/go2432/data/x", size=None,
           frozen=True, steps=("fetch it",), stated_gb=None):
    measured = {}
    if size is not None:
        measured = {"bytes": size, "files": 1, "frozen": "2026-10-24"}
        if frozen:
            measured["tree_sha256"] = TREE
    counts = {"size_gb": stated_gb} if stated_gb is not None else {}
    return {"id": ident, "name": ident.upper(), "group": "ct", "reach": reach, "status": status,
            "grid_path": grid_path, "measured": measured, "counts": counts, "licence": "CC BY 4.0",
            "how_to_get": list(steps)}


class PlannerTest(unittest.TestCase):
    def setUp(self):
        self.records = {
            "big": record("big", size=3 * TB),
            "thawed": record("thawed", size=1 * TB, frozen=False),
            "norecipe": record("norecipe", size=TB, steps=()),
            "athome": record("athome", grid_path="/wsu/home/go2432/data/athome", size=TB // 2),
            "wanted": record("wanted", status="todo", grid_path=None, stated_gb=1500),
            "gated": record("gated", status="needs-owner", reach="gated", grid_path=None, stated_gb=10),
            "sizeless": record("sizeless", status="todo", grid_path=None),
        }
        self.volume = {"quota_bytes": 22 * TB, "used_bytes": 18 * TB, "target_bytes": 20 * TB,
                       "home_quota_bytes": 4 * TB, "home_used_bytes": 1 * TB}

    def plan(self, volume=None):
        return storage.build_plan(self.records, volume or self.volume, None)

    def run_check(self, text, volume=None):
        return storage.check(self.plan(volume), storage.parse_selection(text))

    def test_places_and_sizes(self):
        sets = {entry["id"]: entry for entry in self.plan()["sets"]}
        self.assertEqual(sets["big"]["location"], "lab")
        self.assertEqual(sets["athome"]["location"], "home")
        self.assertEqual(sets["wanted"]["location"], "none")
        self.assertEqual((sets["wanted"]["bytes"], sets["wanted"]["bytes_known"]), (1500 * 10 ** 9, False))
        self.assertTrue(sets["wanted"]["fetchable"])
        self.assertFalse(sets["gated"]["fetchable"])
        plan = self.plan()
        self.assertEqual(plan["volume"]["datasets_bytes"], 5 * TB)
        self.assertEqual(plan["volume"]["other_bytes"], 13 * TB)

    def test_a_fitting_combination(self):
        result = self.run_check("-big, +wanted athome@lab")
        self.assertEqual(result["problems"], [])
        self.assertEqual(result["lab_after"], 18 * TB - 3 * TB + 1500 * 10 ** 9 + TB // 2)
        self.assertEqual(result["home_after"], TB // 2)

    def test_over_the_cap(self):
        problems = self.run_check("+wanted thawed@home big@home")["problems"]
        self.assertTrue(any("home would hold" in p for p in problems), problems)
        problems = self.run_check("+wanted", dict(self.volume, used_bytes=19 * TB))["problems"]
        self.assertTrue(any("over its cap of 20.00 TB" in p for p in problems), problems)

    def test_refusals(self):
        problems = self.run_check("-thawed -norecipe -wanted +gated +sizeless +big athome@home -big big@home")["problems"]
        for words in ("thawed is not frozen", "norecipe has no recipe", "wanted is not on the grid",
                      "gated is gated", "sizeless has no size", "big is already on the grid",
                      "athome is already in the home", "big is named twice"):
            self.assertTrue(any(words in p for p in problems), (words, problems))
        self.assertTrue(self.run_check("+nothing")["problems"])
        with self.assertRaises(ValueError):
            storage.parse_selection("-big; rm -rf /")

    def test_pending_requests(self):
        pulls = [{"number": 7, "html_url": "u7", "head": {"ref": "storage/request-20261024T000000Z"},
                  "body": "Made.\n\nSelection: `-big +wanted`\n\n- big"},
                 {"number": 8, "html_url": "u8", "head": {"ref": "claude/8"}, "body": "Selection: `-big`"},
                 {"number": 9, "html_url": "u9", "head": {"ref": "storage/request-x"}, "body": "Selection: `rm -rf`"}]
        plan = storage.build_plan(self.records, self.volume, None, pulls)
        self.assertEqual(plan["requests"], [{"number": 7, "url": "u7", "selection": "-big +wanted"},
                                            {"number": 9, "url": "u9", "selection": ""}])

    def test_home_unread(self):
        volume = dict(self.volume, home_used_bytes=None)
        problems = self.run_check("big@home", volume)["problems"]
        self.assertTrue(any("home's use has not been read" in p for p in problems))
        self.assertEqual(self.run_check("-big", volume)["problems"], [])

    def test_commands(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = os.path.join(tmp, "datasets")
            os.makedirs(folder)
            for ident, entry in self.records.items():
                with open(os.path.join(folder, ident + ".json"), "w") as handle:
                    json.dump(entry, handle)
            volume = os.path.join(tmp, "VOLUME.json")
            with open(volume, "w") as handle:
                json.dump(self.volume, handle)
            base = ["--records", folder, "--volume", volume, "--overlap", os.path.join(tmp, "none.json")]
            out = os.path.join(tmp, "PLAN.json")
            self.assertEqual(storage.main(base + ["plan", "--out", out]), 0)
            self.assertEqual(storage.main(base + ["plan", "--out", out, "--check"]), 0)
            request = os.path.join(tmp, "requests", "r.json")
            text = os.path.join(tmp, "r.md")
            self.assertEqual(storage.main(base + ["request", "--out", request, "--text", text, "--", "-big +wanted"]), 0)
            with open(request) as handle:
                made = json.load(handle)
            self.assertEqual([a["id"] for a in made["actions"]], ["big", "wanted"])
            self.assertEqual((made["actions"][0]["grid_path"], made["actions"][0]["tree_sha256"]),
                             ("/rs/rs_grp_oschome/go2432/data/x", TREE))
            self.assertNotIn("grid_path", made["actions"][1])
            self.assertEqual(made["actions"][0]["folder"], "/rs/rs_grp_oschome/go2432/data/x")
            with open(text) as handle:
                body = handle.read()
            self.assertIn("big (BIG): retire", body)
            self.assertIn("exact size read before it lands", body)
            self.assertEqual(storage.main(base + ["check", "--", "-thawed"]), 1)



class OverlapTest(unittest.TestCase):
    def test_only_shared_scans_count(self):
        pair = dict.fromkeys(("patients", "series", "same_bytes", "same_values", "same_geometry"), 0)
        table = {"pairs": [dict(pair, a="ctspine1k", b="ctspinopelvic1k", same_values=526, same_geometry=747),
                           dict(pair, a="amos22", b="ctspine1k", same_geometry=3),
                           {"a": "ctspine1k", "b": "verse", "patients": 2, "series": 0, "same_bytes": 0}]}
        found = storage.overlap_of(table, "ctspine1k")
        self.assertEqual([entry["with"] for entry in found], ["ctspinopelvic1k", "verse"])
        self.assertEqual(found[0]["same_scans"], 526)
        self.assertEqual(found[1]["same_scans"], 0, "a format-1 pair has no voxel count")


class ValueTest(unittest.TestCase):
    """What a set is worth, read from its record alone: masks people read count as level truth,
    a tool's masks do not, and a count the record does not give stays null."""

    def test_read_masks_give_level_truth_and_a_prior_source(self):
        rec = dict(record("spine_ct"), regions=["spine", "pelvis"], counts={"subjects": 400, "ct_volumes": 410},
                   level_truth="vertebra masks by level",
                   segmentations=[{"origin": "release", "vertebrae": "by level", "by": "the authors", "where": "masks/"}])
        value = storage.value_of(rec)
        self.assertEqual((value["level_truth"], value["level_truth_people"], value["level_truth_scans"]),
                         ("read", 400, 410))
        self.assertTrue(value["prior_source"] and value["masks_held"] and value["spine"])
        self.assertEqual(value["masks_by_level"], "read")

    def test_a_tools_masks_are_automatic_and_count_no_people(self):
        rec = dict(record("screening"), regions=["chest"], counts={"subjects": 24713},
                   level_truth="counted by the census pipeline once fetched",
                   segmentations=[{"origin": "release", "vertebrae": "by level",
                                   "by": "IDC, automatic (TotalSegmentator)", "where": None}])
        value = storage.value_of(rec)
        self.assertEqual((value["level_truth"], value["level_truth_people"]), ("automatic", None))
        self.assertTrue(value["prior_source"])
        self.assertFalse(value["masks_held"])

    def test_none_and_unread(self):
        none = storage.value_of(dict(record("films"), group="films", level_truth="none; no spine"))
        self.assertEqual((none["level_truth"], none["level_truth_people"], none["spine"]), ("no", 0, None))
        unread = storage.value_of(dict(record("films2"), group="films", level_truth="not recorded"))
        self.assertEqual((unread["level_truth"], unread["people"]), ("unknown", None))

    def test_power_block(self):
        self.assertEqual(storage.people_needed(), 385)
        records = {"a": dict(record("a", size=TB), counts={"subjects": 300}, level_truth="L1 to L5 by the authors"),
                   "b": dict(record("b", status="todo", grid_path=None), counts={"subjects": 900},
                             level_truth="L1 to L5")}
        power = storage.build_plan(records, {"used_bytes": TB}, None)["power"]
        self.assertEqual(power["level_truth_people_kept"], 300, "a set not on the drives is not kept")
        self.assertEqual((power["half_width"], power["confidence"], power["assumed_accuracy"]), (0.05, 0.95, 0.5))


if __name__ == "__main__":
    unittest.main()
