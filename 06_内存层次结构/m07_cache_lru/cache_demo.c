/* Set-associative, write-allocate LRU cache simulator (educational subset).
 * Address-only trace operations: L, S and M. One block per valid access;
 * malformed/cross-block inputs return a failure. No cache data is modeled.
 */
#include <inttypes.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct line { uint64_t tag, stamp; bool valid; };
struct cache {
    struct line *lines;
    unsigned s, E, b;
    uint64_t clock;
    unsigned hits, misses, evictions;
};

static bool cache_init(struct cache *c, unsigned s, unsigned E, unsigned b) {
    if (s > 12U || E == 0 || E > 16U || b >= 64U || s + b >= 64U) return false;
    const size_t sets = (size_t)1U << s;
    if (sets > SIZE_MAX / E) return false;
    c->lines = calloc(sets * E, sizeof *c->lines);
    if (!c->lines) return false;
    c->s=s; c->E=E; c->b=b; c->clock=0;
    c->hits=c->misses=c->evictions=0;
    return true;
}

static void access_block(struct cache *c, uint64_t addr) {
    const uint64_t set_mask = ((UINT64_C(1) << c->s) - 1U);
    const size_t set_id = (size_t)((addr >> c->b) & set_mask);
    const uint64_t tag = addr >> (c->s + c->b);
    struct line *set = c->lines + set_id * c->E;
    struct line *choice = NULL;
    for (unsigned i=0; i<c->E; i++) {
        if (set[i].valid && set[i].tag == tag) {
            c->hits++;
            set[i].stamp = ++c->clock;
            return;
        }
        if (!set[i].valid) choice=&set[i];
    }
    c->misses++;
    if (!choice) {
        choice=&set[0];
        for (unsigned i=1;i<c->E;i++) if (set[i].stamp < choice->stamp) choice=&set[i];
        c->evictions++;
    }
    choice->tag=tag;
    choice->valid=true;
    choice->stamp=++c->clock;
}

static bool access_operation(struct cache *c, char op, uint64_t addr, unsigned size) {
    if (op=='I') return true;
    if (op!='L' && op!='S' && op!='M') return false;
    if (size == 0U) return false;
    const uint64_t offset_mask = (UINT64_C(1) << c->b) - 1U;
    if ((uint64_t)(size-1U) > offset_mask - (addr & offset_mask)) return false;
    access_block(c,addr);
    if (op=='M') access_block(c,addr);
    return true;
}

static int selftest(void) {
    struct cache c={0};
    if (!cache_init(&c,1,1,2)) return 1;
    const struct {char op; uint64_t addr; unsigned size;} checks[]={
        {'L',0,1},{'L',0,1},{'L',8,1},{'M',8,1},{'L',4,1},{'L',0,1}
    };
    for(size_t i=0;i<sizeof checks/sizeof checks[0];i++)
        if(!access_operation(&c,checks[i].op,checks[i].addr,checks[i].size))return 1;
    const bool first=(c.hits==3 && c.misses==4 && c.evictions==2);
    free(c.lines);
    memset(&c,0,sizeof c);
    if (!cache_init(&c,0,2,2)) return 1;
    const uint64_t lru[]={0,4,0,8,0,4};
    for(size_t i=0;i<sizeof lru/sizeof lru[0];i++)access_block(&c,lru[i]);
    const bool second=(c.hits==2 && c.misses==4 && c.evictions==2);
    const bool cross_block_rejected=!access_operation(&c,'L',3,2);
    free(c.lines);
    memset(&c,0,sizeof c);
    const bool invalid_rejected=!cache_init(&c,13,1,2) && !cache_init(&c,1,0,2)
                              && !cache_init(&c,1,1,63);
    if (!first || !second || !cross_block_rejected || !invalid_rejected) {
        fputs("M07 cache LRU: FAIL\n",stderr);
        return 1;
    }
    puts("M07 cache LRU: PASS");
    return 0;
}

static int trace_file(const char *path, unsigned s,unsigned E,unsigned b) {
    struct cache c={0};
    if (!cache_init(&c,s,E,b)) return 2;
    FILE *fp=fopen(path,"r");
    if (!fp) {perror("trace open");free(c.lines);return 2;}
    char line[256];
    unsigned line_no=0;
    int result=0;
    while (fgets(line,sizeof line,fp)) {
        line_no++;
        char op='\0', extra='\0';
        uint64_t addr=0;
        unsigned size=0;
        if(line[0]=='\n' || line[0]=='#')continue;
        const int matched=sscanf(line," %c %" SCNx64 ",%u %c",&op,&addr,&size,&extra);
        if(matched!=3 || !access_operation(&c,op,addr,size)) {
            fprintf(stderr,"invalid trace line %u\n",line_no);
            result=2;
            break;
        }
    }
    if(ferror(fp))result=2;
    fclose(fp);
    if(!result)printf("hits:%u misses:%u evictions:%u\n",c.hits,c.misses,c.evictions);
    free(c.lines);
    return result;
}

static bool parse_unsigned(const char *text,unsigned *number) {
    char tail='\0';
    return sscanf(text,"%u%c",number,&tail)==1;
}

int main(int argc,char **argv) {
    if(argc==1)return selftest();
    if(argc==6 && strcmp(argv[1],"--trace")==0) {
        unsigned s=0,E=0,b=0;
        if(!parse_unsigned(argv[3],&s)||!parse_unsigned(argv[4],&E)||!parse_unsigned(argv[5],&b))return 2;
        return trace_file(argv[2],s,E,b);
    }
    fputs("usage: cache_demo [--trace path s E b]\n",stderr);
    return 2;
}
