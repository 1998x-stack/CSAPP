// 01_2.3.2_二进制补码加法

/*

Lecture: 02_程序结构和执行/2.3_整数运算
Content: 01_2.3.2_二进制补码加法

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
bool is_out_of_range(std::int64_t exact) {
    static_assert(std::is_signed_v<T> && sizeof(T) <= sizeof(std::int32_t),
                  "Check only signed types up to 32 bits");
    return exact < std::numeric_limits<T>::min() || exact > std::numeric_limits<T>::max();
}

void basic_twos_complement_addition() {
    const std::int32_t x = 1000000000;
    const std::int32_t y = 1500000000;
    const std::int64_t exact = static_cast<std::int64_t>(x) + y; // no signed overflow
    print_binary("x", x);
    print_binary("y", y);
    std::cout << "数学加法结果 (int64_t): " << exact << '\n';
    std::cout << "32位加法溢出检测: " << (is_out_of_range<std::int32_t>(exact) ? "是" : "否") << '\n';

    // A bit pattern can be obtained using defined unsigned modulo arithmetic.
    const std::uint32_t bits = static_cast<std::uint32_t>(x) + static_cast<std::uint32_t>(y);
    std::cout << "32位模加法的位模式: " << std::bitset<32>(bits) << '\n';
}

void handle_different_bitwidth_addition() {
    const std::int8_t a = 100, b = 50;
    const std::int64_t exact = static_cast<int>(a) + static_cast<int>(b);
    print_binary("a", a);
    print_binary("b", b);
    std::cout << "8位数学加法结果: " << exact << '\n'
              << "8位加法溢出检测: " << (is_out_of_range<std::int8_t>(exact) ? "是" : "否") << '\n';
    const std::uint8_t bits = static_cast<std::uint8_t>(exact);
    const int signed_interpretation = bits < 128 ? bits : static_cast<int>(bits) - 256;
    std::cout << "8位补码位模式: " << std::bitset<8>(bits)
              << "，按补码解释: " << signed_interpretation << '\n';
}

void modulo_addition() {
    const int x = -7, y = 5;
    const int sum = x + y;
    const int remainder = sum % 16; // C++ remainder keeps the dividend's sign
    const int nonnegative_mod = (remainder + 16) % 16;
    print_binary("x", x);
    print_binary("y", y);
    print_binary("sum", sum);
    std::cout << "C++ 余数 (-2 % 16): " << remainder << '\n'
              << "非负模16: " << nonnegative_mod << '\n';
}

int main() {
    std::cout << "基本的二进制补码加法操作:\n";
    basic_twos_complement_addition();
    std::cout << "\n处理不同位宽的二进制补码加法:\n";
    handle_different_bitwidth_addition();
    std::cout << "\n二进制补码数的模运算:\n";
    modulo_addition();
}
