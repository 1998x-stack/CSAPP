#include "arith.h"
/* Separate translation unit: symbols resolved by the linker. */
int64_t m08_sum_3(int64_t a, int64_t b, int64_t c) {
    return a + b + c; /* test vectors avoid signed overflow */
}
uint64_t m08_xor_mask(uint64_t x, uint64_t mask) {
    return x ^ mask;
}
