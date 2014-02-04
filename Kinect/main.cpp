#include <stdio.h>
#include <sys/socket.h>
// #include <sys/un.h>
#include <linux/un.h>
#include <sys/types.h>
#include <signal.h>
#include <wait.h>
#include <unistd.h>
#include <string.h>
#include <vector>
#include "kinect.h"

int socket_fd;
std::vector<pid_t> children;

static void interrupt_handler(int signo) {
  printf("arret du programme\n");
  for(std::vector<pid_t>::iterator it = children.begin();
      it != children.end(); it++) {
    kill(*it, SIGKILL);
    waitpid(*it, NULL, 0);
  }

  close(socket_fd);
  unlink("/tmp/togetic-k");
}

int connection_handler(int connection_fd) {
  signed int x = 0;
  signed int y = 0;
  signed int z = 0;
  size_t len = 0;

  while(1) {
    char buffer[25] = {0};
    len = sprintf(buffer, "T %d %d %d\n", x, y, z);
    if(len > 0) {
      write(connection_fd, buffer, len);
    }
    x = (x + 1) % 4096;
  }
  return 0;
}

int main(int argc, char ** argv) {
  Kinect k("Togetic");
  openni::Status rc = openni::STATUS_OK;
  rc = k.Init(argc, argv);
  if (rc != openni::STATUS_OK)
  {
    return 1;
  }
  k.Run();
  return 0;
}

int _main(void) {
  struct sockaddr_un address;
  int connection_fd;
  socklen_t address_length;
  pid_t child;

  if(signal(SIGINT, interrupt_handler) == SIG_ERR) {
    printf("An error occurred while setting a signal handler.\n");
    return 1;
  }

  socket_fd = socket(PF_UNIX, SOCK_STREAM, 0);
  if(socket_fd < 0) {
    printf("socket() failed\n");
    return 1;
  }

  unlink("/tmp/togetic-k");

  memset(&address, 0, sizeof(struct sockaddr_un));
  address.sun_family = AF_UNIX;
  snprintf(address.sun_path, UNIX_PATH_MAX, "/tmp/togetic-k");

  if(bind(socket_fd,
        (struct sockaddr *) &address,
        sizeof(struct sockaddr_un)) != 0) {
    printf("bind() failed\n");
    return 1;
  }

  if(listen(socket_fd, 5) != 0) {
    printf("listen() failed\n");
    return 1;
  }

  while((connection_fd = accept(socket_fd, 
          (struct sockaddr *) &address,
          &address_length)) > -1) {
    child = fork();
    if(child == 0) {
      return connection_handler(connection_fd);
    }
    else {
      children.push_back(child);
      close(connection_fd);
    }
  }

  return 0;
}
