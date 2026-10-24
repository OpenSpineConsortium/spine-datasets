"""The overlap ledger (tools/lineage.py): DICOM UIDs read without a DICOM library, the same bytes
and the same scans found across sets, names counted only when they look like identifiers, and a
public table that carries counts alone."""

import gzip
import hashlib
import json
import os
import sqlite3
import struct
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import lineage  # noqa: E402


def element_explicit(group, element, vr, value):
    if vr in lineage.LONG_VRS:
        return struct.pack("<HH2sHI", group, element, vr, 0, len(value)) + value
    return struct.pack("<HH2sH", group, element, vr, len(value)) + value


def element_implicit(group, element, value):
    return struct.pack("<HHI", group, element, len(value)) + value


def padded(text):
    data = text.encode("ascii")
    return data + (b"\x00" if len(data) % 2 else b"")


def dicom_file(patient, study, series, implicit=False, with_sequence=True):
    syntax = padded(lineage.IMPLICIT_LE if implicit else "1.2.840.10008.1.2.1")
    meta_body = element_explicit(0x0002, 0x0010, b"UI", syntax)
    meta = element_explicit(0x0002, 0x0000, b"UL", struct.pack("<I", len(meta_body))) + meta_body
    if implicit:
        body = element_implicit(0x0008, 0x0060, padded("CT"))
        if with_sequence:
            item = element_implicit(0x0008, 0x1150, padded("1.2.3"))
            body += struct.pack("<HHI", 0x0008, 0x1140, lineage.UNDEFINED)
            body += struct.pack("<HHI", 0xFFFE, 0xE000, lineage.UNDEFINED) + item
            body += struct.pack("<HHI", 0xFFFE, 0xE00D, 0) + struct.pack("<HHI", 0xFFFE, 0xE0DD, 0)
        body += element_implicit(0x0010, 0x0020, padded(patient))
        body += element_implicit(0x0020, 0x000D, padded(study))
        body += element_implicit(0x0020, 0x000E, padded(series))
        body += element_implicit(0x7FE0, 0x0010, b"\x00" * 16)
    else:
        body = element_explicit(0x0008, 0x0060, b"CS", padded("CT"))
        if with_sequence:
            item = element_explicit(0x0008, 0x1150, b"UI", padded("1.2.3"))
            body += struct.pack("<HH2sHI", 0x0008, 0x1140, b"SQ", 0, lineage.UNDEFINED)
            body += struct.pack("<HHI", 0xFFFE, 0xE000, lineage.UNDEFINED) + item
            body += struct.pack("<HHI", 0xFFFE, 0xE00D, 0) + struct.pack("<HHI", 0xFFFE, 0xE0DD, 0)
        body += element_explicit(0x0010, 0x0020, b"LO", padded(patient))
        body += element_explicit(0x0020, 0x000D, b"UI", padded(study))
        body += element_explicit(0x0020, 0x000E, b"UI", padded(series))
    return b"\x00" * 128 + b"DICM" + meta + body


def write_set(top, ident, files):
    """A frozen set: its files and the file list a freeze would have written beside them."""
    folder = os.path.join(top, ident)
    lines = []
    for path, data in sorted(files.items()):
        full = os.path.join(folder, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "wb") as handle:
            handle.write(data)
        lines.append("%s\t%d\t%s\n" % (hashlib.sha256(data).hexdigest(), len(data), path))
    with gzip.open(os.path.join(folder, lineage.FILE_LIST), "wb") as handle:
        handle.write("".join(lines).encode("utf-8"))
    return folder


BIG = lineage.DATA_BYTES


class DicomTest(unittest.TestCase):
    def test_explicit_with_a_sequence_before_the_uids(self):
        tags = lineage.dicom_tags(dicom_file("LIDC-0001", "1.2.840.1", "1.2.840.2"))
        self.assertEqual(tags[lineage.PATIENT_ID], "LIDC-0001")
        self.assertEqual(tags[lineage.STUDY_UID], "1.2.840.1")
        self.assertEqual(tags[lineage.SERIES_UID], "1.2.840.2")

    def test_implicit(self):
        tags = lineage.dicom_tags(dicom_file("P1", "1.9.1", "1.9.2", implicit=True))
        self.assertEqual(tags[lineage.SERIES_UID], "1.9.2")

    def test_no_preamble_implicit(self):
        data = element_implicit(0x0008, 0x0060, padded("CT")) + element_implicit(0x0020, 0x000E, padded("1.5.5"))
        self.assertEqual(lineage.dicom_tags(data)[lineage.SERIES_UID], "1.5.5")

    def test_not_dicom(self):
        with self.assertRaises(lineage.NotDicom):
            lineage.dicom_tags(b"\x1f\x8b" + b"x" * 300)


class NamesTest(unittest.TestCase):
    def test_stems(self):
        self.assertEqual(lineage.stem_of("raw/a/HN_P001_0000.nii.gz"), "hn_p001")
        self.assertEqual(lineage.stem_of("labels/1.3.6.1.4.1.9328.50.4.0001_seg.nii.gz"), "1.3.6.1.4.1.9328.50.4.0001")
        self.assertIsNone(lineage.stem_of("README.md"))

    def test_only_identifier_names_count(self):
        self.assertTrue(lineage.stem_counts("1.3.6.1.4.1.9328.50.4.0001"))
        self.assertTrue(lineage.stem_counts("verse_gl003"))
        self.assertFalse(lineage.stem_counts("case_00001"))
        self.assertFalse(lineage.stem_counts("img0001"))
        self.assertFalse(lineage.stem_counts("abcdefgh"))


class BuildTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        top = self.tmp.name
        shared_scan = b"S" * BIG
        self.a = write_set(top, "set_a", {
            "raw/p1/s1/1.dcm": dicom_file("TCIA-PT-0001", "1.2.3.10", "1.2.3.11"),
            "raw/p1/s1/2.dcm": dicom_file("TCIA-PT-0001", "1.2.3.10", "1.2.3.11"),
            "raw/vol/1.2.3.11.nii.gz": shared_scan,
            "raw/vol/case_00001.nii.gz": b"A" * BIG,
            "LICENSE": b"same licence",
        })
        self.b = write_set(top, "set_b", {
            "images/1.2.3.11.nii.gz": shared_scan,
            "images/case_00001.nii.gz": b"B" * BIG,
            "LICENSE": b"same licence",
        })
        self.c = write_set(top, "set_c", {
            "dicom/x/1.dcm": dicom_file("TCIA-PT-0001", "1.2.3.10", "1.2.3.11", implicit=True),
        })
        self.plan = os.path.join(top, "plan.tsv")
        with open(self.plan, "w") as handle:
            handle.write("set_a\t%s\t-\nset_b\t%s\t-\nset_c\t%s\t-\nmissing\t%s/none\t-\n" % (self.a, self.b, self.c, top))
        self.out = os.path.join(top, "out")

    def tearDown(self):
        self.tmp.cleanup()

    def pair(self, table, a, b):
        return next(row for row in table["pairs"] if (row["a"], row["b"]) == (a, b))

    def test_the_overlap_table(self):
        table = lineage.build(lineage.sets_from(self.plan), self.out, workers=2)
        self.assertEqual(sorted(table["sets"]), ["set_a", "set_b", "set_c"])
        ab = self.pair(table, "set_a", "set_b")
        self.assertEqual((ab["same_files"], ab["same_bytes"]), (1, BIG), "the licence is under the floor")
        self.assertEqual(ab["names"], 1, "the UID name, not case_00001")
        ac = self.pair(table, "set_a", "set_c")
        self.assertEqual((ac["series"], ac["studies"], ac["patients"]), (1, 1, 1))
        self.assertEqual(self.pair(table, "set_b", "set_c")["names_to_uids"], 1)
        self.assertEqual(table["sets"]["set_a"]["unique_bytes"], BIG, "only case_00001 of set_a is its own")
        self.assertEqual(table["sets"]["set_a"]["dicom_series"], 1)

    def test_outputs(self):
        lineage.build(lineage.sets_from(self.plan), self.out)
        public = lineage.read_overlap(os.path.join(self.out, lineage.OVERLAP))
        self.assertEqual(lineage.public_problems(public), [])
        text = json.dumps(public)
        for secret in ("1.2.3.11", "TCIA-PT-0001", "case_00001", "raw/"):
            self.assertNotIn(secret, text)
        db = sqlite3.connect(os.path.join(self.out, lineage.LEDGER))
        self.assertEqual(db.execute("SELECT count(*) FROM file").fetchone()[0], 9)
        self.assertEqual(db.execute("SELECT count(*) FROM dicom").fetchone()[0], 2)

    def test_shared_tree(self):
        shared = os.path.join(self.tmp.name, "shared")
        write_set(shared, "set_d", {"raw/1.2.3.11.nii.gz": b"S" * BIG})
        found = dict(lineage.sets_from(self.plan, shared))
        self.assertIn("set_d", found)
        self.assertNotIn("missing", found)


class PublicTest(unittest.TestCase):
    def table(self):
        counts = dict.fromkeys(lineage.SET_KEYS, 0)
        return {"format": lineage.FORMAT, "built_at": "2026-10-24T00:00:00Z", "data_bytes_floor": BIG,
                "sets": {"a": dict(counts), "b": dict(counts)},
                "pairs": [dict(dict.fromkeys(lineage.PAIR_KEYS - {"a", "b"}, 0), a="a", b="b")]}

    def test_counts_pass(self):
        self.assertEqual(lineage.public_problems(self.table()), [])

    def test_a_name_is_refused(self):
        table = self.table()
        table["sets"]["a"]["files"] = "1.2.3.11"
        self.assertTrue(lineage.public_problems(table))
        table = self.table()
        table["pairs"][0]["example"] = "case_00001"
        self.assertTrue(lineage.public_problems(table))
        table = self.table()
        table["sets"]["TCIA-PT-0001"] = table["sets"].pop("a")
        self.assertTrue(lineage.public_problems(table))

    def test_tree(self):
        with tempfile.TemporaryDirectory() as tmp:
            overlap = os.path.join(tmp, lineage.OVERLAP)
            lineage.write_overlap(self.table(), overlap)
            tree = os.path.join(tmp, "tree.json")
            with open(tree, "w") as handle:
                json.dump({"tree": [{"path": "frozen/a.json", "mode": "100644", "type": "blob", "content": "{}"}]}, handle)
            self.assertTrue(lineage.add_to_tree(overlap, tree))
            with open(tree) as handle:
                paths = [entry["path"] for entry in json.load(handle)["tree"]]
            self.assertEqual(paths, ["frozen/a.json", "lineage/OVERLAP.json"])


if __name__ == "__main__":
    unittest.main()
