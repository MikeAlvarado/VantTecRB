'''
Module to receive data from drone
'''
import socket
import json

HOST = "127.0.0.1"
PORT = 5000
END = 'kthanksbye'

def receive(global_data):
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.bind((HOST, PORT))
    my_socket.listen(1)
    conn, addr = my_socket.accept()
    print("Connection from: " + str(addr))
    header = b''
    fhand = open("file.jpg", "wb+")
    img_data = b''

    while True:
        data = conn.recv(1024)
        if not data:
            raise RuntimeError("No header/data")
        header += data
        # end-of-header in buffer yet_
        eoh = header.find(b'kthanksbye')

        if eoh == -1:
            continue
        # split the header and keep data
        header, data = header[:eoh], header[eoh + len(END):]
        header = header.decode()

        # Dock number
        if header == "DockNum":
            data = data.decode()
            global_data.dock_num = data
        # Map
        elif header == "Map":
            data = data.decode()
            global_data.map_data = json.loads(data)
        # Dock photo
        else:
            # Analyse header
            # "DockPhoto,500,424,12"
            try:
                start, length, offset, size = header.split(',')
            except ValueError:
                print("Unknown header", header)
                continue
            if start == "DockPhoto":
                length, offset, size = map(int, [length, offset, size])

                if offset + size == length:
                    fhand.write(img_data)
                    img_data = b''
                else:
                    img_data += data
        header = b''
    conn.close()
