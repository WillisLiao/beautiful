import socket
import threading
import logging
name = ""
logging.basicConfig(filename='std.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logging.warning('This message will get logged on to a file')
#now we will Create and configure logger 
logging.basicConfig(filename="std.log", 
					format='%(asctime)s %(message)s', 
					filemode='w') 

#Let us Create an object 
logger=logging.getLogger() 

#Now we are going to Set the threshold of logger to DEBUG 
logger.setLevel(logging.DEBUG) 
def recv(sock, addr):
    global name
    print('addr',addr)
    print('name',name)
    print('sock',sock)
    sock.sendto(name.encode('utf-8'), addr)
    while True:
        data = sock.recv(1024)
        print(data.decode('utf-8'))

def send(sock, addr):
    while True:
        string = input('')
        message = name +" : " +string
        data = message.encode('utf-8')
        sock.sendto(data,addr)
        logging.info(string)
        if string.lower() == 'EXIT'.lower():
            break


print('-------------------%s-------------------'%name)

def main():
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    host = socket.gethostname()
    host ='10.22.75.174'

    port = 9999
    server = (host,port)
    tr = threading.Thread(target=recv, args=(s, server),daemon=True)
    ts = threading.Thread(target=send, args=(s, server))
    tr.start()
    ts.start()
    ts.join()
    s.close()

if __name__ == '__main__':
    print("-----歡迎來到聊天室,退出聊天室請輸入'EXIT(不分大小寫)'-----")
    name = input("請輸入你的名稱")
    print('-------------------%s-------------------'%name)
    main()



