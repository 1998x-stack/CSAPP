#!/usr/bin/env python3
"""CSAPP Global Edition TOC coverage: read-only by default, --write generated metadata."""
from __future__ import annotations

import argparse
import ast
from collections import Counter
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
OUTLINE = ROOT / "curriculum/book_outline.json"
CATALOG = ROOT / "curriculum/catalog.json"
REPORT = ROOT / "docs/M04_COVERAGE.md"
EXTS = (".md", ".py", ".cpp", ".html")
EXPECTED_PER_CHAPTER = (19, 36, 58, 36, 26, 26, 23, 29, 55, 14, 23, 33)
ID = re.compile(r"(?<!\d)((?:1[0-2]|[1-9])\.\d+(?:\.\d+)?)(?=_|$)")


def clean(value):
    return value.replace(" ", "_").replace("/", "_").replace("-", "_").replace("\\", "_")


def numbered_id(name):
    match = ID.search(name)
    if not match:
        raise ValueError(f"No section ID in {name!r}")
    return match.group(1)


def outline_ids(book):
    chapters = book.get("chapters", [])
    if [item.get("id") for item in chapters] != [str(x) for x in range(1, 13)]:
        raise ValueError("All 12 numbered chapters must appear in order")
    if len({item.get("repository_root") for item in chapters}) != 12:
        raise ValueError("Chapter roots must be unique")
    ids = []
    for ch, expected in zip(chapters, EXPECTED_PER_CHAPTER):
        groups = ch.get("subsection_counts")
        if (not isinstance(groups, list) or not groups or
                any(type(n) is not int or n < 0 for n in groups)):
            raise ValueError(f"Invalid subsections for chapter {ch['id']}")
        current = []
        for section, count in enumerate(groups, 1):
            label = f"{ch['id']}.{section}"
            current.append(label)
            current.extend(f"{label}.{subsection}" for subsection in range(1, count + 1))
        if len(current) != expected:
            raise ValueError(f"Chapter {ch['id']}: expected {expected}, got {len(current)}")
        if not ch.get("unnumbered_materials"):
            raise ValueError(f"Unnumbered materials absent in chapter {ch['id']}")
        ids.extend(current)
    if len(ids) != 378 or len(set(ids)) != 378 or book.get("expected_numbered_entries") != 378:
        raise ValueError("Book outline must contain exactly 378 distinct numbered chapter entries")
    appendix = book.get("appendix", {})
    if appendix.get("id") != "A" or appendix.get("numbered_entries") != ["A.1", "A.2"]:
        raise ValueError("Appendix A.1 and A.2 must be present")
    return ids + ["A.1", "A.2"]


def parse_main_structure():
    parsed = ast.parse((ROOT / "main.py").read_text(encoding="utf-8"))
    for node in parsed.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "structure" for target in node.targets
        ):
            return ast.literal_eval(node.value)
    raise ValueError("main.py structure dictionary not found")


def source_topics(structure):
    topics = {}
    def add(title, directory):
        stem = clean(title)
        number = numbered_id(stem)
        if number in topics:
            raise ValueError(f"Duplicate repository topic {number}")
        base = (directory / stem).as_posix()
        extensions = []
        for extension in EXTS:
            path = ROOT / (base + extension)
            if path.is_symlink():
                raise ValueError(f"Unexpected linked topic file: {path}")
            if path.is_file():
                extensions.append(extension)
        if tuple(extensions) != EXTS:
            raise ValueError(f"Incomplete four-file topic {number}: {extensions}")
        topics[number] = {
            "topic_base": base,
            "file_extensions": extensions,
            "title_zh": re.sub(r"^(?:\d{2}_)?\d+\.\d+(?:\.\d+)?_", "", title).replace("_", " "),
        }

    def descend(mapping, parent):
        for title, children in mapping.items():
            directory = parent / clean(title)
            if isinstance(children, dict) and children:
                descend(children, directory)
            elif isinstance(children, list) and children:
                for i, child in enumerate(children):
                    if isinstance(child, dict) and child:
                        descend(child, directory)
                    elif isinstance(child, str):
                        add(f"{i:02d}_{child}", directory)
                    else:
                        raise ValueError(f"Unexpected entry under {directory}: {child!r}")
            else:
                add(title, directory)
    descend(structure, Path())
    return topics


