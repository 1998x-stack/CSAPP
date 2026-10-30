"""M06: guarantee no numbered knowledge point is omitted from chapters 1–3.

The list tracks *scope*, not completeness. Four runnable labs are audited
separately from the 113 textbook section/subsection IDs.
"""
from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCOPE = ROOT / "labs/m06_scope.json"
MANIFEST = ROOT / "examples/manifest.json"

# Independent TOC structure for CSAPP 3e Global Edition chapters 1–3.
COUNTS = (
    (0, 0, 0, 2, 0, 0, 4, 0, 3, 0),
    (9, 8, 8, 6, 0),
    (0, 3, 0, 4, 5, 8, 6, 5, 3, 5, 7, 0),
)


def numbered_ids():
    ids = []
    for chapter, sections in enumerate(COUNTS, 1):
        for section, child_count in enumerate(sections, 1):
            label = f"{chapter}.{section}"
            ids.append(label)
            ids.extend(f"{label}.{subsection}" for subsection in range(1, child_count + 1))
    return ids


class M06ScopeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scope = json.loads(SCOPE.read_text(encoding="utf-8"))
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    def test_every_numbered_item_of_first_three_chapters(self):
        expected = numbered_ids()
        actual = [row["id"] for row in self.scope["topics"]]
        self.assertEqual(len(actual), 113)
        self.assertEqual(actual, expected)
        self.assertEqual(len(set(actual)), len(actual))
        self.assertEqual(Counter(row["id"].split(".")[0] for row in self.scope["topics"]),
                         {"1": 19, "2": 36, "3": 58})
        for row in self.scope["topics"]:
            self.assertTrue(row["title_zh"])
            self.assertIn(row["mapping"], ("topic_files", "section_directory", "unmapped"))
        self.assertEqual(self.scope["expected_by_chapter"], {"1": 19, "2": 36, "3": 58})

    def test_registered_lab_sources_and_knowledge_links(self):
        labs = {entry["id"]: entry for entry in self.manifest["examples"]
                if entry["id"].startswith("m06_")}
        self.assertEqual(set(labs), {
            "m06_ch01_pipeline", "m06_ch02_bits", "m06_ch02_float", "m06_ch03_abi",
        })
        scope_labs = {record["target"]: record["knowledge_points"]
                      for record in self.scope["labs"]}
        self.assertEqual(set(labs), set(scope_labs))
        book_ids = set(numbered_ids())
        for ident, lab in labs.items():
            self.assertEqual(scope_labs[ident], lab["knowledge_points"])
            self.assertTrue(set(lab["knowledge_points"]).issubset(book_ids))
            self.assertTrue(lab["expected"].endswith("PASS"))
            chapter = ident.split("_")[1][-2:]
            for file in lab["sources"]:
                self.assertTrue(file.startswith(chapter + "_"))
                self.assertTrue((ROOT / file).is_file(), file)
        self.assertEqual(labs["m06_ch03_abi"]["platform"], "linux-x86_64")
        self.assertIn("abi_x86_64.S", labs["m06_ch03_abi"]["sources"][1])

    def test_m04_mapping_consistency_when_available(self):
        book = ROOT / "curriculum/catalog.json"
        if not book.is_file():
            self.skipTest("M04 PR #4 is not merged; snapshot validated by independent TOC")
        mapping = json.loads(book.read_text(encoding="utf-8"))
        entries = [item for item in mapping["entries"]
                   if item["chapter_id"] in ("1", "2", "3")]
        for source, canonical in zip(self.scope["topics"], entries):
            self.assertEqual(source["id"], canonical["id"])
            self.assertEqual(source["mapping"], canonical["status"])

    def test_no_scaffold_note_is_claimed_as_completed(self):
        self.assertTrue(all("completion" not in row and "verified" not in row
                            for row in self.scope["topics"]))
        self.assertEqual(self.scope["schema_version"], 1)

    def test_inspection_and_abi_sources_present(self):
        inspection = (ROOT / "scripts/m06_inspect.py").read_text(encoding="utf-8")
        self.assertIn('"readelf"', inspection)
        self.assertIn('"objdump"', inspection)
        asm = (ROOT / "03_程序的机器级表示/m06_sysv_abi/abi_x86_64.S").read_text(encoding="utf-8")
        for token in ("csapp_m06_sum3", "csapp_m06_max2", "cmovl", ".note.GNU-stack"):
            self.assertIn(token, asm)


if __name__ == "__main__":
    unittest.main()
