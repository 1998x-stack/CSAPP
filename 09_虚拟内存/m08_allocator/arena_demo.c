#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

/* Small fixed-size bump allocator demonstration, not malloc/free. */
struct arena {
    unsigned char data[256];
    size_t offset;
};

static void *allocate(struct arena *a, size_t n, size_t align) {
    if (!a || !align || (align & (align-1)) != 0) return NULL;
    if (a->offset > sizeof a->data) return NULL;
    const size_t base = (size_t)(uintptr_t)a->data;
    if (base > SIZE_MAX - a->offset) return NULL;
    const size_t here = base + a->offset;
    if (here > SIZE_MAX - (align-1)) return NULL;
    const size_t padding = (align - (here & (align-1))) & (align-1);
    if (padding > sizeof a->data - a->offset ||
        n > sizeof a->data - a->offset - padding) return NULL;
    void *result = a->data + a->offset + padding;
    a->offset += padding + n;
    return result;
}

int main(void) {
    struct arena a = {0};
    unsigned char *p = allocate(&a,64,16);
    uint64_t *q = allocate(&a,sizeof(uint64_t),_Alignof(uint64_t));
    if (!p || !q || (uintptr_t)p % 16 || (uintptr_t)q % _Alignof(uint64_t)) return 1;
    memset(p,0xa5,64);
    *q = UINT64_C(0x1234567890abcdef);
    for (size_t i=0;i<64;i++) if(p[i]!=0xa5) return 1;
    if (*q!=UINT64_C(0x1234567890abcdef)) return 1;
    const size_t before=a.offset;
    if (allocate(&a, SIZE_MAX, 8) != NULL || a.offset != before) return 1;
    if (allocate(&a, 1, 3) != NULL || a.offset != before) return 1;
    if (allocate(&a, 257, 1) != NULL || a.offset != before) return 1;
    if (!allocate(&a,0,1) || a.offset != before) return 1;
    puts("M08 arena allocator: PASS");
    return 0;
}
