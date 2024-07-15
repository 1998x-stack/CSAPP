// 3.3_数据格式

/*

Lecture: 03_程序的机器级表示/3.3_数据格式
Content: 3.3_数据格式

*/
#include <iostream>
#include <cstdint>

using namespace std;

int main() {
    // Primitive data types
    cout << "Primitive Data Types:" << endl;
    cout << "=====================" << endl;
    
    cout << "Size of char: " << sizeof(char) << " byte(s)" << endl;
    cout << "Size of short: " << sizeof(short) << " byte(s)" << endl;
    cout << "Size of int: " << sizeof(int) << " byte(s)" << endl;
    cout << "Size of long: " << sizeof(long) << " byte(s)" << endl;
    cout << "Size of float: " << sizeof(float) << " byte(s)" << endl;
    cout << "Size of double: " << sizeof(double) << " byte(s)" << endl;
    cout << "Size of pointer: " << sizeof(void*) << " byte(s)" << endl;
    
    // Fixed-size integer types
    cout << "\nFixed-size Integer Types:" << endl;
    cout << "========================" << endl;
    
    cout << "Size of int8_t: " << sizeof(int8_t) << " byte(s)" << endl;
    cout << "Size of int16_t: " << sizeof(int16_t) << " byte(s)" << endl;
    cout << "Size of int32_t: " << sizeof(int32_t) << " byte(s)" << endl;
    cout << "Size of int64_t: " << sizeof(int64_t) << " byte(s)" << endl;
    
    // Data alignment
    struct DataStruct {
        char c;
        short s;
        int i;
        double d;
    };
    
    cout << "\nData Alignment:" << endl;
    cout << "===============" << endl;
    cout << "Size of DataStruct: " << sizeof(DataStruct) << " byte(s)" << endl;
    cout << "Offset of char c: " << offsetof(DataStruct, c) << " byte(s)" << endl;
    cout << "Offset of short s: " << offsetof(DataStruct, s) << " byte(s)" << endl;
    cout << "Offset of int i: " << offsetof(DataStruct, i) << " byte(s)" << endl;
    cout << "Offset of double d: " << offsetof(DataStruct, d) << " byte(s)" << endl;
    
    // Endianness check
    uint32_t num = 0x12345678;
    uint8_t* ptr = reinterpret_cast<uint8_t*>(&num);
    
    cout << "\nEndianness:" << endl;
    cout << "===========" << endl;
    
    cout << "Memory representation of 0x12345678: ";
    for (int i = sizeof(num) - 1; i >= 0; --i) {
        cout << hex << static_cast<int>(ptr[i]) << " ";
    }
    cout << endl;
    
    return 0;
}