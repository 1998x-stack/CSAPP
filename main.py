structure = {
    "01_计算机系统概览": [
        {
            "1.1_信息是位+上下文": []
        },
        {
            "1.2_程序被其他程序翻译成不同的形式": []
        },
        {
            "1.3_了解编译系统的工作原理是有益的": []
        },
        {
            "1.4_处理器读取并解释存储在内存中的指令": [
                "1.4.1_系统的硬件组织",
                "1.4.2_运行_hello_程序"
            ]
        },
        {
            "1.5_缓存很重要": []
        },
        {
            "1.6_存储设备形成一个层次结构": []
        },
        {
            "1.7_操作系统管理硬件": [
                "1.7.1_进程",
                "1.7.2_线程",
                "1.7.3_虚拟内存",
                "1.7.4_文件"
            ]
        },
        {
            "1.8_系统通过网络与其他系统通信": []
        },
        {
            "1.9_重要主题": [
                "1.9.1_阿姆达尔定律",
                "1.9.2_并发和并行",
                "1.9.3_计算机系统中抽象的重要性"
            ]
        },
        
        
    ],
    "02_程序结构和执行": [
        {
            "2.1_表示和操作信息": [
                "2.1.1_十六进制表示法",
                "2.1.2_数据大小",
                "2.1.3_地址和字节顺序",
                "2.1.4_表示字符串",
                "2.1.5_表示代码",
                "2.1.6_布尔代数简介",
                "2.1.7_C语言中的位级操作",
                "2.1.8_C语言中的逻辑操作",
                "2.1.9_C语言中的移位操作"
            ]
        },
        {
            "2.2_整数表示": [
                "2.2.1_整数数据类型",
                "2.2.2_无符号编码",
                "2.2.3_二进制补码编码",
                "2.2.4_有符号和无符号之间的转换",
                "2.2.5_C语言中的有符号与无符号",
                "2.2.6_扩展数字的位表示",
                "2.2.7_截断数字",
                "2.2.8_有符号和无符号的建议"
            ]
        },
        {
            "2.3_整数运算": [
                "2.3.1_无符号加法",
                "2.3.2_二进制补码加法",
                "2.3.3_二进制补码求反",
                "2.3.4_无符号乘法",
                "2.3.5_二进制补码乘法",
                "2.3.6_用常数乘法",
                "2.3.7_除以2的幂",
                "2.3.8_整数运算的最后思考"
            ]
        },
        {
            "2.4_浮点数": [
                "2.4.1_分数二进制数",
                "2.4.2_IEEE浮点表示",
                "2.4.3_数字示例",
                "2.4.4_舍入",
                "2.4.5_浮点运算",
                "2.4.6_C语言中的浮点"
            ]
        },
    ],
    "03_程序的机器级表示": [
        {
            "3.1_历史视角": []
        },
        {
            "3.2_程序编码": [
                "3.2.1_机器级代码",
                "3.2.2_代码示例",
                "3.2.3_格式化注意事项"
            ]
        },
        {
            "3.3_数据格式": []
        },
        {
            "3.4_访问信息": [
                "3.4.1_操作数说明符",
                "3.4.2_数据移动指令",
                "3.4.3_数据移动示例",
                "3.4.4_推入和弹出栈数据"
            ]
        },
        {
            "3.5_算术和逻辑运算": [
                "3.5.1_加载有效地址",
                "3.5.2_一元和二元运算",
                "3.5.3_移位运算",
                "3.5.4_讨论",
                "3.5.5_特殊算术运算"
            ]
        },
        {
            "3.6_控制": [
                "3.6.1_条件码",
                "3.6.2_访问条件码",
                "3.6.3_跳转指令",
                "3.6.4_跳转指令编码",
                "3.6.5_用条件控制实现条件分支",
                "3.6.6_用条件移动实现条件分支",
                "3.6.7_循环",
                "3.6.8_开关语句"
            ]
        },
        {
            "3.7_程序": [
                "3.7.1_运行时栈",
                "3.7.2_控制转移",
                "3.7.3_数据转移",
                "3.7.4_栈上的局部存储",
                "3.7.5_寄存器中的局部存储",
                "3.7.6_递归程序"
            ]
        },
        {
            "3.8_数组分配和访问": [
                "3.8.1_基本原理",
                "3.8.2_指针运算",
                "3.8.3_嵌套数组",
                "3.8.4_固定大小数组",
                "3.8.5_可变大小数组"
            ]
        },
        {
            "3.9_异质数据结构": [
                "3.9.1_结构体",
                "3.9.2_联合",
                "3.9.3_数据对齐"
            ]
        },
        {
            "3.10_在机器级程序中结合控制和数据": [
                "3.10.1_理解指针",
                "3.10.2_现实生活中的使用：使用_gdb_调试器",
                "3.10.3_越界内存引用和缓冲区溢出",
                "3.10.4_防止缓冲区溢出攻击",
                "3.10.5_支持可变大小的栈帧"
            ]
        },
        {
            "3.11_浮点代码": [
                "3.11.1_浮点移动和转换操作",
                "3.11.2_程序中的浮点代码",
                "3.11.3_浮点算术运算",
                "3.11.4_定义和使用浮点常量",
                "3.11.5_在浮点代码中使用位操作",
                "3.11.6_浮点比较运算",
                "3.11.7_关于浮点代码的观察"
            ]
        },
        
        
    ],
    "04_处理器架构": [
        {
            "4.1_Y86-64指令集架构": [
                "4.1.1_程序员可见状态",
                "4.1.2_Y86-64指令",
                "4.1.3_指令编码",
                "4.1.4_Y86-64异常",
                "4.1.5_Y86-64程序",
                "4.1.6_一些Y86-64指令细节"
            ]
        },
        {
            "4.2_逻辑设计和硬件控制语言HCL": [
                "4.2.1_逻辑门",
                "4.2.2_组合电路和HCL布尔表达式",
                "4.2.3_字级组合电路和HCL整数表达式",
                "4.2.4_集合成员关系",
                "4.2.5_存储器和时钟"
            ]
        },
        {
            "4.3_顺序Y86-64实现": [
                "4.3.1_将处理组织成阶段",
                "4.3.2_SEQ硬件结构",
        "4.3.3_SEQ计时",
        "4.3.4_SEQ阶段实现"
        ]
        },
        {
        "4.4_流水线的一般原理": [
        "4.4.1_计算流水线",
        "4.4.2_详细了解流水线操作",
        "4.4.3_流水线的限制",
        "4.4.4_带反馈的系统流水线"
        ]
        },
        {
        "4.5_流水线Y86-64实现": [
        "4.5.1_SEQ+:_重排计算阶段",
        "4.5.2_插入流水线寄存器",
        "4.5.3_重排和重新标记信号",
        "4.5.4_下一PC预测",
        "4.5.5_流水线冒险",
        "4.5.6_异常处理",
        "4.5.7_PIPE阶段实现",
        "4.5.8_流水线控制逻辑",
        "4.5.9_性能分析",
        "4.5.10_未完成的业务"
        ]
        },
        
        
        ],
        "05_优化程序性能": [
        {
        "5.1_优化编译器的能力和限制": []
        },
        {
        "5.2_表达程序性能": []
        },
        {
        "5.3_程序示例": []
        },
        {
        "5.4_消除循环低效": []
        },
        {
        "5.5_减少过程调用": []
        },
        {
        "5.6_消除不需要的内存引用": []
        },
        {
        "5.7_理解现代处理器": [
        "5.7.1_整体操作",
        "5.7.2_功能单元性能",
        "5.7.3_处理器操作的抽象模型"
        ]
        },
        {
        "5.8_循环展开": []
        },
        {
        "5.9_增强并行性": [
        "5.9.1_多累加器",
        "5.9.2_重关联变换"
        ]
        },
        {
        "5.10_优化组合代码结果总结": []
        },
        {
        "5.11_一些限制因素": [
        "5.11.1_寄存器溢出",
        "5.11.2_分支预测和错误预测惩罚"
        ]
        },
        {
        "5.12_理解内存性能": [
        "5.12.1_加载性能",
        "5.12.2_存储性能"
        ]
        },
        {
        "5.13_现实生活中的性能改进技术": []
        },
        {
        "5.14_识别和消除性能瓶颈": [
        "5.14.1_程序剖析",
        "5.14.2_使用剖析器指导优化"
        ]
        },
        
        
        ],
        "06_内存层次结构": [
        {
        "6.1_存储技术": [
        "6.1.1_随机存取存储器",
        "6.1.2_磁盘存储",
        "6.1.3_固态硬盘",
        "6.1.4_存储技术趋势"
        ]
        },
        {
        "6.2_局部性": [
        "6.2.1_程序数据的局部性",
        "6.2.2_指令获取的局部性",
        "6.2.3_局部性总结"
        ]
        },
        {
        "6.3_内存层次结构": [
        "6.3.1_内存层次结构中的缓存",
        "6.3.2_内存层次结构概念总结"
        ]
        },
        {
        "6.4_缓存存储器": [
        "6.4.1_通用缓存存储器组织",
        "6.4.2_直接映射缓存",
        "6.4.3_组关联缓存",
        "6.4.4_完全关联缓存",
        "6.4.5_写操作问题",
        "6.4.6_实际缓存层次结构的解剖",
        "6.4.7_缓存参数对性能的影响"
        ]
        },
        {
        "6.5_编写缓存友好的代码": []
        },
        {
        "6.6_综合:缓存对程序性能的影响": [
        "6.6.1_内存山",
        "6.6.2_重排循环以增加空间局部性",
        "6.6.3_在程序中利用局部性"
        ]
        },
        
        
        ],
        "07_链接": [
        {
        "7.1_编译器驱动程序": []
        },
        {
        "7.2_静态链接": []
        },
        {
        "7.3_目标文件": []
        },
        {
        "7.4_可重定位目标文件": []
        },
        {
        "7.5_符号和符号表": []
        },
        {
        "7.6_符号解析": [
        "7.6.1_链接器如何解析重复的符号名称",
        "7.6.2_使用静态库进行链接",
        "7.6.3_链接器如何使用静态库解析引用"
        ]
        },
        {
        "7.7_重定位": [
        "7.7.1_重定位条目",
        "7.7.2_重定位符号引用"
        ]
        },
        {
        "7.8_可执行目标文件": []
        },
        {
        "7.9_加载可执行目标文件": []
        },
        {
        "7.10_使用共享库进行动态链接": []
        },
        {
        "7.11_从应用程序加载和链接共享库": []
        },
        {
        "7.12_位置无关代码(PIC)": []
        },
        {
        "7.13_库插入": [
        "7.13.1_编译时插入",
        "7.13.2_链接时插入",
        "7.13.3_运行时插入"
        ]
        },
        {
        "7.14_操作目标文件的工具": []
        },
        
        
        ],
        "08_异常控制流": [
        {
        "8.1_异常": [
        "8.1.1_异常处理",
        "8.1.2_异常类别",
        "8.1.3_Linux/x86-64系统中的异常"
        ]
        },
        {
        "8.2_进程": [
        "8.2.1_逻辑控制流",
        "8.2.2_并发流",
        "8.2.3_私有地址空间",
        "8.2.4_用户模式和内核模式",
        "8.2.5_上下文切换"
        ]
        },
        {
        "8.3_系统调用错误处理": []
        },
        {
        "8.4_进程控制": [
        "8.4.1_获取进程ID",
        "8.4.2_创建和终止进程",
        "8.4.3_收割子进程",
        "8.4.4_使进程休眠",
        "8.4.5_加载和运行程序",
        "8.4.6_使用fork和execve运行程序"
        ]
        },
        {
        "8.5_信号": [
        "8.5.1_信号术语",
        "8.5.2_发送信号",
        "8.5.3_接收信号",
        "8.5.4_阻塞和解除阻塞信号",
        "8.5.5_编写信号处理程序",
        "8.5.6_同步流以避免恶劣的并发错误",
        "8.5.7_显式等待信号"
        ]
        },
        {
        "8.6_非本地跳转": []
        },
        {
        "8.7_操作进程的工具": []
        },
        
        
        ],
    "09_虚拟内存": [
        {
            "9.1_物理地址和虚拟地址": []
        },
        {
            "9.2_地址空间": []
        },
        {
            "9.3_虚拟内存作为缓存工具": [
                "9.3.1_DRAM缓存组织",
                "9.3.2_页表",
                "9.3.3_页命中",
                "9.3.4_页错误",
                "9.3.5_分配页",
                "9.3.6_再次救援的局部性"
            ]
        },
        {
            "9.4_虚拟内存作为内存管理工具": []
        },
        {
            "9.5_虚拟内存作为内存保护工具": []
        },
        {
            "9.6_地址转换": [
                "9.6.1_整合缓存和虚拟内存",
                "9.6.2_使用TLB加速地址转换",
                "9.6.3_多级页表",
                "9.6.4_综合：端到端地址转换"
            ]
        },
        {
            "9.7_案例研究：Intel_Core_i7/Linux_内存系统": [
                "9.7.1_Core_i7地址转换",
                "9.7.2_Linux虚拟内存系统"
            ]
        },
        {
            "9.8_内存映射": [
                "9.8.1_重新审视共享对象",
                "9.8.2_重新审视fork函数",
                "9.8.3_重新审视execve函数",
                "9.8.4_使用mmap函数进行用户级内存映射"
            ]
        },
        {
            "9.9_动态内存分配": [
                "9.9.1_malloc和free函数",
                "9.9.2_为什么需要动态内存分配？",
                "9.9.3_分配器的要求和目标",
                "9.9.4_碎片化",
                "9.9.5_实现问题",
                "9.9.6_隐式空闲链表",
                "9.9.7_放置已分配的块",
                "9.9.8_拆分空闲块",
                "9.9.9_获取额外的堆内存",
                "9.9.10_合并空闲块",
                "9.9.11_使用边界标记进行合并",
                "9.9.12_综合：实现一个简单的分配器",
                "9.9.13_显式空闲链表",
                "9.9.14_分离空闲链表"
            ]
        },
        {
            "9.10_垃圾回收": [
                "9.10.1_垃圾回收器基础",
                "9.10.2_标记-清除垃圾回收器",
                "9.10.3_C程序的保守标记-清除"
            ]
        },
        {
            "9.11_C程序中常见的内存相关错误": [
                "9.11.1_解引用错误指针",
                "9.11.2_读取未初始化内存",
                "9.11.3_允许栈缓冲区溢出",
                "9.11.4_假定指针和它们指向的对象大小相同",
                "9.11.5_越界错误",
                "9.11.6_引用指针而不是它指向的对象",
                "9.11.7_误解指针运算",
                "9.11.8_引用不存在的变量",
                "9.11.9_引用空闲堆块中的数据",
                "9.11.10_引入内存泄漏"
            ]
        },
        
        
    ],
    "10_系统级I/O": [
        {
            "10.1_Unix_I/O": []
        },
        {
            "10.2_文件": []
        },
        {
            "10.3_打开和关闭文件": []
        },
        {
            "10.4_读取和写入文件": []
        },
        {
            "10.5_使用Rio包进行稳健的读取和写入": [
                "10.5.1_Rio无缓冲输入输出函数",
                "10.5.2_Rio缓冲输入函数"
            ]
        },
        {
            "10.6_读取文件元数据": []
        },
        {
            "10.7_读取目录内容": []
        },
        {
            "10.8_共享文件": []
        },
        {
            "10.9_I/O重定向": []
        },
        {
            "10.10_标准I/O": []
        },
        {
            "10.11_综合：我应该使用哪些I/O函数？": []
        },
        
        
    ],
    "11_网络编程": [
        {
            "11.1_客户端-服务器编程模型": []
        },
        {
            "11.2_网络": []
        },
        {
            "11.3_全球IP互联网": [
                "11.3.1_IP地址",
                "11.3.2_互联网域名",
                "11.3.3_互联网连接"
            ]
        },
        {
            "11.4_套接字接口": [
                "11.4.1_套接字地址结构",
                "11.4.2_套接字函数",
                "11.4.3_连接函数",
                "11.4.4_绑定函数",
                "11.4.5_监听函数",
                "11.4.6_接受函数",
                "11.4.7_主机和服务转换",
                "11.4.8_套接字接口辅助函数",
                "11.4.9_回显客户端和服务器示例"
            ]
        },
        {
            "11.5_Web服务器": [
                "11.5.1_Web基础",
                "11.5.2_Web内容",
                "11.5.3_HTTP事务",
                "11.5.4_提供动态内容"
            ]
        },
        {
            "11.6_综合：Tiny_Web服务器": []
        },
        
        
    ],
    "12_并发编程": [
        {
            "12.1_使用进程进行并发编程": [
                "12.1.1_基于进程的并发服务器",
                "12.1.2_进程的优缺点"
            ]
        },
        {
            "12.2_使用I/O多路复用进行并发编程": [
                "12.2.1_基于I/O多路复用的并发事件驱动服务器",
                "12.2.2_I/O多路复用的优缺点"
            ]
        },
        {
            "12.3_使用线程进行并发编程": [
                "12.3.1_线程执行模型",
                "12.3.2_POSIX线程",
                "12.3.3_创建线程",
                "12.3.4_终止线程",
                "12.3.5_回收已终止的线程",
                "12.3.6_分离线程",
                "12.3.7_初始化线程",
                "12.3.8_基于线程的并发服务器"
            ]
        },
        {
            "12.4_线程程序中的共享变量": [
                "12.4.1_线程内存模型",
                "12.4.2_将变量映射到内存",
                "12.4.3_共享变量"
            ]
        },
        {
            "12.5_使用信号量同步线程": [
                "12.5.1_进度图",
                "12.5.2_信号量",
                "12.5.3_使用信号量进行互斥",
                "12.5.4_使用信号量调度共享资源",
                "12.5.5_综合：基于预线程的并发服务器"
            ]
        },
        {
            "12.6_使用线程实现并行性": []
        },
        {
            "12.7_其他并发问题": [
                "12.7.1_线程安全",
                "12.7.2_重入性",
                "12.7.3_在线程程序中使用现有库函数",
                "12.7.4_竞态条件",
                "12.7.5_死锁"
            ]
        },
    ]
}



