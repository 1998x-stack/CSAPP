// 02_2.1.3_地址和字节顺序

/*

Lecture: 02_程序结构和执行/2.1_表示和操作信息
Content: 02_2.1.3_地址和字节顺序

*/
#include <iostream>
#include <cstdint>

/**
 * @brief Check system endianness
 * 
 * @return true if system is little-endian, false if system is big-endian
 */
bool isLittleEndian() {
    uint16_t number = 0x1;
    uint8_t *numPtr = reinterpret_cast<uint8_t*>(&number);
    return (numPtr[0] == 1);
}

/**
 * @brief Convert 32-bit integer from little-endian to big-endian
 * 
 * @param value The 32-bit integer to convert
 * @return uint32_t The converted 32-bit integer in big-endian format
 */
uint32_t littleToBigEndian(uint32_t value) {
    return ((value & 0x000000FF) << 24) | 
           ((value & 0x0000FF00) << 8)  | 
           ((value & 0x00FF0000) >> 8)  | 
           ((value & 0xFF000000) >> 24);
}

/**
 * @brief Convert 32-bit integer from big-endian to little-endian
 * 
 * @param value The 32-bit integer to convert
 * @return uint32_t The converted 32-bit integer in little-endian format
 */
uint32_t bigToLittleEndian(uint32_t value) {
    return ((value & 0x000000FF) << 24) | 
           ((value & 0x0000FF00) << 8)  | 
           ((value & 0x00FF0000) >> 8)  | 
           ((value & 0xFF000000) >> 24);
}

int main() {
    // Check system endianness
    if (isLittleEndian()) {
        std::cout << "System is Little-Endian" << std::endl;
    } else {
        std::cout << "System is Big-Endian" << std::endl;
    }

    // Example: Little-endian to Big-endian
    uint32_t littleEndianValue = 0x01234567;
    uint32_t bigEndianValue = littleToBigEndian(littleEndianValue);
    std::cout << "Little-Endian Value: 0x" << std::hex << littleEndianValue << std::endl;
    std::cout << "Converted to Big-Endian: 0x" << std::hex << bigEndianValue << std::endl;

    // Example: Big-endian to Little-endian
    bigEndianValue = 0x89ABCDEF;
    littleEndianValue = bigToLittleEndian(bigEndianValue);
    std::cout << "Big-Endian Value: 0x" << std::hex << bigEndianValue << std::endl;
    std::cout << "Converted to Little-Endian: 0x" << std::hex << littleEndianValue << std::endl;

    return 0;
}
