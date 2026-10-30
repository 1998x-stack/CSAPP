/* M07: a deliberately small, bounded Y86-64 teaching interpreter.
 * Supported instructions: halt (00), nop (10), rrmovq (20), irmovq (30),
 * addq (60), subq (61), andq (62), xorq (63), jmp (70), je (73).
 * This is NOT the full CSAPP Y86-64 ISA or pipelined processor.
 */
#include <inttypes.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

enum { REG_COUNT = 15, RNONE = 15, MAX_STEPS = 100 };
enum status { AOK, HLT, ADR, INS, LIMIT };
struct cpu {
    uint64_t reg[REG_COUNT];
    uint64_t pc;
    bool zf;
    bool sf;
    bool of;
    enum status status;
};

static bool immediate(const uint8_t *program, size_t size, uint64_t pos,
                      uint64_t *result) {
    if (pos > size || size - (size_t)pos < 8U) return false;
    uint64_t value = 0;
    for (unsigned i = 0; i < 8; i++) value |= (uint64_t)program[(size_t)pos + i] << (8U * i);
    *result = value;
    return true;
}

static void step(struct cpu *cpu, const uint8_t *program, size_t size) {
    if (cpu->pc >= size) { cpu->status = ADR; return; }
    const uint64_t start = cpu->pc;
    const uint8_t op = program[(size_t)start];
    if (op == 0x00) { cpu->status = HLT; cpu->pc++; return; }
    if (op == 0x10) { cpu->pc++; return; }
    if (op == 0x70 || op == 0x73) {
        uint64_t destination = 0;
        if (!immediate(program, size, start + 1U, &destination)) { cpu->status = ADR; return; }
        if (op == 0x70 || cpu->zf) cpu->pc = destination;
        else cpu->pc += 9U;
        return;
    }
    if (op != 0x20 && op != 0x30 && (op < 0x60 || op > 0x63)) {
        cpu->status = INS; return;
    }
    if (start + 1U >= size) { cpu->status = ADR; return; }
    const uint8_t r = program[(size_t)start + 1U];
    const unsigned a = r >> 4, b = r & 0x0fU;
    if (b >= REG_COUNT || (op == 0x30 ? a != RNONE : a >= REG_COUNT)) {
        cpu->status = INS; return;
    }
    if (op == 0x20) { cpu->reg[b] = cpu->reg[a]; cpu->pc += 2U; return; }
    if (op == 0x30) {
        uint64_t value = 0;
        if (!immediate(program, size, start + 2U, &value)) { cpu->status = ADR; return; }
        cpu->reg[b] = value;
        cpu->pc += 10U;
        return;
    }
    const uint64_t left = cpu->reg[a];
    const uint64_t right = cpu->reg[b];
    uint64_t result = 0;
    bool overflow = false;
    switch (op) {
    case 0x60: /* addq rA,rB */
        result = right + left;
        overflow = (((~(right ^ left)) & (right ^ result)) >> 63) != 0U;
        break;
    case 0x61: /* subq rA,rB => rB - rA */
        result = right - left;
        overflow = (((right ^ left) & (right ^ result)) >> 63) != 0U;
        break;
    case 0x62: result = right & left; break;
    case 0x63: result = right ^ left; break;
    default: cpu->status = INS; return;
    }
    cpu->reg[b] = result;
    cpu->zf = result == 0;
    cpu->sf = (result >> 63) != 0;
    cpu->of = overflow;
    cpu->pc += 2U;
}

static enum status run(struct cpu *cpu, const uint8_t *program, size_t size) {
    for (unsigned count = 0; count < MAX_STEPS && cpu->status == AOK; count++) {
        step(cpu, program, size);
    }
    if (cpu->status == AOK) cpu->status = LIMIT;
    return cpu->status;
}

static int check(bool condition, const char *name) {
    if (condition) return 0;
    fprintf(stderr, "Y86 test failed: %s\n", name);
    return 1;
}

int main(void) {
    int failures = 0;
    /* irmovq $7,%rax ; irmovq $5,%rbx ; addq %rbx,%rax ; halt */
    const uint8_t program[] = {
        0x30, 0xf0, 7,0,0,0,0,0,0,0,
        0x30, 0xf3, 5,0,0,0,0,0,0,0,
        0x60, 0x30, 0x00
    };
    struct cpu cpu = {0};
    failures += check(run(&cpu, program, sizeof program) == HLT, "halt");
    failures += check(cpu.reg[0] == 12, "register result 7+5=12");
    failures += check(cpu.pc == sizeof program, "final PC");
    failures += check(!cpu.zf && !cpu.sf && !cpu.of, "condition codes");

    /* subq %rbx,%rax produces zero; je jumps over an invalid opcode. */
    const uint8_t branch[] = {
        0x30,0xf0, 9,0,0,0,0,0,0,0,
        0x30,0xf3, 9,0,0,0,0,0,0,0,
        0x61,0x30, 0x73, 32,0,0,0,0,0,0,0,
        0xff, 0x00
    };
    memset(&cpu, 0, sizeof cpu);
    failures += check(run(&cpu, branch, sizeof branch) == HLT, "conditional jump");
    failures += check(cpu.zf && cpu.reg[0] == 0, "zero flag");

    const uint8_t bad_register[] = { 0x20, 0xf0, 0x00 };
    memset(&cpu, 0, sizeof cpu);
    failures += check(run(&cpu, bad_register, sizeof bad_register) == INS, "invalid register");
    const uint8_t truncated[] = { 0x30, 0xf0, 1, 2 };
    memset(&cpu, 0, sizeof cpu);
    failures += check(run(&cpu, truncated, sizeof truncated) == ADR, "truncated immediate");
    const uint8_t invalid[] = { 0xff };
    memset(&cpu, 0, sizeof cpu);
    failures += check(run(&cpu, invalid, sizeof invalid) == INS, "invalid opcode");
    const uint8_t loop[] = { 0x70, 0,0,0,0,0,0,0,0 };
    memset(&cpu, 0, sizeof cpu);
    failures += check(run(&cpu, loop, sizeof loop) == LIMIT, "step bound");
    const uint8_t bad_jump[] = { 0x70, 0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff };
    memset(&cpu, 0, sizeof cpu);
    failures += check(run(&cpu, bad_jump, sizeof bad_jump) == ADR, "jump address bound");
    const uint8_t overflow_test[] = {
        0x30,0xf0, 0xff,0xff,0xff,0xff,0xff,0xff,0xff,0x7f,
        0x30,0xf3, 1,0,0,0,0,0,0,0,
        0x60,0x30,0x00
    };
    memset(&cpu, 0, sizeof cpu);
    failures += check(run(&cpu, overflow_test, sizeof overflow_test) == HLT, "overflow case halts");
    failures += check(cpu.of && cpu.sf && !cpu.zf && cpu.reg[0] == UINT64_C(0x8000000000000000),
                      "signed overflow flags, defined unsigned operation");
    if (failures) return 1;
    puts("M07 Y86 subset: PASS");
    return 0;
}