import argparse
from pathlib import Path
from typing import Any, Iterator


# The chapter structure above remains the single source of truth for scaffolding.
# Never overwrite existing course notes, examples, or README.md.
def _safe_name(value: str) -> str:
    name = value.replace(" ", "_").replace("/", "_").replace("-", "_").replace("\\", "_")
    if name in {"", ".", ".."} or name.startswith("."):
        raise ValueError(f"Unsafe course entry name: {value!r}")
    return name


def iter_scaffold_files(course_structure: dict[str, Any]) -> Iterator[tuple[Path, str]]:
    """Yield (relative_path, template) pairs; do not mutate the filesystem."""
    def walk(items: dict[str, Any], parent: Path, lecture_parts: tuple[str, ...]):
        for title, children in items.items():
            directory = parent / _safe_name(title)
            lecture = lecture_parts + (title,)
            if isinstance(children, dict) and children:
                yield from walk(children, directory, lecture)
            elif isinstance(children, list) and children:
                for index, child in enumerate(children):
                    if isinstance(child, dict) and child:
                        yield from walk(child, directory, lecture)
                    elif isinstance(child, str):
                        yield from emit(directory, lecture, f"{index:02d}_{child}")
                    else:
                        raise ValueError(f"Unexpected course entry under {title}: {child!r}")
            else:
                yield from emit(directory, lecture, title)

    def emit(directory: Path, lecture: tuple[str, ...], title: str):
        stem = _safe_name(title)
        prefix = f"Lecture: {'/'.join(lecture)}\nContent: {title}"
        yield directory / f"{stem}.py", f'# {title}\n\n"""\n{prefix}\n"""\n\n'
        yield directory / f"{stem}.md", f'# {title}\n\n"""\n{prefix}\n"""\n\n'
        yield directory / f"{stem}.cpp", f'// {title}\n\n/*\n\n{prefix}\n\n*/\n'

    yield from walk(course_structure, Path(), ())


