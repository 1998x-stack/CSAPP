/* A loop unrolling exercise. Runtime speed varies by compiler/machine: only
 * numerical equivalence is a test; use --bench for observational timing.
 * Unsigned arithmetic is modulo 2^64 by C11 definition.
 */
#define _POSIX_C_SOURCE 200809L
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

static uint64_t sum_scalar(const uint64_t *a, size_t n) {
    uint64_t result = 0;
    for (size_t i = 0; i < n; i++) result += a[i];
    return result;
}

static uint64_t sum_unrolled4(const uint64_t *a, size_t n) {
    uint64_t a0 = 0, a1 = 0, a2 = 0, a3 = 0;
    size_t i = 0;
    for (; n - i >= 4; i += 4) {
        a0 += a[i]; a1 += a[i+1]; a2 += a[i+2]; a3 += a[i+3];
    }
    uint64_t result = a0 + a1 + a2 + a3;
    for (; i < n; i++) result += a[i];
    return result;
}

static int selftest(void) {
    uint64_t numbers[130];
    for (size_t i = 0; i < 130; i++) numbers[i] = (uint64_t)(i*i + 7U);
    numbers[0] = UINT64_MAX;
    const size_t sizes[] = {0,1,2,3,4,5,7,8,9,15,16,17,31,32,63,64,65,129,130};
    for (size_t i = 0; i < sizeof sizes / sizeof sizes[0]; i++) {
        const size_t n = sizes[i];
        if (sum_scalar(numbers,n) != sum_unrolled4(numbers,n)) {
            fprintf(stderr,"M07 unrolled mismatch at n=%zu\n",n);
            return 1;
        }
    }
    if (sum_scalar(NULL,0) != 0 || sum_unrolled4(NULL,0) != 0) return 1;
    puts("M07 loop optimization: PASS");
    return 0;
}

static double seconds(void) {
    struct timespec ts;
    if (clock_gettime(CLOCK_MONOTONIC, &ts) != 0) return -1;
    return (double)ts.tv_sec + (double)ts.tv_nsec * 1e-9;
}

static int benchmark(void) {
    const size_t n = 1U << 18;
    const unsigned rounds = 80;
    uint64_t *data = malloc(n * sizeof *data);
    if (!data) return 1;
    for (size_t i = 0; i < n; i++) data[i] = (uint64_t)(i + 1);
    volatile uint64_t observable = 0;
    const double start_scalar = seconds();
    for (unsigned i = 0; i < rounds; i++) observable = observable ^ sum_scalar(data,n);
    const double end_scalar = seconds();
    const double start_unrolled = seconds();
    for (unsigned i = 0; i < rounds; i++) observable = observable ^ sum_unrolled4(data,n);
    const double end_unrolled = seconds();
    free(data);
    if (start_scalar < 0 || start_unrolled < 0) return 1;
    printf("scalar seconds=%.6f, unrolled4 seconds=%.6f (no performance threshold)\n",
           end_scalar - start_scalar, end_unrolled - start_unrolled);
    printf("observable checksum=%" PRIu64 "\n", (uint64_t)observable);
    puts("M07 loop benchmark: PASS");
    return 0;
}

int main(int argc, char **argv) {
    if (argc == 1) return selftest();
    if (argc == 2 && strcmp(argv[1],"--bench") == 0)
        return selftest() == 0 ? benchmark() : 1;
    fputs("usage: loop_demo [--bench]\n",stderr);
    return 2;
}
