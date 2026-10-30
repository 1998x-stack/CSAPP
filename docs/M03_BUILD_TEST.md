# M03：统一构建、测试与源码清单

## 目的和范围

本模块提供非破坏性 C/C++/x86-64 汇编构建入口。仓库目前保留数百个源代码模板，**不应该**自动把所有 .cpp 文件加入编译；清单只列入已经人工审核的实际示例。

### 前置环境

- CMake 3.20+，Python 3.9+，支持 C11 与 C++17 的 GCC 或 Clang。
- x86-64 汇编烟雾测试仅在 **Linux x86-64 / System V ABI** 环境构建；其他平台自动跳过（C/C++ 仍可构建）。
- 不依赖第三方 Python 包，Ubuntu GitHub Actions 使用 GCC 与 Clang 两种工具链。
- UBSan 需要 GCC/Clang，默认关闭，以便本地普通构建。CI 会启用。

## 统一构建与测试命令

在仓库根目录执行：

```bash
# 审核清单：只读取目录和 JSON，不修改源码
python3 scripts/audit_sources.py --check
python3 scripts/audit_sources.py --json
python3 scripts/audit_sources.py --details

# 构建所有登记过的独立示例和两个编译器 smoke test
cmake -S . -B build/m03 -DCMAKE_BUILD_TYPE=Debug -DCSAPP_ENABLE_UBSAN=ON
cmake --build build/m03 --parallel 2

# 运行 CTest：6 个 C++ 示例 + 1 个 C 烟雾测试 + Linux x86-64 汇编烟雾测试
ctest --test-dir build/m03 --output-on-failure

# 运行跨模块的 Python 回归测试
python3 -m unittest discover -s tests -v
```

### 清单格式

`examples/manifest.json`（schema_version = 1）：

```json
{
  "id": "ch02_integer_types",
  "sources": ["02_程序结构和执行/2.2_整数表示/00_2.2.1_整数数据类型.cpp"],
  "expected": "int32_t 最大值 + 1 超出 int32_t 范围: 2147483648"
}
```

这是 `examples` 数组中的一条记录。每个目标使用独立的 `id`，一个或多个 `sources`，及至少一个用于 CTest 输出检查的 `expected` 正则表达式。目录路径必须相对仓库根目录，位于教材章节范围内；禁止路径穿越与符号链接。新增实验在经审查和测试后登记到此清单，不必更改整个 CMakeLists.txt。

目前 M02 已审查的六个 C++ 示例是首次纳入清单的教学目标；`tests/fixtures` 中的 C/ASM 程序仅验证编译环境，不算完成 CSAPP 实验。

### 代码与模板的区分

`scripts/audit_sources.py` 读取章节下的 .c/.cc/.cpp/.cxx/.s/.S/.py 文件，粗略归类：
- `placeholder`：只有注释或模块 docstring，没有实际程序内容。
- `implemented`：含有代码内容，但**未必编译成功或行为正确**。
- `implemented_not_curated_count`：已写代码但尚未通过审查、未加入构建清单的源文件数量。

这些指标是**进度观察工具**，不是完成度评分。新增加的实验目标必须先通过编译、测试和人工审查。

## 验收清单

- 清单中 6 个已修复 C++ 程序都可以由 CMake 编译并通过 CTest。
- C 与 Linux x86-64 AT&T 汇编样例可编译、链接并运行，能验证基本的 System V 调用约定。
- GCC/Clang 分别完成 `-Wall -Wextra -Wpedantic -Werror` + UBSan 构建和测试。
- `python3 -m unittest discover -s tests -v` 的 M01、M02、M03 测试不相互冲突。
- 新系统不会删除、覆盖或重命名既有课程文件。
- `build/` 被 git 忽略；关闭 PR / revert 提交即可回退本模块。

## 下一步

M04 将统一教材目录和知识点标识。M06–M09 再逐章补充真实的 C / 汇编 / Linux 系统实验。M03 只交付可验证的工程基础，不虚报各章覆盖率。
