import socket
import threading
name ="Willis"
def recv(sock, addr):
    global name
    print('addr', addr)
    print('name', name)
    print('sock', sock)
    sock.sendto(name.encode('utf-8'), addr)
    while True:
        data = sock.recv(1024)
        recvMsg = data.decode('utf-8')
        print(recvMsg)

        if recvMsg.lower() =='EXIT'.lower():
            break

def send(sock, addr):
    while True:
        string = input('')
        message = 'Server: ' + string
        data = message.encode('utf-8')
        sock.sendto(data, addr)
        if string.lower() =='EXIT'.lower():
            break

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = '10.22.98.67'
port = 2022
server = (host, port)
s.bind(server)
msg, clientAddr = s.recvfrom(1024)
name = msg.decode('utf-8')
tr = threading.Thread(target=recv, args=(s, clientAddr), daemon=True)
ts = threading.Thread(target=send, args=(s, clientAddr))
try:
    tr.start()
    ts.start()
    ts.join()
except ConnectionResetError:
    print('Error: someone left unexpected. ')

s.close()