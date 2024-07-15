// 00_2.2.1_整数数据类型

/*

Lecture: 02_程序结构和执行/2.2_整数表示
Content: 00_2.2.1_整数数据类型

*/
#include <iostream>
#include <limits>
#include <cstdint>

// 打印整数的详细信息
template<typename T>
void print_integer_info(const std::string& type_name, T value) {
    std::cout << "类型: " << type_name << std::endl;
    std::cout << "值: " << value << std::endl;
    std::cout << "最小值: " << std::numeric_limits<T>::min() << std::endl;
    std::cout << "最大值: " << std::numeric_limits<T>::max() << std::endl;
    std::cout << std::endl;
}

// 处理整数溢出
void handle_overflow() {
    int32_t max_int32 = std::numeric_limits<int32_t>::max();
    int32_t min_int32 = std::numeric_limits<int32_t>::min();

    std::cout << "溢出示例:" << std::endl;
    std::cout << "最大 int32_t: " << max_int32 << std::endl;
    std::cout << "最大 int32_t + 1: " << max_int32 + 1 << std::endl; // 溢出
    std::cout << "最小 int32_t: " << min_int32 << std::endl;
    std::cout << "最小 int32_t - 1: " << min_int32 - 1 << std::endl; // 溢出
    std::cout << std::endl;
}

// 数值扩展示例
void numeric_extension() {
    int8_t small_int = -128;
    int32_t extended_int = small_int; // 符号扩展

    uint8_t small_uint = 255;
    uint32_t extended_uint = small_uint; // 零扩展

    std::cout << "数值扩展示例:" << std::endl;
    std::cout << "int8_t (符号扩展): " << static_cast<int32_t>(small_int) << " -> " << extended_int << std::endl;
    std::cout << "uint8_t (零扩展): " << static_cast<uint32_t>(small_uint) << " -> " << extended_uint << std::endl;
    std::cout << std::endl;
}

int main() {
    // 打印不同整数类型的信息
    print_integer_info("signed char", static_cast<signed char>(-128));
    print_integer_info("unsigned char", static_cast<unsigned char>(255));
    print_integer_info("short", static_cast<short>(-32768));
    print_integer_info("unsigned short", static_cast<unsigned short>(65535));
    print_integer_info("int", static_cast<int>(-2147483648));
    print_integer_info("unsigned int", static_cast<unsigned int>(4294967295));
    print_integer_info("long", static_cast<long>(-2147483648));
    print_integer_info("unsigned long", static_cast<unsigned long>(4294967295));
    print_integer_info("int32_t", static_cast<int32_t>(-2147483648));
    print_integer_info("uint32_t", static_cast<uint32_t>(4294967295));
    print_integer_info("int64_t", static_cast<int64_t>(-9223372036854775807 - 1));
    print_integer_info("uint64_t", static_cast<uint64_t>(18446744073709551615U));

    // 演示整数溢出
    handle_overflow();

    // 演示数值扩展
    numeric_extension();

    return 0;
}
