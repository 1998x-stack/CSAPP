"""M07: all 88 chapter 4–6 TOC entries and three lab mappings stay visible.

Run: python3 -m unittest discover -s tests -p 'test_m07_*.py' -v
Tests are metadata checks; C programs are compiled and run by the CMake CI.
"""
from collections import Counter
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCOPE = ROOT / "labs/m07_scope.json"
MANIFEST = ROOT / "examples/manifest.json"

# CSAPP 3e Global Edition independent numbered section/subsection counts.
SECTIONS = {
    4: (6, 5, 4, 4, 10, 1),
    5: (0, 0, 0, 0, 0, 0, 3, 0, 2, 0, 2, 2, 0, 2, 0),
    6: (4, 3, 2, 7, 0, 3, 0),
}


def expected_ids():
    result = []
    for chapter, sections in SECTIONS.items():
        for sec, children in enumerate(sections, start=1):
            prefix = f"{chapter}.{sec}"
            result.append(prefix)
            result.extend(f"{prefix}.{i}" for i in range(1, children + 1))
    return result


class TestM07CurriculumAndLabs(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scope = json.loads(SCOPE.read_text(encoding="utf-8"))
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    def test_all_88_numbers_in_all_three_chapters(self):
        actual = [row["id"] for row in self.scope["topics"]]
        self.assertEqual(actual, expected_ids())
        self.assertEqual(len(actual), 88)
        self.assertEqual(len(set(actual)), 88)
        self.assertEqual(Counter(x.split(".")[0] for x in actual), {"4": 36, "5": 26, "6": 26})
        self.assertEqual(self.scope["expected_by_chapter"], {"4": 36, "5": 26, "6": 26})
        self.assertEqual(len(self.scope["topics"]), len(set(actual)))
        self.assertTrue(all(row.get("title_zh") for row in self.scope["topics"]))

    def test_no_false_completion_or_ignored_section(self):
        allowed = {"topic_files", "section_directory", "unmapped"}
        for row in self.scope["topics"]:
            self.assertIn(row["mapping"], allowed)
            self.assertNotIn("completed", row)
            self.assertNotIn("verified", row)
            self.assertIsInstance(row["lab_ids"], list)
        self.assertEqual(sum(not row["lab_ids"] for row in self.scope["topics"]), 74)
        self.assertEqual(sum(bool(row["lab_ids"]) for row in self.scope["topics"]), 14)

    def test_lab_manifest_and_scope_links(self):
        labs = {lab["id"]: lab for lab in self.manifest["examples"] if lab["id"].startswith("m07_")}
        expected = {"m07_ch04_y86_subset", "m07_ch05_loop", "m07_ch06_cache"}
        self.assertEqual(set(labs), expected)
        indexed = {lab["target"]: lab["knowledge_points"] for lab in self.scope["labs"]}
        self.assertEqual(set(indexed), expected)
        by_id = {row["id"]: row for row in self.scope["topics"]}
        for name, lab in labs.items():
            self.assertEqual(lab["knowledge_points"], indexed[name])
            self.assertTrue(lab["expected"].endswith("PASS"))
            self.assertTrue(lab["sources"])
            chapter = name.split("_")[1][-2:]
            for src in lab["sources"]:
                self.assertTrue(src.startswith(chapter + "_"), src)
                self.assertTrue((ROOT / src).is_file(), src)
            for number in lab["knowledge_points"]:
                self.assertIn(number, by_id)
                self.assertIn(name, by_id[number]["lab_ids"])
        self.assertEqual(sum(len(lab["knowledge_points"]) for lab in labs.values()), 14)

    def test_m04_mapping_if_present(self):
        catalog_file = ROOT / "curriculum/catalog.json"
        if not catalog_file.exists():
            self.skipTest("M04 PR #4 not merged; independent TOC count checked")
        book = json.loads(catalog_file.read_text(encoding="utf-8"))
        chapters = [e for e in book["entries"] if e["chapter_id"] in ("4", "5", "6")]
        self.assertEqual([e["id"] for e in chapters], [e["id"] for e in self.scope["topics"]])
        for a, b in zip(self.scope["topics"], chapters):
            self.assertEqual(a["mapping"], b["status"])

    def test_cache_trace_and_cmake_integration(self):
        fixture = ROOT / "06_内存层次结构/m07_cache_lru/trace_fixture.txt"
        lines = [line for line in fixture.read_text(encoding="utf-8").splitlines()
                 if line.strip() and not line.startswith("#")]
        self.assertEqual(len(lines), 6)
        self.assertIn(" M 8,1", lines)
        cmake = (ROOT / "CMakeLists.txt").read_text(encoding="utf-8")
        self.assertIn("m07_cache_trace", cmake)
        self.assertIn("hits:3 misses:4 evictions:2", cmake)

    def test_lab_source_is_not_claimed_as_full_y86_or_cachelab(self):
        source = (ROOT / "04_处理器架构/m07_y86_subset/y86_demo.c").read_text(encoding="utf-8")
        self.assertIn("NOT the full CSAPP Y86-64 ISA", source)
        cache = (ROOT / "06_内存层次结构/m07_cache_lru/cache_demo.c").read_text(encoding="utf-8")
        self.assertIn("No cache data is modeled", cache)


if __name__ == "__main__":
    unittest.main()
