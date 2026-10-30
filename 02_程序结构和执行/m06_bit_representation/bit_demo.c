#include <inttypes.h>
#include <limits.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

/* All shifting takes place in unsigned arithmetic, avoiding signed-overflow UB. */
static uint32_t rotate_left(uint32_t value, unsigned amount) {
    const unsigned n = amount % 32U;
    if (n == 0U) {
        return value;
    }
    return (value << n) | (value >> (32U - n));
}

static uint32_t bits_of_i32(int32_t value) {
    uint32_t bits = 0;
    /* Extract the object representation without signed/unsigned cast ambiguity. */
    memcpy(&bits, &value, sizeof(bits));
    return bits;
}

static int check(int yes, const char *label) {
    if (!yes) {
        fprintf(stderr, "FAILED: %s\n", label);
        return 1;
    }
    return 0;
}

int main(void) {
    if (CHAR_BIT != 8 || sizeof(uint32_t) != 4 || sizeof(int32_t) != 4) {
        puts("M06 bit representation: SKIP (requires 8-bit bytes and 32-bit integers)");
        return 0;
    }
    int failures = 0;
    failures += check(rotate_left(UINT32_C(0x12345678), 0) == UINT32_C(0x12345678), "rotate zero");
    failures += check(rotate_left(UINT32_C(0x12345678), 4) == UINT32_C(0x23456781), "rotate four");
    failures += check(rotate_left(UINT32_C(0x80000001), 1) == UINT32_C(0x00000003), "rotate boundary");
    failures += check(rotate_left(UINT32_C(0x12345678), 32) == UINT32_C(0x12345678), "rotate 32");
    failures += check(rotate_left(UINT32_C(0x12345678), 33) == rotate_left(UINT32_C(0x12345678), 1), "rotate 33");
    failures += check(bits_of_i32(INT32_C(-1)) == UINT32_MAX, "two's complement -1");
    failures += check(bits_of_i32(INT32_MIN) == UINT32_C(0x80000000), "two's complement min");
    const uint8_t sum8 = (uint8_t)((unsigned)UINT8_C(250) + (unsigned)UINT8_C(10));
    failures += check(sum8 == 4U, "unsigned 8-bit modulo 256");

    /* memcpy shows byte order without aliasing rules or pointer casts. */
    const uint32_t value = UINT32_C(0x01020304);
    uint8_t bytes[4] = {0, 0, 0, 0};
    memcpy(bytes, &value, sizeof(bytes));
    const int little = bytes[0] == 4 && bytes[1] == 3 && bytes[2] == 2 && bytes[3] == 1;
    const int big = bytes[0] == 1 && bytes[1] == 2 && bytes[2] == 3 && bytes[3] == 4;
    failures += check(little || big, "host byte order is known");

    if (failures != 0) return 1;
    printf("byte order: %s\n", little ? "little-endian" : "big-endian");
    printf("uint8 modulo: %" PRIu8 "\n", sum8);
    puts("M06 bit representation: PASS");
    return 0;
}
