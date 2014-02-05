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
#include <sstream>

int socket_fd;
std::vector<pid_t> children;
float x = 0;
float y = 0;
float z = 0;

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
  printf("Nouvelle connexion\n");
  fflush(stdout);
  size_t len = 0;

  while(1) {
    std::ostringstream oss;
    oss << "T " << x << " " << y << " " << z << "\n";
    write(connection_fd, oss.str().c_str(), oss.str().size());
  }
  return 0;
}

void server(void) {
  printf("Demarrage du serveur\n");
  fflush(stdout);
  struct sockaddr_un address;
  int connection_fd;
  socklen_t address_length;
  pid_t child;

  if(signal(SIGINT, interrupt_handler) == SIG_ERR) {
    printf("An error occurred while setting a signal handler.\n");
    return;
  }

  socket_fd = socket(PF_UNIX, SOCK_STREAM, 0);
  if(socket_fd < 0) {
    printf("socket() failed\n");
    return;
  }

  unlink("/tmp/togetic-k");

  memset(&address, 0, sizeof(struct sockaddr_un));
  address.sun_family = AF_UNIX;
  snprintf(address.sun_path, UNIX_PATH_MAX, "/tmp/togetic-k");

  if(bind(socket_fd,
        (struct sockaddr *) &address,
        sizeof(struct sockaddr_un)) != 0) {
    printf("bind() failed\n");
    return;
  }

  if(listen(socket_fd, 5) != 0) {
    printf("listen() failed\n");
    return;
  }

  while((connection_fd = accept(socket_fd, 
          (struct sockaddr *) &address,
          &address_length)) > -1) {
    child = fork();
    if(child == 0) {
      printf("coucou tu veux voir ma ...\n");
      fflush(stdout);
      exit(connection_handler(connection_fd));
    }
    else {
      children.push_back(child);
      close(connection_fd);
    }
  }
}

int main(int argc, char ** argv) {
  Kinect k("Togetic", &x, &y, &z);
  openni::Status rc = openni::STATUS_OK;
  rc = k.Init(argc, argv);
  if (rc != openni::STATUS_OK)
  {
    return 1;
  }

  pid_t child;
  child = fork();

  if(child == 0) {
    server();
  }
  else {
    printf("Lancement de la kinect\n");
    fflush(stdout);
    k.Run();
    // exit(0);
  }
  return 0;
}