def build_catalog():
    book = json.loads(OUTLINE.read_text(encoding="utf-8"))
    expected = outline_ids(book)
    topics = source_topics(parse_main_structure())
    if len(topics) != 310 or not set(topics).issubset(set(expected)):
        raise ValueError("Source structure is no longer the 310 canonical TOC leaves; review changes")

    for chapter in book["chapters"]:
        if not (ROOT / chapter["repository_root"]).is_dir():
            raise ValueError(f"Chapter directory missing: {chapter['repository_root']}")

    # Register every parent section represented by a real grouping directory.
    directories = {}
    indexed = set()
    for topic in topics.values():
        base = Path(topic["topic_base"])
        indexed.update(base.as_posix() + ext for ext in EXTS)
        for depth in range(2, len(base.parts)):
            folder = base.parts[depth - 1]
            match = re.match(r"^((?:1[0-2]|[1-9])\.\d+)_", folder)
            if match:
                number = match.group(1)
                directory = Path(*base.parts[:depth]).as_posix()
                if number in directories and directories[number] != directory:
                    raise ValueError(f"Multiple grouping folders for {number}")
                directories[number] = directory

    extras = []
    for chapter in book["chapters"]:
        for path in sorted((ROOT / chapter["repository_root"]).rglob("*")):
            if not path.is_file() or path.is_symlink() or path.suffix not in EXTS:
                continue
            relative = path.relative_to(ROOT).as_posix()
            if relative not in indexed:
                extras.append({
                    "path": relative,
                    "related_section": numbered_id(path.parent.name),
                })

    entries = []
    for number in expected:
        chapter_id = number.split(".")[0]
        entry = {"id": number, "chapter_id": chapter_id}
        if number in topics:
            entry.update({"status": "topic_files", **topics[number]})
        elif number in directories:
            entry.update({"status": "section_directory", "directory": directories[number]})
        else:
            entry.update({"status": "unmapped"})
        entries.append(entry)

    chapters = []
    for book_chapter in book["chapters"]:
        belonging = [entry for entry in entries if entry["chapter_id"] == book_chapter["id"]]
        counts = Counter(entry["status"] for entry in belonging)
        chapters.append({
            "id": book_chapter["id"],
            "title_zh": book_chapter["title_zh"],
            "expected": len(belonging),
            "topic_files": counts["topic_files"],
            "section_directory": counts["section_directory"],
            "unmapped": counts["unmapped"],
        })
    tally = Counter(entry["status"] for entry in entries)
    return {
        "schema_version": 1,
        "outline_source": "curriculum/book_outline.json",
        "status_legend": {
            "topic_files": "Four files are present; their existence does not imply completed knowledge or tested code",
            "section_directory": "Book section exists as a grouping directory with child topics, not an independent article",
            "unmapped": "Numbered book entry has no matching topic files or grouping directory",
        },
        "totals": {
            "chapters": 12, "book_numbered": 378, "appendix_numbered": 2,
            "topic_files": tally["topic_files"],
            "section_directory": tally["section_directory"],
            "unmapped": tally["unmapped"], "supplementary_files": len(extras),
        },
        "chapters": chapters, "entries": entries,
        "supplementary_files": extras,
        "unnumbered_materials": {c["id"]: c["unnumbered_materials"] for c in book["chapters"]},
        "appendix": book["appendix"],
        "front_matter": book["front_matter"],
        "back_matter": book["back_matter"],
    }


def report_text(data):
    t = data["totals"]
    lines = [
        "# M04：CSAPP 第三版教材目录全量覆盖报告", "",
        "本报告由 scripts/build_curriculum.py 自动生成，基准为第三版 Global Edition 的目录编号。",
        "目录元数据不含教材正文或练习答案。已有目录名称不会被本模块改动。", "",
        "## 统计口径", "",
        "- topic_files：四种对应文件均存在，但不表示讲解或代码已完成。",
        "- section_directory：目录存在且含下级知识点，但没有独立知识文件。",
        "- unmapped：原书目录编号缺少对应的知识文件或目录。",
        "- 附录 A.1 / A.2 同样收录；额外参考资料单独保存。", "",
        f"**12 章、{t['book_numbered']} 个带编号目录项、附录 2 项。**", "",
        "| 章节 | 教材条目 | 文件知识点 | 父节目录 | 未映射 |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for chapter in data["chapters"]:
        lines.append(f"| {chapter['id']} {chapter['title_zh']} | {chapter['expected']} | {chapter['topic_files']} | {chapter['section_directory']} | {chapter['unmapped']} |")
    missing = [e["id"] for e in data["entries"] if e["status"] == "unmapped"]
    parents = [e["id"] for e in data["entries"] if e["status"] == "section_directory"]
    lines += [
        "", "## 尚未映射的教材编号", "",
        ", ".join(missing) if missing else "无", "",
        "## 有目录、无独立文章的父节编号", "",
        ", ".join(parents) if parents else "无", "",
        "## 已存在但不属于标准四文件组的补充资料", "",
    ]
    for extra in data["supplementary_files"]:
        lines.append(f"- {extra['path']} （归属 {extra['related_section']}）")
    lines += [
        "", "## 重要边界", "",
        "各章文献注释、作业题、习题解答及前言、参考文献、索引均在 book_outline.json 中登记类别，",
        "但此目录层级无法逐题核实原书每个旁栏、图表或练习；不应将文件存在当作内容已完成。",
        "", "## 校验与更新", "",
        "默认运行 python3 scripts/build_curriculum.py 只打印统计。",
        "CI 运行 python3 scripts/build_curriculum.py --check 检查目录漂移。",
        "有意变更目录时执行 python3 scripts/build_curriculum.py --write，仅重新生成 catalog.json 与此报告。",
        "",
    ]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    g = parser.add_mutually_exclusive_group()
    g.add_argument("--check", action="store_true")
    g.add_argument("--write", action="store_true")
    args = parser.parse_args()
    catalog = build_catalog()
    content = json.dumps(catalog, ensure_ascii=False, indent=2) + "\n"
    report = report_text(catalog)
    print(json.dumps(catalog["totals"], ensure_ascii=False, sort_keys=True))
    if args.write:
        CATALOG.write_text(content, encoding="utf-8")
        REPORT.write_text(report, encoding="utf-8")
        return 0
    if args.check:
        changed = [str(path) for path, expected in ((CATALOG, content), (REPORT, report))
                   if not path.is_file() or path.read_text(encoding="utf-8") != expected]
        if changed:
            print(f"Curriculum map drift: {changed}", file=sys.stderr)
            return 1
        print("Book TOC, source structure, curriculum map and supplementary files match")
    return 0


if __name__ == "__main__":
    sys.exit(main())
