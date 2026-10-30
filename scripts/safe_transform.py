#!/usr/bin/env python3
"""Preview or explicitly apply a limited Markdown math-delimiter conversion.

No automatic deletion of citations or Chinese bracketed text. Never scans source
code, PDFs, git metadata, or symlinks. Applying always creates a .bak backup.
"""
from __future__ import annotations

import argparse
import difflib
from pathlib import Path


REPLACEMENTS = ((r"\[", "$$"), (r"\]", "$$"), (r"\(", "$"), (r"\)", "$"))


def convert(text: str) -> str:
    for before, after in REPLACEMENTS:
        text = text.replace(before, after)
    return text


def candidates(root: Path):
    root = root.resolve()
    if not root.is_dir():
        raise ValueError(f"Not a directory: {root}")
    for path in sorted(root.rglob("*.md")):
        if ".git" in path.relative_to(root).parts or path.is_symlink() or not path.is_file():
            continue
        if not path.resolve().is_relative_to(root):
            continue
        yield path


def process(root: Path, apply: bool = False, verbose: bool = False) -> dict[str, int]:
    stats = {"scanned": 0, "changed": 0, "applied": 0, "skipped_backup": 0}
    for path in candidates(root):
        stats["scanned"] += 1
        try:
            old = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        new = convert(old)
        if new == old:
            continue
        stats["changed"] += 1
        print(f"{'APPLY' if apply else 'PREVIEW'} {path}")
        if verbose:
            print("".join(difflib.unified_diff(old.splitlines(True), new.splitlines(True),
                                               fromfile=str(path), tofile=str(path) + " (proposed)")))
        if apply:
            backup = path.with_name(path.name + ".bak")
            try:
                with backup.open("xb") as out:
                    out.write(path.read_bytes())
            except FileExistsError:
                stats["skipped_backup"] += 1
                print(f"SKIP (backup already exists): {backup}")
                continue
            path.write_text(new, encoding="utf-8")
            stats["applied"] += 1
    return stats


def main() -> None:
    parser = argparse.ArgumentParser(description="Safe Markdown-only delimiter conversion")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--apply", action="store_true", help="Apply changes and create .bak backups")
    parser.add_argument("--diff", action="store_true", help="Print unified diff")
    args = parser.parse_args()
    stats = process(args.root, apply=args.apply, verbose=args.diff)
    print(" ".join(f"{k}={v}" for k, v in stats.items()))


if __name__ == "__main__":
    main()
