#include <string.h>
#include <stdio.h>
#include <stdlib.h>
 
int main (int argc, char **argv)
{
  printf("Please enter your name: ");

  //it seems as though these buffers need to be the same size or Linux will
  //allocate them in such a way that it notices the buffer overflow
  char buffer[16];
  char program_to_run[16] = "pwd";

  gets(buffer);
  printf("Hi, %s!  You are in directory ", buffer);
  fflush(stdout);
  system(program_to_run);
}
