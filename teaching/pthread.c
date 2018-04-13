// Simple example of using pthreads in C.
// Adapted from http://cs.gmu.edu/~white/CS571/Examples/Pthread/create.c
// Downloaded 1/24/2013
//
// TO COMPILE:
// gcc -pthread pthread.c

#include <stdio.h>
#include <pthread.h> 

#define sleep_time 2

main()  {
  pthread_t f2_thread, f1_thread; 
  void *f2(), *f1(); //forward declarations necessary

  int shared_var = 0;

  printf("Main: PID=%d\n", getpid());
  printf("Main: shared_var=%d\n", shared_var);
  printf("Main: spawning 2 threads...\n");

  pthread_create(&f1_thread,NULL,f1,&shared_var);
  pthread_create(&f2_thread,NULL,f2,&shared_var);
  pthread_join(f1_thread,NULL);
  pthread_join(f2_thread,NULL);

  printf("Main: shared_var=%d\n", shared_var);
}

// Note that these definitions MUST appear after main,
// or the compiler will complain about the argument type being
// int *x instead of a void *x.
// We are tricking the compiler into thinking they're the
// latter via the forward declarations in main.
void *f1(int *x){
  printf("f1: PID=%d\n", getpid());
  (*x) = 1;
  sleep(sleep_time);
  printf("thread 1: shared_var=%d\n",*x);
  pthread_exit(0); 
}

void *f2(int *x){
  printf("f2: PID=%d\n", getpid());
  (*x) = 2;
  sleep(sleep_time);
  printf("thread 2: shared_var=%d\n",*x);
  pthread_exit(0); 
}

