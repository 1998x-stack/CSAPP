"""M05 complete docs navigation and evidence-gated status regression tests."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile
from unittest.mock import patch
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("build_docs", ROOT / "scripts" / "build_docs.py")
docs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(docs)


class M05DocumentationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = docs.json_read(docs.CATALOG)
        cls.plans = docs.build_plan()
        cls.status = json.loads(cls.plans["metadata/status.json"])
        cls.entries = cls.status["entries"]

    def test_380_pages_all_twelve_chapters_and_appendix_exist(self):
        self.assertEqual(self.status["entry_count"], 380)
        self.assertEqual(len(self.entries), 380)
        self.assertEqual(len({e["id"] for e in self.entries}), 380)
        for entry in self.catalog["entries"]:
            self.assertIn(docs.location(entry), self.plans)
            self.assertIn(f"# {entry['id']} {entry['title_zh']}", self.plans[docs.location(entry)])
        for n in range(1, 13):
            self.assertIn(f"chapters/{n:02d}/index.md", self.plans)
            self.assertIn(f"第 {n} 章", self.plans[f"chapters/{n:02d}/index.md"])
        self.assertIn("appendix/index.md", self.plans)
        for number in ("A.1", "A.2"):
            self.assertIn(f"appendix/{number}.md", self.plans)

    def test_missing_entries_have_explicit_honest_placeholders(self):
        missing = [e for e in self.catalog["entries"] if e["status"] == "unmapped"]
        self.assertEqual(len(missing), 15)
        for entry in missing:
            page = self.plans[docs.location(entry)]
            self.assertIn("待完善", page)
            self.assertIn("不包含编造的教材讲解", page)
            self.assertNotIn("## 原始学习笔记", page)
        group = [e for e in self.catalog["entries"] if e["status"] == "section_directory"]
        self.assertEqual(len(group), 55)
        for entry in group:
            self.assertIn("## 下级条目", self.plans[docs.location(entry)])

    def test_note_code_and_review_are_distinct(self):
        by_id = {e["id"]: e for e in self.entries}
        self.assertEqual(by_id["1.1"]["notes"], "draft")
        self.assertEqual(by_id["12.7.5"]["notes"], "template")
        self.assertEqual(by_id["12.7.5"]["code"], "template")
        self.assertEqual(by_id["2.2.3"]["test"], "verified")
        self.assertEqual(by_id["2.2.3"]["code"], "implemented")
        self.assertNotIn("reviewed", {s["notes"] for s in self.entries})
        self.assertEqual(self.status["counts"]["test:verified"], 6)
        self.assertEqual(self.status["counts"]["mapping:unmapped"], 15)
        self.assertEqual(self.status["counts"]["mapping:section_directory"], 55)
        self.assertEqual(self.status["counts"]["mapping:topic_files"], 310)

    def test_all_supplemental_assets_remain_accessible(self):
        self.assertEqual(len(self.status["supplementary_files"]), 4)
        for row in self.status["supplementary_files"]:
            self.assertTrue(docs.checked_file(row["path"]).is_file())
            self.assertIn(docs.source_link(row["path"]), self.plans["progress.md"])

    def test_review_evidence_must_match_real_m02_suite(self):
        reviews = docs.get_reviews(self.catalog)
        self.assertEqual(len(reviews["tests_verified"]), 6)
        invalid = docs.json_read(docs.REVIEWS)
        invalid["tests_verified"][0]["source"] = "02_程序结构和执行/nonexistent.cpp"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "reviews.json"
            path.write_text(json.dumps(invalid, ensure_ascii=False), encoding="utf-8")
            with patch.object(docs, "REVIEWS", path):
                with self.assertRaises(ValueError):
                    docs.get_reviews(self.catalog)

    def test_generate_and_verify_without_touching_source(self):
        # Temporarily change only the permitted generated output directory.
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "m05-docs"
            with patch.object(docs, "OUTPUT", output):
                docs.generate(self.plans, output)
                self.assertTrue((output / docs.MARKER).exists())
                files = {p.relative_to(output).as_posix()
                         for p in output.rglob("*") if p.is_file()}
                self.assertEqual(files, set(self.plans) | {docs.MARKER})
                self.assertEqual((output / "appendix/A.1.md").read_text(encoding="utf-8"),
                                 self.plans["appendix/A.1.md"])
                docs.generate(self.plans, output)
                self.assertEqual(files, {p.relative_to(output).as_posix()
                                         for p in output.rglob("*") if p.is_file()})
                (output / "chapters/01/1.1.md").write_text("manual edit\n", encoding="utf-8")
                self.assertNotEqual(
                    (output / "chapters/01/1.1.md").read_text(encoding="utf-8"),
                    self.plans["chapters/01/1.1.md"],
                )

    def test_refuse_to_replace_unmarked_generated_folder(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "protected"
            output.mkdir()
            (output / "my-notes.md").write_text("IMPORTANT")
            with patch.object(docs, "OUTPUT", output):
                with self.assertRaises(ValueError):
                    docs.generate(self.plans, output)
            self.assertEqual((output / "my-notes.md").read_text(), "IMPORTANT")


if __name__ == "__main__":
    unittest.main()
