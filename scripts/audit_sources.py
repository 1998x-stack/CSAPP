#!/usr/bin/env python3
"""Read-only CSAPP source inventory and curated build manifest validation.

Usage: python3 scripts/audit_sources.py [--check] [--json] [--details]
A source file is 'placeholder' iff it contains only comments/whitespace (C)
or a Python module docstring. 'Implemented' does NOT mean verified or correct.
"""
from __future__ import annotations

import argparse
import ast
from collections import Counter
import json
from pathlib import Path, PurePosixPath
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "examples" / "manifest.json"
SOURCE_EXT = frozenset({".c", ".cc", ".cpp", ".cxx", ".s", ".S", ".py"})
BUILDABLE_EXT = SOURCE_EXT - {".py"}
_ID = re.compile(r"^[a-z][a-z0-9_]*$")
_CHAPTER = re.compile(r"^(?:0[1-9]|1[0-2])_")
_BLOCK = re.compile(r"/\*.*?\*/", flags=re.S)
_LINE = re.compile(r"//[^\n]*")


def is_placeholder(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".py":
        try:
            nodes = ast.parse(text).body
        except SyntaxError:
            return False  # broken Python is not an empty placeholder
        return not nodes or (
            len(nodes) == 1
            and isinstance(nodes[0], ast.Expr)
            and isinstance(nodes[0].value, ast.Constant)
            and isinstance(nodes[0].value.value, str)
        )
    return not _LINE.sub("", _BLOCK.sub("", text)).strip()


def chapter_sources(root: Path):
    for chapter in sorted(root.iterdir()):
        if chapter.is_symlink() or not chapter.is_dir() or not _CHAPTER.match(chapter.name):
            continue
        for path in sorted(chapter.rglob("*")):
            if path.suffix in SOURCE_EXT and path.is_file() and not path.is_symlink():
                if not path.resolve().is_relative_to(root.resolve()):
                    continue
                yield path


def validate_manifest(root: Path, manifest: dict) -> list[str]:
    errors = []
    if manifest.get("schema_version") != 1 or not isinstance(manifest.get("examples"), list):
        return ["Manifest must define schema_version 1 and an examples array"]
    ids: set[str] = set()
    source_sets: set[tuple[str, ...]] = set()
    for index, example in enumerate(manifest["examples"]):
        label = f"examples[{index}]"
        if not isinstance(example, dict):
            errors.append(f"{label} must be an object")
            continue
        ident = example.get("id")
        sources = example.get("sources")
        expected = example.get("expected")
        if not isinstance(ident, str) or not _ID.fullmatch(ident):
            errors.append(f"{label}: invalid target id")
        elif ident in ids:
            errors.append(f"{label}: duplicate id {ident}")
        else:
            ids.add(ident)
        if not isinstance(expected, str) or not expected.strip():
            errors.append(f"{label}: expected output must be a nonempty string")
        if not isinstance(sources, list) or not sources or not all(isinstance(s, str) for s in sources):
            errors.append(f"{label}: sources must be a nonempty array of paths")
            continue
        if len(set(sources)) != len(sources):
            errors.append(f"{label}: duplicate source paths")
        key = tuple(sorted(sources))
        if key in source_sets:
            errors.append(f"{label}: duplicate source group")
        source_sets.add(key)
        for source in sources:
            posix = PurePosixPath(source)
            if (posix.is_absolute() or ".." in posix.parts or "\\" in source
                    or not _CHAPTER.match(posix.parts[0]) or posix.suffix not in BUILDABLE_EXT):
                errors.append(f"{label}: unsafe or unsupported source: {source}")
                continue
            path = root / source
            if not path.is_file() or path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
                errors.append(f"{label}: source absent or symlink: {source}")
            elif is_placeholder(path):
                errors.append(f"{label}: source is a placeholder: {source}")
    return errors


def inventory(root: Path, manifest: dict):
    counts = Counter()
    unregistered = []
    known = {
        s for example in manifest.get("examples", []) if isinstance(example, dict)
        for s in example.get("sources", []) if isinstance(s, str)
    }
    for path in chapter_sources(root):
        suffix = path.suffix
        stub = is_placeholder(path)
        counts[f"{suffix}:placeholder" if stub else f"{suffix}:implemented"] += 1
        if not stub and path.relative_to(root).as_posix() not in known:
            unregistered.append(path.relative_to(root).as_posix())
    return dict(sorted(counts.items())), unregistered


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail on invalid manifest entries")
    parser.add_argument("--json", action="store_true", help="Emit structured JSON report")
    parser.add_argument("--details", action="store_true", help="List implemented but unregistered files")
    args = parser.parse_args()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    errors = validate_manifest(ROOT, manifest)
    counts, unregistered = inventory(ROOT, manifest)
    report = {
        "curated_examples": len(manifest.get("examples", [])),
        "inventory": counts,
        "implemented_not_curated_count": len(unregistered),
        "errors": errors,
    }
    if args.details:
        report["implemented_not_curated"] = unregistered
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"Curated build examples: {report['curated_examples']}")
        for key, value in counts.items():
            print(f"  {key}: {value}")
        print(f"Implemented but not in curated manifest: {len(unregistered)}")
        if args.details:
            for name in unregistered:
                print(f"  unregistered: {name}")
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
    return int(bool(args.check and errors))


if __name__ == "__main__":
    sys.exit(main())
