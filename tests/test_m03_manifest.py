"""M03 manifest and source-inventory contract tests (no third-party packages)."""
import importlib.util
from pathlib import Path
import json
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("audit_sources", ROOT / "scripts" / "audit_sources.py")
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class ManifestTests(unittest.TestCase):
    def test_curated_sources_exist_and_have_code(self):
        manifest = json.loads((ROOT / "examples" / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(audit.validate_manifest(ROOT, manifest), [])
        self.assertGreaterEqual(len(manifest["examples"]), 6)
        self.assertEqual(len({row["id"] for row in manifest["examples"]}),
                         len(manifest["examples"]))

    def test_placeholder_detection(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cpp = root / "blank.cpp"
            cpp.write_text("// title\n/* Description */\n", encoding="utf-8")
            self.assertTrue(audit.is_placeholder(cpp))
            cpp.write_text("int main() { return 0; }\n", encoding="utf-8")
            self.assertFalse(audit.is_placeholder(cpp))
            py = root / "blank.py"
            py.write_text('# comment\n"""Lecture: demo"""\n', encoding="utf-8")
            self.assertTrue(audit.is_placeholder(py))
            py.write_text('"""Demo"""\nprint(1)\n', encoding="utf-8")
            self.assertFalse(audit.is_placeholder(py))

    def test_rejects_duplicate_unsafe_and_stub_sources(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "01_Unit").mkdir()
            (root / "01_Unit" / "stub.cpp").write_text("// only comments\n", encoding="utf-8")
            invalid = {
                "schema_version": 1,
                "examples": [
                    {"id": "dup", "sources": ["01_Unit/stub.cpp"], "expected": "ok"},
                    {"id": "dup", "sources": ["../outside.cpp"], "expected": "ok"},
                ],
            }
            errors = audit.validate_manifest(root, invalid)
            self.assertTrue(any("placeholder" in e for e in errors), errors)
            self.assertTrue(any("duplicate id" in e for e in errors), errors)
            self.assertTrue(any("unsafe" in e for e in errors), errors)


if __name__ == "__main__":
    unittest.main()
