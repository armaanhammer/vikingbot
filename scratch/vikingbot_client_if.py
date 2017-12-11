import argparse
import socket

def get_args():
    parser = argparse.ArgumentParser(description='vikingbot client.')

    parser.add_argument(
            '--host',
            default='192.168.0.108',
            help='host ip of the vikingbot')

    parser.add_argument(
            '--port',
            default=5000,
            type=int,
            help='port used to communicate to the vikingbot')

    return parser.parse_args()

def Main(host, port):
        mySocket = socket.socket()
        mySocket.connect((host,port))

        message = raw_input(" -> ")

        while message != 'q':
            if message:
                mySocket.send(message.encode())
                data = mySocket.recv(1024).decode()

                print ('Received from server: ' + data)

            message = raw_input(" -> ")

        mySocket.close()

if __name__ == '__main__':
    args = get_args()

    print('Host: {}'.format(args.host))
    print('Port: {}'.format(args.port))

    Main(args.host, args.port)
