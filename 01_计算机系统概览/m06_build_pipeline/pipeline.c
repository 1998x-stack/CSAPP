#include "pipeline.h"

/*
 * The linker resolves this symbol from driver.c into pipeline.o.
 * Compile stages: gcc -E, gcc -S, gcc -c, and final link.
 */
int64_t csapp_m06_pipeline_add(int64_t left, int64_t right) {
    return left + right;
}
