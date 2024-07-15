// 00_2.3.1_无符号加法

/*

Lecture: 02_程序结构和执行/2.3_整数运算
Content: 00_2.3.1_无符号加法

*/
#include <iostream>
#include <limits>
#include <bitset>

// 打印二进制表示
template <typename T>
void print_binary(const std::string& label, T value) {
    std::cout << label << ": " << std::bitset<sizeof(T) * 8>(value) << " (" << static_cast<uint64_t>(value) << ")" << std::endl;
}

// 检测无符号加法溢出
bool detect_overflow(unsigned int x, unsigned int y) {
    unsigned int sum = x + y;
    return sum < x || sum < y;
}

// 示例1：基本的无符号加法操作
void basic_unsigned_addition() {
    unsigned int x = 3000000000;
    unsigned int y = 1500000000;

    unsigned int sum = x + y;
    print_binary("x", x);
    print_binary("y", y);
    print_binary("sum", sum);

    if (detect_overflow(x, y)) {
        std::cout << "加法溢出检测: 是" << std::endl;
    } else {
        std::cout << "加法溢出检测: 否" << std::endl;
    }
}

// 示例2：处理不同位宽的无符号加法
void handle_different_bitwidth_addition() {
    unsigned char a = 200; // 8位无符号整数
    unsigned char b = 100; // 8位无符号整数

    unsigned char sum = a + b;
    print_binary("a", a);
    print_binary("b", b);
    print_binary("sum", sum);

    if (detect_overflow(a, b)) {
        std::cout << "8位加法溢出检测: 是" << std::endl;
    } else {
        std::cout << "8位加法溢出检测: 否" << std::endl;
    }
}

// 示例3：无符号数的模运算
void modulo_addition() {
    unsigned int x = 15;
    unsigned int y = 10;

    unsigned int sum = x + y;
    unsigned int mod_sum = sum % 16; // 模16的结果
    print_binary("x", x);
    print_binary("y", y);
    print_binary("sum", sum);
    print_binary("mod_sum (模16)", mod_sum);
}

int main() {
    std::cout << "基本的无符号加法操作:" << std::endl;
    basic_unsigned_addition();
    std::cout << std::endl;

    std::cout << "处理不同位宽的无符号加法:" << std::endl;
    handle_different_bitwidth_addition();
    std::cout << std::endl;

    std::cout << "无符号数的模运算:" << std::endl;
    modulo_addition();
    std::cout << std::endl;

    return 0;
}
