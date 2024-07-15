// 02_2.3.3_二进制补码求反

/*

Lecture: 02_程序结构和执行/2.3_整数运算
Content: 02_2.3.3_二进制补码求反

*/
#include <iostream>
#include <limits>
#include <bitset>

// 打印二进制表示
template <typename T>
void print_binary(const std::string& label, T value) {
    std::cout << label << ": " << std::bitset<sizeof(T) * 8>(value) << " (" << static_cast<int64_t>(value) << ")" << std::endl;
}

// 检测二进制补码求反溢出
bool detect_overflow(int x, int result) {
    // 在二进制补码中，只有最小负数（-2^(w-1)）在求反时会溢出
    return x == std::numeric_limits<T>::min();
}

// 示例1：基本的二进制补码求反操作
void basic_twos_complement_negation() {
    int x = -5;
    int neg_x = ~x + 1;

    print_binary("x", x);
    print_binary("neg_x", neg_x);

    if (detect_overflow(x, neg_x)) {
        std::cout << "求反溢出检测: 是" << std::endl;
    } else {
        std::cout << "求反溢出检测: 否" << std::endl;
    }
}

// 示例2：处理不同位宽的二进制补码求反
void handle_different_bitwidth_negation() {
    int8_t a = -50; // 8位二进制补码整数
    int8_t neg_a = ~a + 1;

    print_binary("a", a);
    print_binary("neg_a", neg_a);

    if (detect_overflow(a, neg_a)) {
        std::cout << "8位求反溢出检测: 是" << std::endl;
    } else {
        std::cout << "8位求反溢出检测: 否" << std::endl;
    }
}

// 示例3：二进制补码数的最小负数求反
void negation_of_min_int() {
    int x = std::numeric_limits<int>::min();
    int neg_x = ~x + 1;

    print_binary("x (min int)", x);
    print_binary("neg_x", neg_x);

    if (detect_overflow(x, neg_x)) {
        std::cout << "最小负数求反溢出检测: 是" << std::endl;
    } else {
        std::cout << "最小负数求反溢出检测: 否" << std::endl;
    }
}

int main() {
    std::cout << "基本的二进制补码求反操作:" << std::endl;
    basic_twos_complement_negation();
    std::cout << std::endl;

    std::cout << "处理不同位宽的二进制补码求反:" << std::endl;
    handle_different_bitwidth_negation();
    std::cout << std::endl;

    std::cout << "二进制补码数的最小负数求反:" << std::endl;
    negation_of_min_int();
    std::cout << std::endl;

    return 0;
}
