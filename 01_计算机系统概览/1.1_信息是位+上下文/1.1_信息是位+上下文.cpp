// 1.1_信息是位+上下文

/*

Lecture: 01_计算机系统概览/1.1_信息是位+上下文
Content: 1.1_信息是位+上下文

*/
#include <iostream>
#include <bitset>
#include <string>

using namespace std;

// 将字符转换为二进制表示
void charToBinary(char c) {
    bitset<8> bits(c);
    cout << "字符 '" << c << "' 的二进制表示为: " << bits << endl;
}

// 将整数转换为二进制表示
void intToBinary(int n) {
    bitset<32> bits(n);
    cout << "整数 " << n << " 的二进制表示为: " << bits << endl;
}

// 将二进制表示解释为字符
void binaryToChar(string bits) {
    bitset<8> bitset(bits);
    char c = static_cast<char>(bitset.to_ulong());
    cout << "二进制字符串 " << bits << " 被解释为字符: '" << c << "'" << endl;
}

// 将二进制表示解释为整数
void binaryToInt(string bits) {
    bitset<32> bitset(bits);
    int n = static_cast<int>(bitset.to_ulong());
    cout << "二进制字符串 " << bits << " 被解释为整数: " << n << endl;
}

int main() {
    char c = 'a';
    int n = 97;
    
    // 显示字符和整数的二进制表示
    charToBinary(c);
    intToBinary(n);
    
    // 使用二进制字符串
    string charBits = "01100001";
    string intBits = "00000000000000000000000001100001";
    
    // 将二进制字符串解释为字符和整数
    binaryToChar(charBits);
    binaryToInt(intBits);

    return 0;
}