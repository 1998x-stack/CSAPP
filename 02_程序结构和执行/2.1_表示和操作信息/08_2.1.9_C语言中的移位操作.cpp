// 08_2.1.9_C语言中的移位操作

/*

Lecture: 02_程序结构和执行/2.1_表示和操作信息
Content: 08_2.1.9_C语言中的移位操作

*/
#include <iostream>
#include <bitset>

// 显示二进制表示
void print_binary(const std::string& label, unsigned int value) {
    std::cout << label << ": " << std::bitset<32>(value) << std::endl;
}

// 布尔代数示例
void boolean_algebra_example() {
    unsigned int a = 0b1100; // 12
    unsigned int b = 0b1010; // 10

    unsigned int and_result = a & b;
    unsigned int or_result = a | b;
    unsigned int xor_result = a ^ b;
    unsigned int not_a = ~a;

    print_binary("a", a);
    print_binary("b", b);
    print_binary("a & b", and_result);
    print_binary("a | b", or_result);
    print_binary("a ^ b", xor_result);
    print_binary("~a", not_a);
}

// 位级操作示例
void bit_level_operations_example() {
    unsigned int x = 0b1001; // 9
    unsigned int mask = 0b0101; // 5

    unsigned int and_result = x & mask;
    unsigned int or_result = x | mask;
    unsigned int xor_result = x ^ mask;

    print_binary("x", x);
    print_binary("mask", mask);
    print_binary("x & mask", and_result);
    print_binary("x | mask", or_result);
    print_binary("x ^ mask", xor_result);
}

// 逻辑操作示例
void logical_operations_example() {
    bool a = true;
    bool b = false;

    bool and_result = a && b;
    bool or_result = a || b;
    bool not_a = !a;

    std::cout << "a && b: " << and_result << std::endl;
    std::cout << "a || b: " << or_result << std::endl;
    std::cout << "!a: " << not_a << std::endl;
}

// 移位操作示例
void shift_operations_example() {
    unsigned int x = 0b1001; // 9

    unsigned int left_shift = x << 2;
    unsigned int right_shift = x >> 2;

    print_binary("x", x);
    print_binary("x << 2", left_shift);
    print_binary("x >> 2", right_shift);
}

// 复杂示例：将多个操作结合起来
void complex_example() {
    unsigned int a = 0b11001100; // 204
    unsigned int b = 0b10101010; // 170

    // 先进行位级与操作，然后左移，再进行逻辑与操作
    unsigned int result = ((a & b) << 2) && 0b11110000;

    print_binary("a", a);
    print_binary("b", b);
    print_binary("((a & b) << 2) && 0b11110000", result);
}

int main() {
    std::cout << "布尔代数示例:" << std::endl;
    boolean_algebra_example();
    std::cout << std::endl;

    std::cout << "位级操作示例:" << std::endl;
    bit_level_operations_example();
    std::cout << std::endl;

    std::cout << "逻辑操作示例:" << std::endl;
    logical_operations_example();
    std::cout << std::endl;

    std::cout << "移位操作示例:" << std::endl;
    shift_operations_example();
    std::cout << std::endl;

    std::cout << "复杂示例:" << std::endl;
    complex_example();

    return 0;
}