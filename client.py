from socket import *


c = socket(AF_INET, SOCK_STREAM)
c.connect( ('127.0.0.1', 1445))
result = c.recv(1000)

print("Result:" , result)



c.send(b'login admin admin')
result = c.recv(1000)
print("Result:" , result)

c.send(b'close')
c.close()