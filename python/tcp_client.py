from socket import *

HOST = 'localhost'
PORT = 29876 # same port as the server
ADDR = (HOST, PORT)
BUFSIZE = 4096

client = socket(AF_INET, SOCK_STREAM)
client.connect((ADDR))

# Receive from data from the server.
data = client.recv(BUFSIZE)
print data
client.close()
