"""M04: guard every chapter, book TOC ID, source topic and extra resource."""
from __future__ import annotations

from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
FILE = ROOT / "scripts/build_curriculum.py"
SPEC = importlib.util.spec_from_file_location("build_curriculum", FILE)
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)


class CurriculumCompletenessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.book = json.loads(mod.OUTLINE.read_text(encoding="utf-8"))
        cls.catalog = json.loads(mod.CATALOG.read_text(encoding="utf-8"))

    def test_official_ids_exactly_match_12_chapters_plus_appendix(self):
        all_ids = mod.outline_ids(self.book)
        self.assertEqual(len(all_ids), 380)
        self.assertEqual(all_ids[-2:], ["A.1", "A.2"])
        numbered = all_ids[:-2]
        self.assertEqual(len(set(numbered)), 378)
        self.assertEqual(
            hashlib.sha256("\n".join(numbered).encode("utf-8")).hexdigest(),
            "3cf0d91beabc54cf70d07e45facb11c470a47aba07595292a38902c9f0f04b59",
        )
        self.assertEqual([c["id"] for c in self.book["chapters"]],
                         [str(i) for i in range(1, 13)])

    def test_every_book_entry_has_exactly_one_mapping_status(self):
        all_ids = mod.outline_ids(self.book)
        entries = self.catalog["entries"]
        self.assertEqual([e["id"] for e in entries], all_ids)
        self.assertEqual(len({e["id"] for e in entries}), len(entries))
        self.assertEqual(set(e["status"] for e in entries),
                         {"topic_files", "section_directory", "unmapped"})
        stats = Counter(e["status"] for e in entries)
        self.assertEqual(stats["topic_files"], 310)
        self.assertEqual(stats["section_directory"], 55)
        self.assertEqual(stats["unmapped"], 15)
        self.assertEqual([e["id"] for e in entries if e["status"] == "unmapped"],
                         ["1.10", "2.5", "3.12", "4.6", "4.6.1",
                          "5.15", "6.7", "7.15", "8.8", "9.12",
                          "10.12", "11.7", "12.8", "A.1", "A.2"])

    def test_chapter_counts_match_independent_book_baseline(self):
        chapters = self.catalog["chapters"]
        self.assertEqual(len(chapters), 12)
        self.assertEqual(tuple(c["expected"] for c in chapters),
                         mod.EXPECTED_PER_CHAPTER)
        for row in chapters:
            self.assertEqual(
                row["expected"],
                row["topic_files"] + row["section_directory"] + row["unmapped"],
            )

    def test_each_topic_files_exist_and_group_directories_are_present(self):
        for entry in self.catalog["entries"]:
            if entry["status"] == "topic_files":
                self.assertEqual(entry["file_extensions"], list(mod.EXTS))
                for ext in entry["file_extensions"]:
                    self.assertTrue((ROOT / (entry["topic_base"] + ext)).is_file())
            elif entry["status"] == "section_directory":
                self.assertTrue((ROOT / entry["directory"]).is_dir())

    def test_all_chapter_source_and_document_files_are_accounted_for(self):
        indexed = {
            e["topic_base"] + ext
            for e in self.catalog["entries"] if e["status"] == "topic_files"
            for ext in e["file_extensions"]
        }
        extras = {e["path"] for e in self.catalog["supplementary_files"]}
        self.assertEqual(len(extras), 4)
        self.assertFalse(indexed & extras)
        actual = set()
        for ch in self.book["chapters"]:
            for file in (ROOT / ch["repository_root"]).rglob("*"):
                if file.is_file() and file.suffix in mod.EXTS and not file.is_symlink():
                    actual.add(file.relative_to(ROOT).as_posix())
        self.assertEqual(indexed | extras, actual)
        self.assertEqual(len(indexed), 310 * 4)

    def test_unnumbered_materials_and_appendix_not_dropped(self):
        self.assertEqual(set(self.catalog["unnumbered_materials"]),
                         {str(n) for n in range(1, 13)})
        self.assertEqual(self.catalog["appendix"]["numbered_entries"], ["A.1", "A.2"])
        self.assertIn("references", self.catalog["back_matter"])
        self.assertIn("index", self.catalog["back_matter"])
        self.assertIn("preface", self.catalog["front_matter"])

    def test_catalog_and_report_are_deterministically_generated(self):
        expected_catalog = mod.build_catalog()
        self.assertEqual(self.catalog, expected_catalog)
        self.assertEqual(
            mod.CATALOG.read_text(encoding="utf-8"),
            json.dumps(expected_catalog, ensure_ascii=False, indent=2) + "\n",
        )
        self.assertEqual(mod.REPORT.read_text(encoding="utf-8"),
                         mod.report_text(expected_catalog))

    def test_removed_subsection_cannot_be_hidden_by_equal_total(self):
        corrupted = json.loads(json.dumps(self.book))
        # Keep chapter 1's count equal, but substitute a different subsection ID.
        corrupted["chapters"][0]["subsection_counts"][3] -= 1
        corrupted["chapters"][0]["subsection_counts"][6] += 1
        with self.assertRaises(ValueError):
            mod.outline_ids(corrupted)


if __name__ == "__main__":
    unittest.main()
