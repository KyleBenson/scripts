#include <sys/types.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>   // Declaration for exit()

int main()
{
    pid_t parent_pid;
    pid_t child_pid;

    parent_pid = getpid();

    printf("Parent (PID=%i) is forking a child process: press enter to continue....\n", parent_pid);
    getchar();
    child_pid = fork();

    if (child_pid < 0) { /* error occurred */
	fprintf(stderr, "Fork Failed");
	exit(-1);
    }
    else if (child_pid == 0) { /* child process */
	printf("Press enter to continue....\n");
	getchar();
	execlp("/bin/ls", "ls", NULL);
    }
    else { /* parent process */
      printf("Child has PID of %i\n", child_pid);
	wait(NULL);
	printf("Child Complete!\n");
	printf("Press enter to exit....\n");
	getchar();
	exit(0);
    }
}
