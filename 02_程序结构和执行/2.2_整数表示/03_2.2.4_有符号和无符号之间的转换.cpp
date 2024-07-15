// 03_2.2.4_有符号和无符号之间的转换

/*

Lecture: 02_程序结构和执行/2.2_整数表示
Content: 03_2.2.4_有符号和无符号之间的转换

*/
#include <iostream>
#include <limits>
#include <bitset>

// 打印二进制表示
template <typename T>
void print_binary(const std::string& label, T value) {
    std::cout << label << ": " << std::bitset<sizeof(T) * 8>(value) << " (" << static_cast<int64_t>(value) << ")" << std::endl;
}

// 显示转换示例
void explicit_conversion_examples() {
    std::cout << "显式转换示例:" << std::endl;
    
    short v = -12345;
    unsigned short uv = static_cast<unsigned short>(v);
    print_binary("有符号 short v", v);
    print_binary("转换为无符号 unsigned short uv", uv);
    
    unsigned int u = 4294967295u; // UMax
    int tu = static_cast<int>(u);
    print_binary("无符号 unsigned int u", u);
    print_binary("转换为有符号 int tu", tu);
}

// 隐式转换示例
void implicit_conversion_examples() {
    std::cout << "隐式转换示例:" << std::endl;
    
    unsigned int ux = 10;
    int tx = ux; // 隐式转换为有符号整数
    print_binary("无符号 unsigned int ux", ux);
    print_binary("隐式转换为有符号 int tx", tx);

    int x = -1;
    unsigned y = 1;
    int sum = x + y; // -1 被隐式转换为无符号整数
    print_binary("有符号 int x", x);
    print_binary("无符号 unsigned y", y);
    print_binary("x + y 的结果", sum);
}

// 算术操作中的转换示例
void arithmetic_conversion_examples() {
    std::cout << "算术操作中的转换示例:" << std::endl;
    
    int a = -1;
    unsigned b = 2;
    bool result = a < b; // -1 被隐式转换为无符号整数
    print_binary("有符号 int a", a);
    print_binary("无符号 unsigned b", b);
    std::cout << "a < b 的结果: " << result << std::endl;

    int c = -1;
    unsigned d = 0;
    result = c < d; // -1 被隐式转换为无符号整数
    print_binary("有符号 int c", c);
    print_binary("无符号 unsigned d", d);
    std::cout << "c < d 的结果: " << result << std::endl;
}

int main() {
    explicit_conversion_examples();
    std::cout << std::endl;

    implicit_conversion_examples();
    std::cout << std::endl;

    arithmetic_conversion_examples();
    std::cout << std::endl;

    return 0;
}
