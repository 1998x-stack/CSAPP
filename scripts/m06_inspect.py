#!/usr/bin/env python3
"""Inspect the four compiler stages of the M06 chapter-1 multi-file C lab.

Creates files only under build/m06-inspect. Requires CC, nm, objdump and readelf
on a Linux ELF development host. Never touches the original study notes.
"""
from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / "01_计算机系统概览/m06_build_pipeline"
OUT = ROOT / "build/m06-inspect"


def run(args, *, capture=True):
    result = subprocess.run(args, cwd=ROOT, text=True, capture_output=capture, check=False, timeout=60)
    if result.returncode:
        raise RuntimeError(f"{args!r} failed:\n{result.stdout}\n{result.stderr}")
    return result.stdout


def main():
    compiler = os.environ.get("CC", "cc")
    for tool in (compiler, "nm", "objdump", "readelf"):
        if not shutil.which(tool):
            raise RuntimeError(f"Tool required for M06 inspection: {tool}")
    OUT.mkdir(parents=True, exist_ok=True)
    src = LAB / "pipeline.c"
    driver = LAB / "driver.c"
    preprocessed = OUT / "pipeline.i"
    assembly = OUT / "pipeline.s"
    obj = OUT / "pipeline.o"
    driver_obj = OUT / "driver.o"
    binary = OUT / "pipeline_lab"
    flags = ["-std=c11", "-O0", "-g", "-Wall", "-Wextra", "-Wpedantic", "-Werror"]
    run([compiler, *flags, "-E", str(src), "-o", str(preprocessed)])
    run([compiler, *flags, "-S", str(src), "-o", str(assembly)])
    run([compiler, *flags, "-c", str(src), "-o", str(obj)])
    run([compiler, *flags, "-c", str(driver), "-o", str(driver_obj)])
    run([compiler, str(driver_obj), str(obj), "-o", str(binary)])
    checks = {
        "preprocess": "csapp_m06_pipeline_add" in preprocessed.read_text(encoding="utf-8"),
        "assembly": "csapp_m06_pipeline_add" in assembly.read_text(encoding="utf-8"),
        "object_symbol": "csapp_m06_pipeline_add" in run(["nm", "-g", str(obj)]),
        "disassembly": "csapp_m06_pipeline_add" in run(["objdump", "-d", str(binary)]),
        "elf": "ELF" in run(["readelf", "-h", str(binary)]),
        "runtime": "M06 pipeline: PASS" in run([str(binary)]),
    }
    for stage, ok in checks.items():
        print(f"{stage}: {'PASS' if ok else 'FAIL'}")
    if not all(checks.values()):
        return 1
    print("M06 compiler stages: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
