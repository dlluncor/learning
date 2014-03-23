#account.make
# example working make file for use of the class Account
# files: source files:  account.cpp accountmain.cpp
#        header file:  account.h
# executable file: account
#

# first define target file : account 
#              dependencies are the object files that build the program

# 1.  Lessons # lessons_test.o

# now define how each object file is a target and list dependencies and how
#  to build that object file if any dependencies change

CFLAGS = -Wall -g -std=c++0x

lib.o: lib.cc lib.h
	g++ ${CFLAGS} -c lib.cc

lessons.o: lessons.cc lessons.h
	g++ ${CFLAGS} -c lessons.cc

lessons_test.o: lessons_test.cc lessons_test.h
	g++ ${CFLAGS} -c lessons_test.cc

main.o: main.cc lessons.h lessons_test.h
	g++ ${CFLAGS} -c main.cc

lessons: main.o lessons_test.o lessons.o lib.o
	g++ ${CFLAGS} main.o lessons_test.o lessons.o lib.o -lm -o lessons

clean:
	rm lessons lessons.o lessons_test.o main.o

# that's all