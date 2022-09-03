import re
import socket
import time
from select import select

HOST = '127.0.0.1'
PORT = 8882
ALL_DATA = []
list_sockets = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.setblocking(False)
server_socket.bind((HOST, PORT))
server_socket.listen(100)
server_socket.setblocking(True)


def accept_connection(server_socket):
    client_socket, address = server_socket.accept()
    print(f'Connection from {address}' + '\n', 'Processing...' + '\n')
    list_sockets.append(client_socket)


def send_message(client_socket):
    try:
        data = client_socket.recv(1024).decode()
    except UnicodeError:
        client_socket.close()
    else:
        if data:
            try:
                result_data = parser(data)
            except IndexError:
                client_socket.send('Invalid data! Please enter correct data...'.encode() + b'\n')
                pass
            else:
                if result_data[1]:
                    client_socket.send(result_data[0].encode() + b'\n')
                ALL_DATA.append(result_data[0])
        else:
            client_socket.close()
            list_sockets.remove(client_socket)


def parser(data):
    pars_data = re.findall(r'\s00\[', data)
    data_split = data.split(' ')
    result = f'Спортсмен, нагрудный номер {data_split[0]} прошёл отсечку {data_split[1]}, в {data_split[2][:8]}'
    if pars_data:
        return result, True
    else:
        return result, False


def event_loop(server_socket):
    while True:
        reader, writer, exc = select(list_sockets, [], [])
        for sock in reader:
            if sock is server_socket:
                accept_connection(sock)
            else:
                send_message(sock)


def load_log(data):
    with open('logs.txt', 'w') as logs:
        for log in data:
            logs.write(log + '\n')


def main():
    print('Hello!', 'Server starts up...' + '\n')
    list_sockets.append(server_socket)
    event_loop(server_socket)


if __name__ == '__main__':
    main()
