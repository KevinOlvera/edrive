import socket
import sys
import os

from colorama import init, Fore, Style
from tqdm import tqdm

import math

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


if __name__ == "__main__":
    # Initialize the colorama instance
    init(autoreset=True)

    # Read the image to be sended
    file_path = THIS_DIR + '\\to_send.jpeg'
    file = open(file_path, 'rb')

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('localhost', 10000)
    print(Fore.GREEN + 'Connecting to {} port {}'.format(*server_address))
    try:
        sock.connect(server_address)
    except Exception as msg:
        print(Fore.RED + str(msg))
        sys.exit()

    try:
        # Send data
        message = file.read()
        print('Sending {}'.format(file_path))
        sock.sendall(message)

        # Look for the response
        amount_received = 0
        amount_expected = len(message)

        count = 0

        progress_bar = tqdm(total=math.ceil(len(message)/1412))

        # Read the amount of data received from the server
        while amount_received < amount_expected:
            data = sock.recv(1412)
            count += 1
            amount_received += len(data)
            progress_bar.update(1)

        progress_bar.close()
        print('All done.')

    finally:
        file.close()
        print('Closing socket')
        sock.close()