def run_scaffold(root: Path, course_structure: dict[str, Any], apply: bool = False, index: bool = False) -> dict[str, int]:
    """Plan missing files or create them exclusively. Existing data is never replaced."""
    root = root.resolve()
    counts = {"missing": 0, "existing": 0, "created": 0}
    seen: set[Path] = set()
    index_lines = ["# CSAPP — generated course index\n", "<!-- Generated by main.py; never edit README.md here. -->\n"]
    for rel, template in iter_scaffold_files(course_structure):
        if rel in seen:
            raise ValueError(f"Duplicate scaffold path: {rel}")
        seen.add(rel)
        target = root / rel
        if not target.resolve().is_relative_to(root):
            raise ValueError(f"Scaffold path escapes target root: {target}")
        # A symlink (even a dangling one) must never be followed or replaced.
        if target.is_symlink() or target.exists():
            counts["existing"] += 1
        else:
            counts["missing"] += 1
            if apply:
                target.parent.mkdir(parents=True, exist_ok=True)
                try:
                    with target.open("x", encoding="utf-8") as stream:
                        stream.write(template)
                    counts["created"] += 1
                except FileExistsError:
                    counts["existing"] += 1
                    counts["missing"] -= 1
        if rel.suffix == ".md":
            index_lines.append(f"- [{rel.stem}]({rel.as_posix()})\n")

    if index:
        rel = Path("COURSE_INDEX.generated.md")
        target = root / rel
        if target.exists() or target.is_symlink():
            counts["existing"] += 1
        else:
            counts["missing"] += 1
            if apply:
                root.mkdir(parents=True, exist_ok=True)
                try:
                    with target.open("x", encoding="utf-8") as stream:
                        stream.write("\n".join(index_lines))
                    counts["created"] += 1
                except FileExistsError:
                    counts["existing"] += 1
                    counts["missing"] -= 1
    return counts


def main() -> None:
    parser = argparse.ArgumentParser(description="Safely preview or create missing CSAPP chapter templates")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent,
                        help="Target root (defaults to the repository directory)")
    parser.add_argument("--apply", action="store_true", help="Create missing files only; never overwrite")
    parser.add_argument("--index", action="store_true", help="Also create COURSE_INDEX.generated.md only if missing")
    args = parser.parse_args()
    result = run_scaffold(args.root, structure, apply=args.apply, index=args.index)
    print(f"{'Applied' if args.apply else 'Dry run'}: {result['missing']} missing, "
          f"{result['existing']} existing, {result['created']} created. README.md unchanged.")


if __name__ == "__main__":
    main()
