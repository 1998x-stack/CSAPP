#include "arith.h"
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
int main(void) {
    struct sample { int64_t a, b, c, expected; };
    const struct sample cases[] = {
        {1,2,3,6}, {-7,3,2,-2}, {0,0,0,0},
        {INT64_C(2147483647),1,0,INT64_C(2147483648)},
        {INT64_MIN,1,0,INT64_MIN+1}
    };
    for (size_t i=0; i<sizeof cases/sizeof cases[0]; i++) {
        const struct sample *t = &cases[i];
        if (m08_sum_3(t->a,t->b,t->c) != t->expected) {
            fprintf(stderr,"M08 linker sample failed at %zu\n",i);
            return 1;
        }
    }
    if (m08_xor_mask(UINT64_C(0xa5a5),UINT64_C(0x00ff)) != UINT64_C(0xa55a)) return 1;
    puts("M08 linker: PASS");
    return 0;
}
