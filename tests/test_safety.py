"""M01 safety regression tests (stdlib only)."""
import tempfile
import unittest
from pathlib import Path

import main
from scripts.safe_transform import convert, process


class ScaffoldSafetyTests(unittest.TestCase):
    STRUCTURE = {"01_Intro": [{"1.1_Foo": []}, {"1.2_Bar": ["1.2.1_Baz"]}]}

    def test_preview_is_read_only_and_apply_is_idempotent(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            paths = list(main.iter_scaffold_files(self.STRUCTURE))
            self.assertEqual(len(paths), 6)
            self.assertEqual(main.run_scaffold(root, self.STRUCTURE)["missing"], 6)
            self.assertEqual(list(root.iterdir()), [])
            first = main.run_scaffold(root, self.STRUCTURE, apply=True, index=True)
            self.assertEqual(first["created"], 7)
            self.assertFalse((root / "README.md").exists())
            special = root / paths[0][0]
            special.write_text("MY NOTES\n", encoding="utf-8")
            second = main.run_scaffold(root, self.STRUCTURE, apply=True, index=True)
            self.assertEqual(second["created"], 0)
            self.assertEqual(special.read_text(encoding="utf-8"), "MY NOTES\n")

    def test_scaffold_refuses_symlinked_directory_escape(self):
        with tempfile.TemporaryDirectory() as d, tempfile.TemporaryDirectory() as outside:
            root = Path(d)
            (root / "01_Intro").symlink_to(Path(outside), target_is_directory=True)
            with self.assertRaises(ValueError):
                main.run_scaffold(root, self.STRUCTURE, apply=True)
            self.assertEqual(list(Path(outside).iterdir()), [])

    def test_scaffold_does_not_replace_existing_symlink(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            paths = list(main.iter_scaffold_files(self.STRUCTURE))
            target = root / paths[0][0]
            target.parent.mkdir(parents=True)
            target.symlink_to(root / "nonexistent")
            result = main.run_scaffold(root, self.STRUCTURE, apply=True)
            self.assertEqual(result["created"], 5)
            self.assertTrue(target.is_symlink())


class MarkdownSafetyTests(unittest.TestCase):
    def test_transform_preserves_citations(self):
        s = r"Math \(x+y\) and \[x^2\], keep 【来源：教材】"
        self.assertEqual(convert(s), "Math $x+y$ and $$x^2$$, keep 【来源：教材】")

    def test_dry_run_and_backups_and_file_scope(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            md = root / "article.md"
            md.write_text(r"Inline \(x\) and 【引用】", encoding="utf-8")
            py = root / "code.py"
            py.write_text(r"print('\(x\)')", encoding="utf-8")
            pdf = root / "book.pdf"
            pdf.write_bytes(b"%PDF-1.4 \\( untouched")
            (root / "link.md").symlink_to(md)
            preview = process(root)
            self.assertEqual(preview["changed"], 1)
            self.assertEqual(md.read_text(encoding="utf-8"), r"Inline \(x\) and 【引用】")
            applied = process(root, apply=True)
            self.assertEqual(applied["applied"], 1)
            self.assertEqual((root / "article.md.bak").read_text(encoding="utf-8"), r"Inline \(x\) and 【引用】")
            self.assertEqual(md.read_text(encoding="utf-8"), "Inline $x$ and 【引用】")
            self.assertEqual(py.read_text(encoding="utf-8"), r"print('\(x\)')")
            self.assertEqual(pdf.read_bytes(), b"%PDF-1.4 \\( untouched")
            self.assertEqual(process(root, apply=True)["applied"], 0)


if __name__ == "__main__":
    unittest.main()
