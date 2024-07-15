// 01_2.3.2_二进制补码加法

/*

Lecture: 02_程序结构和执行/2.3_整数运算
Content: 01_2.3.2_二进制补码加法

*/
#include <iostream>
#include <limits>
#include <bitset>

// 打印二进制表示
template <typename T>
void print_binary(const std::string& label, T value) {
    std::cout << label << ": " << std::bitset<sizeof(T) * 8>(value) << " (" << static_cast<int64_t>(value) << ")" << std::endl;
}

// 检测二进制补码加法溢出
bool detect_overflow(int x, int y, int result) {
    if ((x > 0 && y > 0 && result < 0) || (x < 0 && y < 0 && result > 0)) {
        return true;
    }
    return false;
}

// 示例1：基本的二进制补码加法操作
void basic_twos_complement_addition() {
    int x = 1000000000;
    int y = 1500000000;

    int sum = x + y;
    print_binary("x", x);
    print_binary("y", y);
    print_binary("sum", sum);

    if (detect_overflow(x, y, sum)) {
        std::cout << "加法溢出检测: 是" << std::endl;
    } else {
        std::cout << "加法溢出检测: 否" << std::endl;
    }
}

// 示例2：处理不同位宽的二进制补码加法
void handle_different_bitwidth_addition() {
    int8_t a = 100; // 8位二进制补码整数
    int8_t b = 50;  // 8位二进制补码整数

    int8_t sum = a + b;
    print_binary("a", a);
    print_binary("b", b);
    print_binary("sum", sum);

    if (detect_overflow(a, b, sum)) {
        std::cout << "8位加法溢出检测: 是" << std::endl;
    } else {
        std::cout << "8位加法溢出检测: 否" << std::endl;
    }
}

// 示例3：二进制补码数的模运算
void modulo_addition() {
    int x = -7;
    int y = 5;

    int sum = x + y;
    int mod_sum = sum % 16; // 模16的结果
    print_binary("x", x);
    print_binary("y", y);
    print_binary("sum", sum);
    print_binary("mod_sum (模16)", mod_sum);
}

int main() {
    std::cout << "基本的二进制补码加法操作:" << std::endl;
    basic_twos_complement_addition();
    std::cout << std::endl;

    std::cout << "处理不同位宽的二进制补码加法:" << std::endl;
    handle_different_bitwidth_addition();
    std::cout << std::endl;

    std::cout << "二进制补码数的模运算:" << std::endl;
    modulo_addition();
    std::cout << std::endl;

    return 0;
}
