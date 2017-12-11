import argparse
import socket
import time
#import yaml

#from vikingbot import vikingbot_12DOF

def get_args():
    parser = argparse.ArgumentParser(description='vikingbot server.')

    parser.add_argument(
            '--host',
            default='192.168.0.108',
            help='host ip of the vikingbot')

    parser.add_argument(
            '--port',
            default=5000,
            type=int,
            help='port used to communicate to the vikingbot')

#    parser.add_argument(
#            '-c',
#            '--config_file',
#            default='config_12DOF.yaml',
#            help='vikingbot configuration file')
#
#    return parser.parse_args()

#def initialize_vikingbot(config_file):
#    # open config file
#    with open(config_file) as f:
#        my_config = yaml.load(f)
#
#    my_vikingbot = vikingbot_12DOF(my_config)
#    my_vikingbot.move_all_legs(raise_value=0, rotate_value=100)
#    time.sleep(1)
#    my_vikingbot.move_all_legs(raise_value=100, rotate_value=100)
#    time.sleep(1)
#    my_vikingbot.move_all_legs(raise_value=0, rotate_value=100)
#
#    return my_vikingbot


def command_processor(data, my_vikingbot):
    print 'Data: {}'.format(data)

    items = data.split()
    print '\nThese are the arguments passed in: ' #debug
    print items #debug
    print '\n' #debug

    if len(items) == 1:
        command = items[0]
        iteration = 1

    elif len(items) == 2:
        command = items[0]
        iteration = float(items[1])

    else:
        return 'ERROR: invalid command format'

    print 'Command: {}'.format(command)
    print 'Iteration: {}'.format(iteration)

    commands = [
        'turn_left' #modify
        'turn_right' #modify
        'go_forward' #new
        'go_back' #new
    ]

    if command == 'turn_left':
        vikingbotMotors.set_motorSpeed(55,100)
        vikingbotMotors.set_SleepTime(iteration)
        vikingbotMotors.turnLeft()
        print 'turning left...'

        return 'Turning Left for {} seconds'.format(iteration)

    elif command == 'turn_right':
        vikingbotMotors.set_motorSpeed(55,100)
        vikingbotMotors.set_SleepTime(iteration)
        vikingbotMotors.turnRight()
        print 'turning right...'

        return 'Turning Right for {} seconds'.format(iteration)

    elif command == 'go_forward':
        vikingbotMotors.set_motorSpeed(55,100)
        vikingbotMotors.set_SleepTime(iteration)
        vikingbotMotors.goForward()
        print 'going forward...'

        return 'Going forward for {} seconds'.format(iteration)

    elif command == 'go_back':
        vikingbotMotors.set_motorSpeed(55,100)
        vikingbotMotors.set_SleepTime(iteration)
        vikingbotMotors.goBack()
        print 'going back...'

        return 'Going back for {} seconds'.format(iteration)

    elif command == 'commands':
        temp = 'Implemented Commands: '
        for command in commands:
            temp += command + ', '

        return temp

    else:
        print 'ERROR: command not recognized: {}'.format(command)
        return 'Command not found!'

#def listenToClient(client, address, my_vikingbot):
def listenToClient(client, address):
    size=1024
    while True:
        try:
            data = client.recv(size).decode()
            if data:
                # Read command from client
                print "from connected user: " + str(data)
                response = command_processor(data, my_vikingbot)

                # data = str(data).upper()
                client.send(response.encode())
            else:
                raise error('Client disconnected')
        except:
            client.close()
            return False

def Main(host, port, config_file):
#    my_vikingbot = initialize_vikingbot(config_file)

    mySocket = socket.socket()
    mySocket.bind((host,port))

    mySocket.listen(5)
    while True:
        client, address = mySocket.accept()
        client.settimeout(300)
        print ("Connection from: " + str(address)
#        listenToClient(client, address, my_vikingbot)
        listenToClient(client, address)

if __name__ == '__main__':
    args = get_args()

    print 'Host: {}'.format(args.host)
    print 'Port: {}'.format(args.port)
#    print 'Config File: {}'.format(args.config_file)

#    Main(args.host, args.port, args.config_file)
    Main(args.host, args.port)
