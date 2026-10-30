#include "pipeline.h"

#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>

struct sample {
    int64_t a;
    int64_t b;
    int64_t expected;
};

int main(void) {
    const struct sample samples[] = {
        { 1, 2, 3 },
        { -10, 15, 5 },
        { INT64_C(2147483647), 1, INT64_C(2147483648) },
        { -9, -7, -16 },
        { 0, 0, 0 },
    };
    for (size_t i = 0; i < sizeof(samples) / sizeof(samples[0]); ++i) {
        const int64_t actual = csapp_m06_pipeline_add(samples[i].a, samples[i].b);
        if (actual != samples[i].expected) {
            fprintf(stderr, "case %zu: got %" PRId64 "\n", i, actual);
            return 1;
        }
    }
    puts("M06 pipeline: PASS");
    return 0;
}
