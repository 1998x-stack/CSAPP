// 03_2.2.4_有符号和无符号之间的转换

/*

Lecture: 02_程序结构和执行/2.2_整数表示
Content: 03_2.2.4_有符号和无符号之间的转换

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

void explicit_conversion_examples() {
    std::cout << "显式转换示例:\n";
    const std::int16_t v = -12345;
    const std::uint16_t uv = static_cast<std::uint16_t>(v); // defined modulo 2^16
    print_binary("有符号 int16_t v", v);
    print_binary("转换为无符号 uint16_t uv", uv);

    // Conversion from an out-of-range uint32_t to int32_t is
    // implementation-defined in C++17. Do not silently assume a result.
    const std::uint32_t u = std::numeric_limits<std::uint32_t>::max();
    const std::int64_t twos_complement = static_cast<std::int64_t>(u) - (std::int64_t{1} << 32);
    print_binary("32位无符号最大值", u);
    std::cout << "按32位补码解释的数学值: " << twos_complement << '\n';
}

void implicit_conversion_examples() {
    std::cout << "隐式转换示例:\n";
    const std::uint32_t ux = 10;
    const std::int32_t tx = static_cast<std::int32_t>(ux); // in range
    print_binary("无符号 uint32_t ux", ux);
    print_binary("转换为有符号 int32_t tx", tx);

    const std::int32_t x = -1;
    const std::uint32_t y = 1;
    const std::uint32_t sum = x + y; // arithmetic is unsigned modulo 2^32
    print_binary("有符号 int32_t x", x);
    print_binary("无符号 uint32_t y", y);
    print_binary("x + y 的无符号结果", sum);
}

void arithmetic_conversion_examples() {
    std::cout << "算术操作中的转换示例:\n";
    const std::int32_t a = -1;
    const std::uint32_t b = 2;
    print_binary("有符号 int32_t a", a);
    print_binary("无符号 uint32_t b", b);
    std::cout << "a < b 的结果: " << (static_cast<std::uint32_t>(a) < b) << '\n'; // implicit conversion made explicit
    const std::int32_t c = -1;
    const std::uint32_t d = 0;
    std::cout << "c < d 的结果: " << (static_cast<std::uint32_t>(c) < d) << '\n'; // equivalent to the mixed-type comparison
}

int main() {
    explicit_conversion_examples();
    std::cout << '\n';
    implicit_conversion_examples();
    std::cout << '\n';
    arithmetic_conversion_examples();
}
