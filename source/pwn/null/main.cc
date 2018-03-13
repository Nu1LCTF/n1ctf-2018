#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <errno.h>
#include <unistd.h>
#include <pthread.h>
#include <sys/syscall.h>

#define ON_ERR(x) if((x) < 0) 

void exit_group(int status) {
	syscall(__NR_exit_group, status);
}

#define prints(s) write(1, s, sizeof(s) - 1)
using PrintFunc = void (*)(const void* buf, size_t size);
void do_print(const void* buf, size_t size) {
	//write(1, buf, size);
	prints("data neutralized\n");	
}
char pad[8]; 
PrintFunc print = NULL;

__attribute__((noinline)) int readint(void) {
	char buffer[0x10];
	
	memset(buffer, 0, sizeof(buffer));
	for(int i = 0; i < sizeof(buffer); i++) {
		if(read(0, &buffer[i], 1) <= 0) {
			exit_group(1);
		}
		if(buffer[i] == '\n') {
			buffer[i] == 0;
			break;
		}
	}
	return atoi(buffer);
}

void nread(void* buf, size_t size) {
	size_t read_size = 0;
	int r;
	char* p = reinterpret_cast<char*>(buf);
	while(read_size < size) {
		r = read(0, p + read_size, size); 	// buggy
		if(r <= 0) {
			prints("I/O error\n");
			exit_group(1);
		}
		read_size += r;
	}
	return;
}

void* thread_main(void* arg) {
	//system("cat banner");
	prints("***************************************\n");
	prints("* Welcome to Nu1L's /dev/null service *\n");
	prints("***************************************\n");
	prints("1. use /dev/null service\n");
	prints("2. exit\n");
	print = do_print;
	while(true) {
		prints("Action: ");
		int r = readint();
		if(r == 1) {
			prints("Size: ");
			int sz = readint();
			if(sz < 0 || sz > 0x4000) {
				prints("Invalid size.\n");
				continue;
			}
			void* buf = malloc(sz);
			prints("Content? (0/1): ");
			int doit = readint();
			if(doit) {
				prints("Input: ");
				nread(buf, sz);
				print(buf, sz);
			}
		} else if(r == 2) {
			break;
		} else if (r == 1337) {
			system("/usr/bin/id");
		} else {
			prints("Invalid command.\n");
		}
	}
	exit_group(0);
}

int main(int argc, char* argv[], char* envp[]) {
	pthread_t thread;
	char buffer[0x100];

	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);

	memset(buffer, 0, sizeof(buffer));
	puts("Enter secret password: ");
	if(!fgets(buffer, sizeof(buffer), stdin)) {
		_exit(1);
	}
	sleep(3);
	if(strcmp(buffer, "i'm ready for challenge\n")) {
		puts("Access denied");
		_exit(1);
	}
	ON_ERR(pthread_create(&thread, NULL, thread_main, NULL)) {
		puts("Internal error, contact admin.");
		_exit(1);
	}
	pthread_join(thread, NULL);
	return 0;
}
