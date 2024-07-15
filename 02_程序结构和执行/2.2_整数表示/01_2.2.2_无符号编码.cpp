// 01_2.2.2_无符号编码

/*

Lecture: 02_程序结构和执行/2.2_整数表示
Content: 01_2.2.2_无符号编码

*/
#include <iostream>
#include <limits>
#include <bitset>

// 打印二进制表示
void print_binary(const std::string& label, unsigned int value) {
    std::cout << label << ": " << std::bitset<32>(value) << std::endl;
}

int main() {
    unsigned int a = 5;  // 0101
    unsigned int b = 12; // 1100

    // 基本的无符号整数操作
    unsigned int sum = a + b;
    unsigned int difference = a - b;
    unsigned int product = a * b;
    unsigned int quotient = b / a;
    unsigned int remainder = b % a;

    // 打印结果
    print_binary("a", a);
    print_binary("b", b);
    print_binary("sum", sum);
    print_binary("difference", difference);
    print_binary("product", product);
    print_binary("quotient", quotient);
    print_binary("remainder", remainder);

    // 最大和最小值
    std::cout << "最大 unsigned int: " << std::numeric_limits<unsigned int>::max() << std::endl;
    std::cout << "最小 unsigned int: " << std::numeric_limits<unsigned int>::min() << std::endl;

    return 0;
}
