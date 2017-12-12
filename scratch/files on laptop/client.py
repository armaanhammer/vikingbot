import socket
 
def Main():
        host = '192.168.0.108'
        port = 5000
         
        mySocket = socket.socket()
        mySocket.connect((host,port))
         
        message = raw_input(" -> ")
         
        while message != 'q':
                mySocket.send(message.encode())
                data = mySocket.recv(1024).decode()
                 
                print 'Received from server: ' + data
                 
                message = raw_input(" -> ")
                 
        mySocket.close()
 
if __name__ == '__main__':
    Main()
