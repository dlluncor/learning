#account.make
# example working make file for use of the class Account
# files: source files:  account.cpp accountmain.cpp
#        header file:  account.h
# executable file: account
#

# first define target file : account 
#              dependencies are the object files that build the program

# 1.  Lessons

lessons: lessons.o
	g++ -o lessons lessons.o -rdynamic

# now define how each object file is a target and list dependencies and how
#  to build that object file if any dependencies change

lessons.o: lessons.cc lessons.h
	g++ -c -g -rdynamic -std=c++0x lessons.cc

clean:
	rm lessons lessons.o

# that's all