#include <stdint.h>
#include <stdio.h>

int main(void) {
    const uint8_t a = UINT8_C(250);
    const uint8_t b = UINT8_C(10);
    const uint8_t wrapped = (uint8_t)((unsigned)a + (unsigned)b);
    if (wrapped != 4) {
        return 1;
    }
    puts("M03 C smoke: ok");
    return 0;
}
