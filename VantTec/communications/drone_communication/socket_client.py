'''
Test module for connection with sockets
'''
import socket

def send_data():
    '''Main function to test connection'''
    host = '127.0.0.1'
    port = 5000

    my_socket = socket.socket()
    my_socket.connect((host, port))

    # message = input('-> ')
    # while message != 'q':
    #     my_socket.send(message.encode())
    #     data = my_socket.recv(1024).decode()
    #     print('Received from server: ' + data)
    #     message = input('-> ')

    messages = ['DockNumkthanksbye3421',
                'DockNumkthanksbye21',
                'DockNumkthanksbye1',
                'DockNumkthanksbye3',
                'DockNumkthanksbye2',
                'Mapkthanksbye89205,205020.59303,4930',
                'Mapkthanksbye85.935,50.593,4930,ghtiw',
                'DockPhoto,500,480,10kthanksbye57khgs23iurih']

    for message in messages:
        my_socket.send(message.encode())
        data = my_socket.recv(1024).decode()
        print('Received from server: ' + data)

    my_socket.close()
