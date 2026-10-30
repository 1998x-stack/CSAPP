"""M08: complete chapter 7–9 scope and five real laboratory targets."""
from collections import Counter
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCOPE = ROOT / "labs/m08_scope.json"
MANIFEST = ROOT / "examples/manifest.json"

SECTIONS = {
    7: (0,0,0,0,0,3,2,0,0,0,0,0,3,0,0),
    8: (3,5,0,6,7,0,0,0),
    9: (0,0,6,0,0,4,2,4,14,3,10,0),
}


def expected_ids():
    ids = []
    for chapter, sections in SECTIONS.items():
        for section, children in enumerate(sections, 1):
            prefix = f"{chapter}.{section}"
            ids.append(prefix)
            ids.extend(f"{prefix}.{i}" for i in range(1, children + 1))
    return ids


class TestM08Labs(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scope = json.loads(SCOPE.read_text(encoding="utf-8"))
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    def test_every_numbered_item_from_chapters_7_8_9(self):
        actual = [row["id"] for row in self.scope["topics"]]
        self.assertEqual(len(actual), 107)
        self.assertEqual(actual, expected_ids())
        self.assertEqual(len(set(actual)), 107)
        self.assertEqual(Counter(id.split(".")[0] for id in actual),
                         {"7": 23, "8": 29, "9": 55})
        self.assertEqual(self.scope["expected_by_chapter"], {"7": 23, "8": 29, "9": 55})

    def test_lab_relations_and_source_presence(self):
        labs = {e["id"]: e for e in self.manifest["examples"] if e["id"].startswith("m08_")}
        names = {"m08_ch07_link", "m08_ch08_fork", "m08_ch08_signals",
                 "m08_ch09_mmap", "m08_ch09_arena"}
        self.assertEqual(set(labs), names)
        registered = {e["target"]: e["knowledge_points"] for e in self.scope["labs"]}
        self.assertEqual(set(registered), names)
        by_id = {e["id"]: e for e in self.scope["topics"]}
        linked = set()
        for target, lab in labs.items():
            self.assertEqual(lab["knowledge_points"], registered[target])
            self.assertTrue(lab["expected"].endswith("PASS"))
            chapter = target.split("_")[1][-2:]
            for source in lab["sources"]:
                self.assertTrue(source.startswith(chapter + "_"), source)
                self.assertTrue((ROOT / source).is_file(), source)
            for number in lab["knowledge_points"]:
                self.assertIn(number, by_id)
                self.assertIn(target, by_id[number]["lab_ids"])
                linked.add(number)
        self.assertEqual(len(linked), 25)
        self.assertEqual(sum(not entry["lab_ids"] for entry in self.scope["topics"]), 82)

    def test_mapping_is_not_completion(self):
        for entry in self.scope["topics"]:
            self.assertTrue(entry["title_zh"])
            self.assertIn(entry["mapping"], ("topic_files", "section_directory", "unmapped"))
            self.assertNotIn("completed", entry)
            self.assertNotIn("verified", entry)
        self.assertIn("not full", self.scope["semantics"])

    def test_crosscheck_m04_when_catalog_exists(self):
        catalog = ROOT / "curriculum/catalog.json"
        if not catalog.is_file():
            self.skipTest("M04 PR #4 not merged; independent TOC baseline checked")
        expected = [e for e in json.loads(catalog.read_text(encoding="utf-8"))["entries"]
                    if e["chapter_id"] in ("7", "8", "9")]
        self.assertEqual([e["id"] for e in expected],
                         [e["id"] for e in self.scope["topics"]])
        for a, b in zip(self.scope["topics"], expected):
            self.assertEqual(a["mapping"], b["status"])

    def test_platform_labs_declared_and_elf_inspection_present(self):
        labs = {e["id"]: e for e in self.manifest["examples"] if e["id"].startswith("m08_")}
        for lab in ("m08_ch08_fork", "m08_ch08_signals", "m08_ch09_mmap"):
            self.assertEqual(labs[lab]["platform"], "linux-x86_64")
        src = (ROOT / "scripts/m08_inspect_linker.py").read_text(encoding="utf-8")
        for name in ('"ar"', '"nm"', '"readelf"', '"objdump"',
                     "m08_sum_3", "M08 static linker inspection: PASS"):
            self.assertIn(name, src)

    def test_original_files_unmodified_by_experiments(self):
        filepaths = [source for e in self.manifest["examples"] if e["id"].startswith("m08_")
                     for source in e["sources"]]
        self.assertEqual(len(filepaths), 6)
        self.assertEqual(len(set(filepaths)), 6)
        self.assertTrue(all("/m08_" in path for path in filepaths))


if __name__ == "__main__":
    unittest.main()
