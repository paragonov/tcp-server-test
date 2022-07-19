import telnetlib
import csv
import time
import openpyxl
from pathlib import Path

HOST = '127.0.0.1'
PORT = 8888


def processing_file(fn):
    input_format = Path(fn).suffix
    if input_format == '' or input_format == '.txt':
        with open(fn, 'r') as data:
            data_file = data.read().strip().split('\n')
        return data_file
    elif input_format == '.csv':
        with open(fn, 'r', newline='') as data:
            data_file = csv.reader(data)
            list_data = []
            for i in list(data_file)[1:]:
                list_data.append(' '.join(i))
        return list_data
    elif input_format == '.xls' or input_format == '.xlsx':
        wb = openpyxl.open(fn, read_only=True)
        sheet = wb.active
        list_data = []
        for row in range(2, sheet.max_row+1):
            list_data.append(
                sheet[row][0].value + ' ' + sheet[row][1].value + ' ' + sheet[row][2].value + ' ' + sheet[row][3].value)
        return list_data
    else:
        print(f'ERROR... Please try again.')


def start_tnclient(fn):
    data_file = processing_file(fn)
    tn = telnetlib.Telnet(HOST, PORT, timeout=1)
    print('Connecting server...' + '\n')
    for data in data_file:
        tn.write(data.encode() + b'\n')
        time.sleep(0.1)
    print(tn.read_very_eager().decode())
    tn.close()
    print('Finished...' + '\n' + 'Goodbye!')


def main():
    while True:
        try:
            file_name = input('Enter path you file: ').strip()
            start_tnclient(file_name)
        except ConnectionRefusedError:
            print('Connection error... Please try again or press CTRL+C for exit.')
        except FileNotFoundError:
            print('File not found... Please try again or press CTRL+C for exit.')
        except KeyboardInterrupt:
            print('\n'+'Goodbye!')
            break
        else:
            break


if __name__ == '__main__':
    main()
