#define _POSIX_C_SOURCE 200809L
#include <errno.h>
#include <stdint.h>
#include <stdio.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

static int wait_child(pid_t pid, int *status) {
    pid_t found;
    do { found = waitpid(pid, status, 0); }
    while (found == -1 && errno == EINTR);
    return found == pid ? 0 : -1;
}

int main(void) {
    int channel[2];
    if (pipe(channel) != 0) { perror("pipe"); return 1; }
    volatile int local = 17;
    const pid_t child = fork();
    if (child < 0) { perror("fork"); close(channel[0]); close(channel[1]); return 1; }
    if (child == 0) {
        close(channel[0]);
        local = 99; /* fork() gives child a private virtual address space. */
        const unsigned char message = (unsigned char)local;
        const ssize_t sent = write(channel[1], &message, 1);
        close(channel[1]);
        _exit(sent == 1 ? 23 : 127);
    }
    close(channel[1]);
    unsigned char received = 0;
    ssize_t n;
    do { n = read(channel[0], &received, 1); }
    while (n == -1 && errno == EINTR);
    close(channel[0]);
    int status = 0;
    if (wait_child(child, &status) != 0) { perror("waitpid"); return 1; }
    if (n != 1 || received != 99 || local != 17 ||
        !WIFEXITED(status) || WEXITSTATUS(status) != 23) {
        fputs("M08 fork/wait/COW: FAIL\n", stderr);
        return 1;
    }
    puts("M08 fork wait: PASS");
    return 0;
}
