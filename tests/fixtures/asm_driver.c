#include <stdint.h>
#include <stdio.h>

/* System V x86-64 ABI: first argument in %rdi, return value in %rax. */
extern int64_t csapp_double_asm(int64_t value);

int main(void) {
    if (csapp_double_asm(INT64_C(21)) != INT64_C(42) ||
        csapp_double_asm(INT64_C(-7)) != INT64_C(-14) ||
        csapp_double_asm(INT64_C(0)) != INT64_C(0)) {
        return 1;
    }
    puts("M03 ASM smoke: ok");
    return 0;
}
