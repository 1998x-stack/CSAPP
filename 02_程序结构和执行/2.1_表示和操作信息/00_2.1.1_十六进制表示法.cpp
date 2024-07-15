// 00_2.1.1_十六进制表示法

/*

Lecture: 02_程序结构和执行/2.1_表示和操作信息
Content: 00_2.1.1_十六进制表示法

*/
#include <iostream>
#include <string>
#include <sstream>
#include <iomanip>
#include <bitset>

/**
 * @brief Convert decimal to hexadecimal
 * 
 * @param decimal The decimal number to convert
 * @return std::string The hexadecimal representation
 */
std::string decimalToHex(int decimal) {
    std::stringstream ss;
    ss << std::hex << std::uppercase << decimal;
    return ss.str();
}

/**
 * @brief Convert hexadecimal to decimal
 * 
 * @param hex The hexadecimal string to convert
 * @return int The decimal representation
 */
int hexToDecimal(const std::string& hex) {
    int decimal;
    std::stringstream ss;
    ss << std::hex << hex;
    ss >> decimal;
    return decimal;
}

/**
 * @brief Convert binary to hexadecimal
 * 
 * @param binary The binary string to convert
 * @return std::string The hexadecimal representation
 */
std::string binaryToHex(const std::string& binary) {
    std::bitset<32> bitset(binary);
    std::stringstream ss;
    ss << std::hex << std::uppercase << bitset.to_ulong();
    return ss.str();
}

/**
 * @brief Convert hexadecimal to binary
 * 
 * @param hex The hexadecimal string to convert
 * @return std::string The binary representation
 */
std::string hexToBinary(const std::string& hex) {
    int decimal = hexToDecimal(hex);
    std::bitset<32> bitset(decimal);
    return bitset.to_string();
}

int main() {
    // 示例：十进制转十六进制
    int decimalNumber = 314156;
    std::string hexString = decimalToHex(decimalNumber);
    std::cout << "Decimal " << decimalNumber << " to Hexadecimal: " << hexString << std::endl;

    // 示例：十六进制转十进制
    std::string hexNumber = "4CB2C";
    int decimalResult = hexToDecimal(hexNumber);
    std::cout << "Hexadecimal " << hexNumber << " to Decimal: " << decimalResult << std::endl;

    // 示例：二进制转十六进制
    std::string binaryNumber = "1111001010110110110011";
    std::string hexResult = binaryToHex(binaryNumber);
    std::cout << "Binary " << binaryNumber << " to Hexadecimal: " << hexResult << std::endl;

    // 示例：十六进制转二进制
    std::string hexToBinaryResult = hexToBinary("F2B6C3");
    std::cout << "Hexadecimal F2B6C3 to Binary: " << hexToBinaryResult << std::endl;

    return 0;
}
