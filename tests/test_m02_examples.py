"""Run the six repaired chapter-2 C++ teaching examples under UndefinedBehaviorSanitizer.

Run with: CXX=g++ python3 -m unittest discover -s tests -p 'test_m02_*.py' -v
"""
from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "02_程序结构和执行"

# Use observable, invariant output instead of assuming a host endian order or
# that a machine's signed overflow wraps in C++.
CASES = (
    (
        "2.2_整数表示/00_2.2.1_整数数据类型.cpp",
        ("int32_t 最大值 + 1 超出 int32_t 范围: 2147483648",
         "int32_t 最小值 - 1 超出 int32_t 范围: -2147483649",
         "uint8_t (零扩展): 255 -> 255"),
    ),
    (
        "2.2_整数表示/02_2.2.3_二进制补码编码.cpp",
        ("最大值加1发生溢出: 是", "最小值减1发生溢出: 是",
         "按 32 位无符号规则得到的位模式 (+1): 10000000000000000000000000000000",
         "按 32 位无符号规则得到的位模式 (-1): 01111111111111111111111111111111"),
    ),
    (
        "2.2_整数表示/03_2.2.4_有符号和无符号之间的转换.cpp",
        ("按32位补码解释的数学值: -1", "x + y 的无符号结果: ",
         "a < b 的结果: 0", "c < d 的结果: 0"),
    ),
    (
        "2.3_整数运算/00_2.3.1_无符号加法.cpp",
        ("32位加法溢出检测: 是", "8位加法溢出检测: 是",
         "sum: 00101100 (44)"),
    ),
    (
        "2.3_整数运算/01_2.3.2_二进制补码加法.cpp",
        ("数学加法结果 (int64_t): 2500000000",
         "32位加法溢出检测: 是",
         "8位加法溢出检测: 是",
         "8位补码位模式: 10010110，按补码解释: -106",
         "C++ 余数 (-2 % 16): -2", "非负模16: 14"),
    ),
    (
        "2.3_整数运算/02_2.3.3_二进制补码求反.cpp",
        ("求反溢出检测: 否", "8位求反溢出检测: 否",
         "数学求反结果 (int64_t): 2147483648",
         "最小负数求反溢出检测: 是",
         "32位无符号模运算位模式: 10000000000000000000000000000000"),
    ),
)


class TestM02IntegerExamples(unittest.TestCase):
    def test_all_examples_with_ubsan(self):
        cxx = os.environ.get("CXX", "g++")
        compiler = shutil.which(cxx)
        if compiler is None:
            self.skipTest(f"Compiler not found: {cxx}")
        with tempfile.TemporaryDirectory(prefix="csapp-m02-") as tmp:
            for index, (name, expected) in enumerate(CASES):
                with self.subTest(source=name, compiler=cxx):
                    source = CHAPTER / name
                    self.assertTrue(source.is_file(), f"Missing sample: {source}")
                    executable = Path(tmp) / f"sample_{index}"
                    compile_result = subprocess.run(
                        [
                            compiler, "-std=c++17", "-O1", "-g",
                            "-Wall", "-Wextra", "-Wpedantic", "-Werror",
                            "-fsanitize=undefined", "-fno-sanitize-recover=all",
                            str(source), "-o", str(executable),
                        ],
                        text=True, capture_output=True, check=False,
                        timeout=60,
                    )
                    self.assertEqual(
                        compile_result.returncode, 0,
                        f"Compile failed: {source}\n{compile_result.stdout}\n{compile_result.stderr}",
                    )
                    run_result = subprocess.run(
                        [str(executable)], text=True, capture_output=True,
                        check=False, timeout=15,
                        env={**os.environ, "UBSAN_OPTIONS": "halt_on_error=1:print_stacktrace=1"},
                    )
                    self.assertEqual(
                        run_result.returncode, 0,
                        f"Run failed: {source}\n{run_result.stdout}\n{run_result.stderr}",
                    )
                    self.assertNotIn("runtime error:", run_result.stderr)
                    for marker in expected:
                        self.assertIn(marker, run_result.stdout, f"Missing expected output from {source}")


if __name__ == "__main__":
    unittest.main()
