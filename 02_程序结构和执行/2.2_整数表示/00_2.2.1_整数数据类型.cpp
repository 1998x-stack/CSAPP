// 00_2.2.1_整数数据类型

/*

Lecture: 02_程序结构和执行/2.2_整数表示
Content: 00_2.2.1_整数数据类型

*/
#include <cstdint>
#include <iostream>
#include <limits>
#include <string>
#include <type_traits>

// Use an integer output type so char / unsigned char do not print as characters.
template <typename T>
void print_integer_info(const std::string& type_name, T value) {
    static_assert(std::is_integral_v<T>, "Expected an integer type");
    using Display = std::conditional_t<std::is_signed_v<T>, std::int64_t, std::uint64_t>;
    std::cout << "类型: " << type_name << '\n'
              << "值: " << static_cast<Display>(value) << '\n'
              << "最小值: " << static_cast<Display>(std::numeric_limits<T>::min()) << '\n'
              << "最大值: " << static_cast<Display>(std::numeric_limits<T>::max()) << "\n\n";
}

// C++ signed overflow is undefined behavior: calculate the mathematical result
// in a wider type instead of evaluating int32_t(max)+1 or int32_t(min)-1.
void handle_overflow() {
    const std::int32_t max_value = std::numeric_limits<std::int32_t>::max();
    const std::int32_t min_value = std::numeric_limits<std::int32_t>::min();
    const std::int64_t beyond_max = static_cast<std::int64_t>(max_value) + 1;
    const std::int64_t below_min = static_cast<std::int64_t>(min_value) - 1;
    std::cout << "溢出示例（在 int64_t 中安全计算）:\n"
              << "int32_t 最大值: " << max_value << '\n'
              << "int32_t 最大值 + 1 超出 int32_t 范围: " << beyond_max << '\n'
              << "int32_t 最小值: " << min_value << '\n'
              << "int32_t 最小值 - 1 超出 int32_t 范围: " << below_min << "\n\n";
}

void numeric_extension() {
    const std::int8_t small_int = -128;
    const std::int32_t extended_int = small_int; // sign extension
    const std::uint8_t small_uint = 255;
    const std::uint32_t extended_uint = small_uint; // zero extension
    std::cout << "数值扩展示例:\n"
              << "int8_t (符号扩展): " << static_cast<int>(small_int) << " -> " << extended_int << '\n'
              << "uint8_t (零扩展): " << static_cast<unsigned>(small_uint) << " -> " << extended_uint
              << "\n\n";
}

int main() {
    print_integer_info("signed char", static_cast<signed char>(-1));
    print_integer_info("unsigned char", std::numeric_limits<unsigned char>::max());
    print_integer_info("short", std::numeric_limits<short>::min());
    print_integer_info("unsigned short", std::numeric_limits<unsigned short>::max());
    print_integer_info("int", std::numeric_limits<int>::min());
    print_integer_info("unsigned int", std::numeric_limits<unsigned int>::max());
    print_integer_info("long", std::numeric_limits<long>::min());
    print_integer_info("unsigned long", std::numeric_limits<unsigned long>::max());
    print_integer_info("int32_t", std::numeric_limits<std::int32_t>::min());
    print_integer_info("uint32_t", std::numeric_limits<std::uint32_t>::max());
    print_integer_info("int64_t", std::numeric_limits<std::int64_t>::min());
    print_integer_info("uint64_t", std::numeric_limits<std::uint64_t>::max());
    handle_overflow();
    numeric_extension();
}
