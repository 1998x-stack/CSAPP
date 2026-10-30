#define _GNU_SOURCE
#include <errno.h>
#include <stdint.h>
#include <stdio.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

static int test_mapping(int flags, int expected_parent_value) {
    const long granularity = sysconf(_SC_PAGESIZE);
    if (granularity <= 0) return 1;
    const size_t length = (size_t)granularity;
    int *const p = mmap(NULL, length, PROT_READ | PROT_WRITE,
                        flags | MAP_ANONYMOUS, -1, 0);
    if (p == MAP_FAILED) { perror("mmap"); return 1; }
    p[0] = 41;
    p[length / sizeof *p - 1] = 1234;
    const pid_t pid = fork();
    if (pid < 0) { perror("fork"); munmap(p,length); return 1; }
    if (pid == 0) {
        if (p[0] != 41 || p[length / sizeof *p - 1] != 1234) _exit(2);
        p[0] = 99;
        _exit(0);
    }
    int status = 0;
    pid_t waited;
    do { waited = waitpid(pid,&status,0); } while (waited < 0 && errno == EINTR);
    const int ok = waited == pid && WIFEXITED(status) && WEXITSTATUS(status) == 0
        && p[0] == expected_parent_value && p[length / sizeof *p - 1] == 1234;
    if (munmap(p,length) != 0) { perror("munmap"); return 1; }
    return ok ? 0 : 1;
}

int main(void) {
    if (test_mapping(MAP_PRIVATE,41) || test_mapping(MAP_SHARED,99)) {
        fputs("M08 mmap fork: FAIL\n",stderr);
        return 1;
    }
    puts("M08 mmap COW: PASS");
    return 0;
}
