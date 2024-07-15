// 02_2.2.3_二进制补码编码

/*

Lecture: 02_程序结构和执行/2.2_整数表示
Content: 02_2.2.3_二进制补码编码

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
bool detect_overflow(int32_t a, int32_t b, int32_t result) {
    // 如果a和b同号，而result与a不同号，则发生溢出
    if ((a > 0 && b > 0 && result < 0) || (a < 0 && b < 0 && result > 0)) {
        return true;
    }
    return false;
}

// 检测二进制补码减法溢出
bool detect_underflow(int32_t a, int32_t b, int32_t result) {
    // 如果a和b异号，而result与a同号，则发生溢出
    if ((a > 0 && b < 0 && result < 0) || (a < 0 && b > 0 && result > 0)) {
        return true;
    }
    return false;
}

// 示例1：基本的二进制补码操作
void basic_twos_complement_operations() {
    int8_t a = -5;  // 8位二进制补码
    int8_t b = 3;

    int8_t sum = a + b;
    int8_t difference = a - b;

    print_binary("a", a);
    print_binary("b", b);
    print_binary("sum", sum);
    print_binary("difference", difference);

    if (detect_overflow(a, b, sum)) {
        std::cout << "加法溢出检测: 是" << std::endl;
    } else {
        std::cout << "加法溢出检测: 否" << std::endl;
    }

    if (detect_underflow(a, b, difference)) {
        std::cout << "减法溢出检测: 是" << std::endl;
    } else {
        std::cout << "减法溢出检测: 否" << std::endl;
    }
}

// 示例2：处理不同位宽的二进制补码
void handle_different_bitwidth() {
    int16_t small_number = -12345;  // 16位二进制补码
    int32_t large_number = small_number;  // 符号扩展

    print_binary("small_number (16位)", small_number);
    print_binary("large_number (32位)", large_number);
}

// 示例3：溢出处理
void overflow_handling() {
    int32_t max_int = std::numeric_limits<int32_t>::max();
    int32_t min_int = std::numeric_limits<int32_t>::min();

    int32_t overflow_sum = max_int + 1;
    int32_t underflow_difference = min_int - 1;

    print_binary("max_int", max_int);
    print_binary("min_int", min_int);
    print_binary("overflow_sum", overflow_sum);
    print_binary("underflow_difference", underflow_difference);

    if (detect_overflow(max_int, 1, overflow_sum)) {
        std::cout << "最大值加1发生溢出" << std::endl;
    } else {
        std::cout << "最大值加1未发生溢出" << std::endl;
    }

    if (detect_underflow(min_int, -1, underflow_difference)) {
        std::cout << "最小值减1发生溢出" << std::endl;
    } else {
        std::cout << "最小值减1未发生溢出" << std::endl;
    }
}

int main() {
    std::cout << "基本的二进制补码操作:" << std::endl;
    basic_twos_complement_operations();
    std::cout << std::endl;

    std::cout << "处理不同位宽的二进制补码:" << std::endl;
    handle_different_bitwidth();
    std::cout << std::endl;

    std::cout << "溢出处理:" << std::endl;
    overflow_handling();
    std::cout << std::endl;

    return 0;
}
