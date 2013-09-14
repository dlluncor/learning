#account.make
# example working make file for use of the class Account
# files: source files:  account.cpp accountmain.cpp
#        header file:  account.h
# executable file: account
#

# first define target file : account 
#              dependencies are the object files that build the program

board15: board15.o
	g++ -o board15 board15.o

# now define how each object file is a target and list dependencies and how
#  to build that object file if any dependencies change

board15.o: board15.cc board15.h
	g++ -c board15.cc

clean:
	rm board15 board15.o

# that's all