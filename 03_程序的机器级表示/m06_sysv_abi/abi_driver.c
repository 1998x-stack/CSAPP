#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>

/* Under the System V AMD64 ABI:
 * 1st/2nd/3rd integer args: rdi/rsi/rdx; return value: rax.
 */
extern int64_t csapp_m06_sum3(int64_t a, int64_t b, int64_t c);
extern int64_t csapp_m06_max2(int64_t a, int64_t b);

struct case_sum {
    int64_t a, b, c, expected;
};

static int check_sum(void) {
    const struct case_sum tests[] = {
        {1, 2, 3, 6},
        {-1, 0, 1, 0},
        {INT64_C(2147483647), 1, 0, INT64_C(2147483648)},
        {-100, 30, 10, -60},
    };
    for (size_t i = 0; i < sizeof(tests) / sizeof(tests[0]); ++i) {
        int64_t got = csapp_m06_sum3(tests[i].a, tests[i].b, tests[i].c);
        if (got != tests[i].expected) {
            fprintf(stderr, "sum3 case %zu: %" PRId64 "\n", i, got);
            return 1;
        }
    }
    return 0;
}

static int check_max(void) {
    const int64_t lowest = INT64_MIN;
    const int64_t highest = INT64_MAX;
    return !(csapp_m06_max2(-5, 2) == 2
          && csapp_m06_max2(100, 4) == 100
          && csapp_m06_max2(lowest, highest) == highest
          && csapp_m06_max2(highest, lowest) == highest
          && csapp_m06_max2(0, 0) == 0);
}

int main(void) {
    if (check_sum() || check_max()) {
        fputs("M06 System V ABI: FAIL\n", stderr);
        return 1;
    }
    puts("M06 System V ABI: PASS");
    return 0;
}
