#include <float.h>
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

/* IEEE-754 binary32 layout: 1 sign, 8 exponent, 23 fraction bits. */
struct binary32 {
    unsigned sign;
    unsigned exponent;
    uint32_t fraction;
};

static struct binary32 unpack(uint32_t bits) {
    struct binary32 value = {
        (unsigned)(bits >> 31),
        (unsigned)((bits >> 23) & UINT32_C(0xff)),
        bits & UINT32_C(0x7fffff),
    };
    return value;
}

static int equal_binary32(uint32_t bits, unsigned sign,
                          unsigned exponent, uint32_t fraction) {
    const struct binary32 actual = unpack(bits);
    return actual.sign == sign
        && actual.exponent == exponent
        && actual.fraction == fraction;
}

static uint32_t bits_of_float(float value) {
    uint32_t bits = 0;
    memcpy(&bits, &value, sizeof(bits));
    return bits;
}

int main(void) {
    if (sizeof(float) != 4 || sizeof(uint32_t) != 4 ||
        FLT_RADIX != 2 || FLT_MANT_DIG != 24 || FLT_MAX_EXP != 128) {
        puts("M06 IEEE754: SKIP (host is not IEEE-754 binary32)");
        return 0;
    }
    const float one = 1.0f;
    const float minus_zero = -0.0f;
    if (bits_of_float(one) != UINT32_C(0x3f800000) ||
        bits_of_float(minus_zero) != UINT32_C(0x80000000)) {
        fputs("binary32 float representation unexpectedly differs\n", stderr);
        return 1;
    }
    const int valid =
        equal_binary32(UINT32_C(0x3f800000), 0U, 127U, 0U) &&
        equal_binary32(UINT32_C(0x80000000), 1U, 0U, 0U) &&
        equal_binary32(UINT32_C(0x00000001), 0U, 0U, 1U) &&  /* smallest subnormal */
        equal_binary32(UINT32_C(0x7f800000), 0U, 255U, 0U) && /* +infinity */
        equal_binary32(UINT32_C(0x7fc00000), 0U, 255U, UINT32_C(0x400000)); /* quiet NaN */
    if (!valid) {
        fputs("IEEE-754 field decode failure\n", stderr);
        return 1;
    }
    printf("float(1.0) bits: 0x%08" PRIx32 "\n", bits_of_float(one));
    puts("M06 IEEE754: PASS");
    return 0;
}
