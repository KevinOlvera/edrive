import socket
import sys
import pickle
import threading
import time
import logging

from tqdm import tqdm
import math

from colorama import init, Fore, Style

from edrive import *


def load_file_bytes(file_path):
    try:
        with open(file_path, 'rb') as file:
            file_bytes = file.read()
            return file_bytes
    except IOError as msg:
        print(Fore.RED + str(msg))
        return None


class Client():
    def __init__(self, host: str, port: int):
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
            #option = input('1-Send file, 2-Delete file, 3-Exit ->')
            #if option == '1':
            #file_name = input('Enter the file name ->')
            input()
            file_name = 'to_send_2.txt'
            file_path = THIS_DIR + (f'\home\{file_name}' if SYSTEM == 'Windows' else f'/home/{file_name}')
            file_bytes = load_file_bytes(file_path)
            file_size = len(file_bytes)

            print(f'Sending {file_name} file : {file_size} bytes')

            BUFFER_SIZE = 10
            
            bytes_sent = 0
            remaining_bytes = file_size
            min = 0
            max = BUFFER_SIZE

            while bytes_sent < file_size:
                remaining_bytes = file_size - bytes_sent
                size = BUFFER_SIZE if remaining_bytes > BUFFER_SIZE else remaining_bytes
                
                #print(f'bytes sent={bytes_sent}, remaining bytes={remaining_bytes}, total bytes={file_size} : min={min} : max={max + size - 1000}')
                
                bytes_to_send = file_bytes[min:max]
                bytes_sent += len(bytes_to_send)
                min += BUFFER_SIZE
                max += size
                self.send_msg(bytes_to_send)
                time.sleep(1)

    def recv_message(self,):
        #data_recv = b''
        while True:
            try:
                data = self.sock.recv(1024 + 18)
                if data:
                    #logging.INFO('recibo')
                    #data_recv = data_recv + pickle.loads(data)
                    print(pickle.loads(data))
                #else:
                    #logging.INFO('no recibo')
            except:
                pass
                #print(Fore.RED + str(Exception))

    def send_msg(self, msg):
        self.sock.sendall(pickle.dumps(msg))


if __name__ == "__main__":
    # Initialize the colorama instance
    init(autoreset=True)
    logging.basicConfig(format="[%(asctime)s] %(message)s", level=logging.INFO, datefmt='%m/%d/%Y %H:%M:%S')
    
    c = Client('192.168.0.120', 5511)