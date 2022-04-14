import socket
import time
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 2022
s.connect(('192.168.1.120', port))
print(s.recv(1024))
s.send('Hi, i am Willis'.encode())
time.sleep(5)
s.send('EXIT'.encode())
time.sleep(2)
print(s.recv(1024).decode("utf-8"))
# time.sleep(5)
s.close()