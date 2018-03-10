Flags = -Wreturn-type -Wall -std=c++11
CPP = g++

main : Makefile main.o vectortest.o
	$(CPP) $(Flags) -o main main.o vectortest.o

main.o : Makefile main.cpp vectortest.h tasks.h
	$(CPP) -c $(Flags) main.cpp -o main.o

vectortest.o : Makefile vectortest.cpp vectortest.h
	$(CPP) -c $(Flags) vectortest.cpp -o vectortest.o
