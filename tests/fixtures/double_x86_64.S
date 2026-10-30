    .text
    .globl csapp_double_asm
    .type csapp_double_asm, @function
csapp_double_asm:
    leaq (%rdi,%rdi), %rax
    ret
    .size csapp_double_asm, .-csapp_double_asm
    .section .note.GNU-stack,"",@progbits
