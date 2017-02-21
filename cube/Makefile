
CC=gcc
CFLAGS=-lm -lwiringPi -Wall
SOURCES=cube.c
TARGETS=cube
#TEST=printf-unit-tests.exe

all: $(TARGETS)

cube: $(SOURCES) Makefile
	$(CC) $(CFLAGS) cube.c -o cube

#modbus-gen-write.exe: $(SOURCES) Makefile
#        $(CC) $(CFLAGS) modbus-gen-write.c -o modbus-gen-write.exe


#test: printf-unit-tests.c Makefile
#        $(CC) $(CFLAGS) printf-unit-tests.c -o $(TEST)

clean:
	rm -f $(TARGETS) $(TEST)

