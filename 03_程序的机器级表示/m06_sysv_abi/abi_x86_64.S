    .text
    .globl csapp_m06_sum3
    .type csapp_m06_sum3, @function
csapp_m06_sum3:
    movq %rdi, %rax
    addq %rsi, %rax
    addq %rdx, %rax
    ret
    .size csapp_m06_sum3, .-csapp_m06_sum3

    .globl csapp_m06_max2
    .type csapp_m06_max2, @function
csapp_m06_max2:
    movq %rdi, %rax
    cmpq %rsi, %rax
    cmovl %rsi, %rax
    ret
    .size csapp_m06_max2, .-csapp_m06_max2
    .section .note.GNU-stack,"",@progbits
