#define _POSIX_C_SOURCE 200809L
#include <signal.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

static volatile sig_atomic_t notifications = 0;
static void on_usr1(int sig) {
    if (sig == SIGUSR1) notifications = 1;
}

int main(void) {
    struct sigaction action;
    memset(&action, 0, sizeof action);
    action.sa_handler = on_usr1;
    if (sigemptyset(&action.sa_mask) != 0 || sigaction(SIGUSR1,&action,NULL) != 0) {
        perror("sigaction"); return 1;
    }
    sigset_t mask, original, pending;
    if (sigemptyset(&mask) != 0 || sigaddset(&mask,SIGUSR1) != 0 ||
        sigprocmask(SIG_BLOCK,&mask,&original) != 0) {
        perror("block"); return 1;
    }
    if (kill(getpid(),SIGUSR1) != 0 || sigpending(&pending) != 0) {
        perror("signal pending"); return 1;
    }
    if (!sigismember(&pending,SIGUSR1) || notifications != 0) {
        fputs("M08 blocked signal was unexpectedly delivered\n",stderr);
        return 1;
    }
    /* Restore original mask, which is known to be unblocked in the test process. */
    if (sigprocmask(SIG_SETMASK,&original,NULL) != 0) {
        perror("unblock"); return 1;
    }
    if (notifications != 1) {
        fputs("M08 handler was not invoked after unblock\n",stderr);
        return 1;
    }
    puts("M08 signals: PASS");
    return 0;
}
