// 02_2.2.3_二进制补码编码

/*

Lecture: 02_程序结构和执行/2.2_整数表示
Content: 02_2.2.3_二进制补码编码

*/
#include <bitset>
#include <cstdint>
#include <iostream>
#include <limits>
#include <string>
#include <type_traits>

template <typename T>
void print_binary(const std::string& label, T value) {
    static_assert(std::is_integral_v<T>, "Expected integer type");
    using Unsigned = std::make_unsigned_t<T>;
    std::cout << label << ": "
              << std::bitset<sizeof(T) * 8>(static_cast<Unsigned>(value))
              << " (" << static_cast<std::int64_t>(value) << ")\n";
}

// Evaluate in int64_t, then test the target int32_t range *before* narrowing.
bool checked_add(std::int32_t a, std::int32_t b, std::int32_t& out) {
    const std::int64_t exact = static_cast<std::int64_t>(a) + b;
    if (exact < std::numeric_limits<std::int32_t>::min() ||
        exact > std::numeric_limits<std::int32_t>::max()) return false;
    out = static_cast<std::int32_t>(exact);
    return true;
}

bool checked_sub(std::int32_t a, std::int32_t b, std::int32_t& out) {
    const std::int64_t exact = static_cast<std::int64_t>(a) - b;
    if (exact < std::numeric_limits<std::int32_t>::min() ||
        exact > std::numeric_limits<std::int32_t>::max()) return false;
    out = static_cast<std::int32_t>(exact);
    return true;
}

void basic_twos_complement_operations() {
    const std::int8_t a = -5, b = 3;
    // Promotion to int happens before the arithmetic; the results fit int8_t.
    const std::int8_t sum = static_cast<std::int8_t>(a + b);
    const std::int8_t difference = static_cast<std::int8_t>(a - b);
    print_binary("a", a);
    print_binary("b", b);
    print_binary("sum", sum);
    print_binary("difference", difference);
    std::cout << "基本加法/减法均未溢出\n";
}

void handle_different_bitwidth() {
    const std::int16_t small = -12345;
    const std::int32_t large = small; // sign extension
    print_binary("small_number (16位)", small);
    print_binary("large_number (32位)", large);
}

void overflow_handling() {
    const std::int32_t max_int = std::numeric_limits<std::int32_t>::max();
    const std::int32_t min_int = std::numeric_limits<std::int32_t>::min();
    std::int32_t result = 0;
    print_binary("max_int", max_int);
    print_binary("min_int", min_int);
    std::cout << "最大值加1发生溢出: " << (checked_add(max_int, 1, result) ? "否" : "是") << '\n';
    std::cout << "最小值减1发生溢出: " << (checked_sub(min_int, 1, result) ? "否" : "是") << '\n';

    // Unsigned arithmetic wraps by the language rules. This demonstrates the
    // raw 32-bit pattern, NOT a valid overflowing signed C++ operation.
    const std::uint32_t wrapped_plus = static_cast<std::uint32_t>(max_int) + std::uint32_t{1};
    const std::uint32_t wrapped_minus = static_cast<std::uint32_t>(min_int) - std::uint32_t{1};
    std::cout << "按 32 位无符号规则得到的位模式 (+1): " << std::bitset<32>(wrapped_plus) << '\n'
              << "按 32 位无符号规则得到的位模式 (-1): " << std::bitset<32>(wrapped_minus) << '\n';
}

int main() {
    std::cout << "基本的二进制补码操作:\n";
    basic_twos_complement_operations();
    std::cout << "\n处理不同位宽的二进制补码:\n";
    handle_different_bitwidth();
    std::cout << "\n溢出处理:\n";
    overflow_handling();
}
