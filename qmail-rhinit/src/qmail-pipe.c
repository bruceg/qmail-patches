#include <signal.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

int splitargs(argc,argv)
int argc;
char** argv;
{
  int i;
  for(i = 1; i < argc; i++) {
    if(argv[i][0] == '-' &&
       argv[i][1] == '-' &&
       argv[i][2] == 0) {
      argv[i] = 0;
      break;
    }
  }
  if(i == 1 || i >= argc-1)
    return -1;
  return i+1;
}

int writer_pid;
int reader_pid;

int fork_writer(argv,pipefd)
char** argv;
int* pipefd;
{
  switch(writer_pid = fork()) {
    case -1:
      return 1;
    case 0:
      close(pipefd[0]);
      if(dup2(pipefd[1], 1) == -1 || close(pipefd[1]) == -1) exit(1);
      execvp(argv[0], argv);
      exit(1);
  }
  return 0;
}

int fork_reader(argv,pipefd)
char** argv;
int* pipefd;
{
  switch(reader_pid = fork()) {
    case -1:
      return 1;
    case 0:
      close(pipefd[1]);
      if(dup2(pipefd[0], 0) == -1 || close(pipefd[0]) == -1) exit(1);
      execvp(argv[0], argv);
      exit(1);
  }
  return 0;
}

int main(argc,argv)
int argc;
char** argv;
{
  int pid;
  int status;
  int p[2];
  int cmd2 = splitargs(argc, argv);
  if(cmd2 < 0) return 1;
  if(pipe(p) == -1) return 1;
  if(fork_writer(argv+1, p)) return 1;
  if(fork_reader(argv+cmd2, p)) {
    kill(writer_pid, SIGTERM);
    return 1;
  }
  for(;;) {
    pid = wait(&status);
    if(pid == writer_pid) {
      writer_pid = -1;
      kill(reader_pid, SIGTERM);
    } else {
      reader_pid = -1;
      if(writer_pid > 0)
        kill(writer_pid, SIGTERM);
      return WIFEXITED(status) ? WEXITSTATUS(status) : 1;
    }
  }
}
