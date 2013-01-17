// Simple example to demonstrate forking child processes in C
// by Kyle Benson (Winter 2013)
// based on processes.c by Daniel

#include <sys/types.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>   // Declaration for exit()

int main()
{
  int parent_pid;
  int child_pid;

  parent_pid = getpid();

  printf("Parent (PID=%i): forking child process\n", parent_pid);
  child_pid = fork();

  if (child_pid < 0) { /* error occurred */
    fprintf(stderr, "Fork Failed");
    exit(-1);
  }
  else if (child_pid == 0) { /* child process */
    //execlp("/bin/ls", "ls", NULL);
    printf("Child (PID%i): sleeping...\n", getpid());
    sleep(2);
    printf("Child (PID%i): awake and done\n", getpid());
  }
  else { /* parent process */
    printf("Parent (PID=%i): child has PID of %i\n", parent_pid, child_pid);
    wait(NULL); 
    printf("Parent (PID=%i): Child Complete!\n", parent_pid);
    exit(0);
  }
}
