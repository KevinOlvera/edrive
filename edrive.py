import os
import platform
import socket
import sys
import pickle
import threading

from tqdm import tqdm
import math

from colorama import init, Fore, Style

BUFFER_SIZE = 1024


class Message():
    def __init__(self, operation, file_name, file_size, file_bytes):
        self.operation: int = operation
        self.file_name: str = file_name
        self.file_size: int = file_size
        self.file_bytes: bytes = file_bytes

    def __str__(self):
        return f'{self.operation}_{self.file_name}'

    def __repr__(self):
        # return f'Message(\'{self.operation}\', \'{self.file_name}\', {self.file_size}, {type(self.file_bytes)})'
        return f'Message(\'{self.operation}\', \'{self.file_name}\', {self.file_size}, {self.file_bytes})'


CTRL_CREATE = 0
CTRL_DELETE = 1
CTRL_SYNC = 2

SYSTEM = platform.system()
THIS_DIR = os.path.dirname(os.path.abspath(__file__))


def load_file_bytes(file_path):
    try:
        with open(file_path, 'rb') as file:
            file_bytes = file.read()
            return file_bytes
    except IOError as msg:
        print(Fore.RED + str(msg))
        return None


class Client():
    def __init__(self, host: str = 'localhost', port: int = 5511):
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect to the server
        self.sock.connect((host, port))

        # Create a new thread to receive the messages
        recv_message = threading.Thread(target=self.recv_message)
        # Attach the thread to the main process
        recv_message.daemon = True
        # Start the thread
        recv_message.start()

        # Loop to send the messages to the server
        while True:
            option = input('1-Send file, 2-Delete file, 3-Exit ->')
            if option == '1':
                file_name = input('Enter the file name ->')
                file_path = THIS_DIR + (f'\\{file_name}' if SYSTEM == 'Windows' else f'/{file_name}')
                file_bytes = load_file_bytes(file_path)
                if file_bytes:
                    connection_message = Message(CTRL_SYNC, file_name, len(file_bytes), b'')
                    self.send_msg(connection_message)

                    print(f'Sending {len(file_bytes)} bytes - {file_name}')
                    self.sock.sendall(file_bytes)

                    # Look for the response
                    amount_received = 0
                    amount_expected = len(file_bytes)

                    count = 1

                    amount_packages = math.ceil(len(file_bytes)/BUFFER_SIZE)

                    # Read the amount of data received from the server
                    while amount_received < amount_expected:
                        data = self.sock.recv(BUFFER_SIZE)
                        amount_received += len(data)
                        count += 1
                        print(f'Receiving {len(data)} bytes from {self.sock.getpeername()} | {count}/{amount_packages} | {amount_received}/{amount_expected}')

                    print('All the bytes was sent to the server')

                else:
                    print(Fore.RED + 'Error: Please enter an existing file name')
            elif option == '2':
                pass
            elif option == '3':
                self.sock.close()
                sys.exit()
            else:
                print(Fore.RED + 'Error: Please enter a valid option')

    def recv_message(self,):
        #data_recv = b''
        while True:
            try:
                data = self.sock.recv(BUFFER_SIZE)
                if data:
                    print(pickle.loads(data))
                    #data_recv += data
                #else:
                #    pass
                    #print(pickle.loads(data_recv))
                    #data_recv = b''
            except:
                pass
                #print(Fore.RED + str(Exception))

    def send_msg(self, msg: Message):
        self.sock.sendall(pickle.dumps(msg))


if __name__ == "__main__":
    # Initialize the colorama instance
    init(autoreset=True)

    # Set the file name to be sended
    #file_name = 'to_send.txt'

    # Read the image to be sended
    #file_path = THIS_DIR + (f'\\{file_name}' if SYSTEM == 'Windows' else f'/{file_name}')
    #file_bytes = load_file_bytes(file_path)

    #new_message = Message(CTRL_CREATE, file_name, len(file_bytes), file_bytes)

    c = Client()
