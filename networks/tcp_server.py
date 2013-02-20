from socket import *

HOST = ''
PORT = 29876
ADDR = (HOST, PORT)
BUFSIZE = 4096

serv = socket(AF_INET, SOCK_STREAM)

# Bind socket to the address
serv.bind((ADDR))
serv.listen(5)  # 5 is max number of queued connections to allow.
print 'listening...'

conn,addr = serv.accept()  # accept the connection.
print '....connected'

# Send info.
info = 'TEST' * 10000
info += '/end'
conn.send(info)

conn.close()
