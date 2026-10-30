#!/usr/bin/env python3
"""Compile and examine a tiny static library, relocation references and ELF."""
from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / "07_链接/m08_static_link"
OUT = ROOT / "build/m08-link-inspect"


def run(*cmd):
    result = subprocess.run(cmd, text=True, capture_output=True, check=False, timeout=60)
    if result.returncode:
        raise RuntimeError(f"{cmd!r}: {result.stderr}\n{result.stdout}")
    return result.stdout


def main():
    cc = os.environ.get("CC", "cc")
    for tool in (cc, "ar", "nm", "readelf", "objdump"):
        if shutil.which(tool) is None:
            raise RuntimeError(f"M08 linker inspection requires {tool}")
    OUT.mkdir(parents=True, exist_ok=True)
    main_o = OUT / "main.o"
    arith_o = OUT / "arith.o"
    library = OUT / "libm08arith.a"
    executable = OUT / "m08_linker"
    flags = ["-std=c11", "-O0", "-g", "-Wall", "-Wextra", "-Wpedantic", "-Werror"]
    run(cc, *flags, "-c", str(LAB / "main.c"), "-o", str(main_o))
    run(cc, *flags, "-c", str(LAB / "arith.c"), "-o", str(arith_o))
    run("ar", "rcs", str(library), str(arith_o))
    undefined = run("nm", "-u", str(main_o))
    defined = run("nm", "-g", "--defined-only", str(library))
    archive = run("ar", "t", str(library))
    relocations = run("readelf", "-r", str(main_o))
    run(cc, str(main_o), str(library), "-o", str(executable))
    elf = run("readelf", "-h", str(executable))
    disassembly = run("objdump", "-d", str(executable))
    result = run(str(executable))
    checks = {
        "unresolved reference before linking": "m08_sum_3" in undefined,
        "defined library symbol": "m08_sum_3" in defined,
        "archive member": "arith.o" in archive,
        "relocation entry": "m08_sum_3" in relocations,
        "ELF format": "ELF" in elf,
        "disassembled function": "m08_sum_3" in disassembly,
        "executed": "M08 linker: PASS" in result,
    }
    for item, ok in checks.items():
        print(f"{item}: {'PASS' if ok else 'FAIL'}")
    if not all(checks.values()):
        return 1
    print("M08 static linker inspection: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
