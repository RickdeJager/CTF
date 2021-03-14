all:	module.c
	gcc -c -Wall -Werror -fpic module.c `pkg-config --cflags --libs gtk+-3.0`
	gcc -shared -o libhack.so module.o `pkg-config --cflags --libs gtk+-3.0`
