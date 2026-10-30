// 00_2.3.1_无符号加法

/*

Lecture: 02_程序结构和执行/2.3_整数运算
Content: 00_2.3.1_无符号加法

*/
#include <bitset>
#include <cstdint>
#include <iostream>
#include <limits>
#include <string>
#include <type_traits>

template <typename T>
void print_binary(const std::string& label, T value) {
    static_assert(std::is_integral_v<T> && std::is_unsigned_v<T>, "Unsigned integer required");
    std::cout << label << ": " << std::bitset<sizeof(T) * 8>(value)
              << " (" << static_cast<std::uint64_t>(value) << ")\n";
}

// Check overflow against the type's own maximum, not a promoted unsigned int.
// In particular, uint8_t(200) + uint8_t(100) exceeds uint8_t's range.
template <typename T>
bool detect_overflow(T x, T y) {
    static_assert(std::is_integral_v<T> && std::is_unsigned_v<T>, "Unsigned integer required");
    return x > static_cast<T>(std::numeric_limits<T>::max() - y);
}

void basic_unsigned_addition() {
    const std::uint32_t x = 3000000000U;
    const std::uint32_t y = 1500000000U;
    const std::uint32_t sum = x + y; // defined modulo 2^32
    print_binary("x", x);
    print_binary("y", y);
    print_binary("sum", sum);
    std::cout << "32位加法溢出检测: " << (detect_overflow(x, y) ? "是" : "否") << '\n';
}

void handle_different_bitwidth_addition() {
    const std::uint8_t a = 200;
    const std::uint8_t b = 100;
    const std::uint8_t sum = static_cast<std::uint8_t>(static_cast<unsigned>(a) + b);
    print_binary("a", a);
    print_binary("b", b);
    print_binary("sum", sum);
    std::cout << "8位加法溢出检测: " << (detect_overflow(a, b) ? "是" : "否") << '\n';
}

void modulo_addition() {
    const unsigned x = 15, y = 10;
    const unsigned sum = x + y;
    const unsigned mod_sum = sum % 16;
    print_binary("x", x);
    print_binary("y", y);
    print_binary("sum", sum);
    print_binary("mod_sum (模16)", mod_sum);
}

int main() {
    std::cout << "基本的无符号加法操作:\n";
    basic_unsigned_addition();
    std::cout << "\n处理不同位宽的无符号加法:\n";
    handle_different_bitwidth_addition();
    std::cout << "\n无符号数的模运算:\n";
    modulo_addition();
}
