// 02_2.3.3_二进制补码求反

/*

Lecture: 02_程序结构和执行/2.3_整数运算
Content: 02_2.3.3_二进制补码求反

*/
#include <bitset>
#include <cstdint>
#include <iostream>
#include <limits>
#include <string>
#include <type_traits>

template <typename T>
void print_binary(const std::string& label, T value) {
    static_assert(std::is_integral_v<T>, "Integer required");
    using U = std::make_unsigned_t<T>;
    std::cout << label << ": " << std::bitset<sizeof(T) * 8>(static_cast<U>(value))
              << " (" << static_cast<std::int64_t>(value) << ")\n";
}

template <typename T>
bool negation_overflows(T value) {
    static_assert(std::is_signed_v<T>, "Signed integer required");
    return value == std::numeric_limits<T>::min();
}

void basic_twos_complement_negation() {
    const int x = -5;
    const int neg_x = -x; // in-range, defined
    print_binary("x", x);
    print_binary("neg_x", neg_x);
    std::cout << "求反溢出检测: " << (negation_overflows(x) ? "是" : "否") << '\n';
}

void handle_different_bitwidth_negation() {
    const std::int8_t a = -50;
    const std::int8_t neg_a = static_cast<std::int8_t>(-static_cast<int>(a));
    print_binary("a", a);
    print_binary("neg_a", neg_a);
    std::cout << "8位求反溢出检测: " << (negation_overflows(a) ? "是" : "否") << '\n';
}

void negation_of_min_int() {
    const std::int32_t x = std::numeric_limits<std::int32_t>::min();
    // A signed 32-bit negation would overflow: never evaluate -x or ~x + 1
    // as int32_t here. Use int64_t for the mathematical result.
    const std::int64_t exact = -static_cast<std::int64_t>(x);
    print_binary("x (min int32_t)", x);
    std::cout << "数学求反结果 (int64_t): " << exact << '\n'
              << "最小负数求反溢出检测: " << (negation_overflows(x) ? "是" : "否") << '\n';
    const std::uint32_t wrapped_bits = std::uint32_t{0} - static_cast<std::uint32_t>(x);
    std::cout << "32位无符号模运算位模式: " << std::bitset<32>(wrapped_bits) << '\n';
}

int main() {
    std::cout << "基本的二进制补码求反操作:\n";
    basic_twos_complement_negation();
    std::cout << "\n处理不同位宽的二进制补码求反:\n";
    handle_different_bitwidth_negation();
    std::cout << "\n二进制补码数的最小负数求反:\n";
    negation_of_min_int();
}
