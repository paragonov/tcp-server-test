import socket
import re
import time
from _socket import SHUT_RDWR

HOST = '127.0.0.1'
PORT = 8888
ALL_DATA = []


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(100)
    server_socket.settimeout(20)
    print('Hello!', 'Server starts up...' + '\n')
    client_socket, address = server_socket.accept()
    print('Processing...' + '\n')
    while True:
        try:
            data = client_socket.recv(1024).decode()
        except Exception:
            continue
        if data:
            try:
                result_data = parser(data)
            except IndexError:
                client_socket.send('Invalid data! Please enter correct data...'.encode() + b'\n')
                continue
            if result_data[1]:
                client_socket.send(result_data[0].encode())
            ALL_DATA.append(result_data[0])
        else:
            break


def parser(data):
    pars_data = re.findall(r'\s00\[', data)
    data_split = data.split(' ')
    result = f'Спортсмен, нагрудный номер {data_split[0]} прошёл отсечку {data_split[1]}, в {data_split[2][:8]}'
    if pars_data:
        return result, True
    else:
        return result, False


def load_log(data):
    with open('logs.txt', 'w') as logs:
        for log in data:
            logs.write(log + '\n')


def main():
    try:
        start_server()
    except KeyboardInterrupt:
        print('Server has finished...', 'Goodbye!')
    except TimeoutError:
        print('Server has finished...', 'Goodbye!')
    else:
        print('Logging in progress...')
        load_log(ALL_DATA)
        print('Server has finished...', 'Goodbye!')


if __name__ == '__main__':
    main()
