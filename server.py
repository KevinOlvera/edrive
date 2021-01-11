import socket
import sys
import pickle
import threading
import logging

from colorama import init, Fore, Style

import math

from edrive import *


class Message():
    def __init__(self, operation, file_name, file_size, file_bytes):
        self.operation: int = operation
        self.file_name: str = file_name
        self.file_size: int = file_size
        self.file_bytes: bytes = file_bytes
    
    def __init__(self, operation, file_name, file_size):
        self.operation: int = operation
        self.file_name: str = file_name
        self.file_size: int = file_size
        self.file_bytes: bytes = b''

    def __str__(self):
        return f'{self.operation}_{self.file_name}'

    def __repr__(self):
        # return f'Message(\'{self.operation}\', \'{self.file_name}\', {self.file_size}, {type(self.file_bytes)})'
        return f'Message(\'{self.operation}\', \'{self.file_name}\', {self.file_size}, {self.file_bytes})'


class Server():
    def __init__(self, host: str, port: int):
        # Define an array to save the active clients connected to the server_address
        self.clients = []
        self.server_address = (host, port)

        # Create a TCP/IP socket
        logging.info('Creating TCP/IP socket')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to the port
        logging.info(f'Binding the socket to the port {self.server_address[1]}')
        self.sock.bind(self.server_address)
        # Listen for incoming connections
        logging.info(f'Enabling the server to accept incoming connections. Maximum connections: {MAX_CONNECTIONS}')
        self.sock.listen(MAX_CONNECTIONS)
        # Set as non blocking socket mode
        logging.info(f'Configuring as non-blocking socket mode')
        self.sock.setblocking(False)

        # Define threads for accepting and processing connections in the server
        accept_thread = threading.Thread(target=self.accept_connections, daemon=True)
        process_thread = threading.Thread(target=self.process_connections, daemon=True)

        # Start the threads
        accept_thread.start()
        process_thread.start()

        try:
            while True:
                pass
        except KeyboardInterrupt:
            self.sock.close()
            sys.exit()


    def accept_connections(self):
        logging.info(Fore.GREEN + f'Starting up on {self.server_address[0]}:{self.server_address[1]}')
        while True:
            try:
                # Wait for a connection
                connection, client_address = self.sock.accept()
                # Set as non blocking connection mode
                connection.setblocking(False)
                logging.info(f'Connection established with' + Fore.GREEN + f' {client_address}')
                # Add the new connection to the clients array
                self.clients.append(connection)
            except:
                pass

    
    def process_connections(self):
        logging.info('Ready to process new connections')
        while True:
            # Condition to start receiving messages if there are one or more clients connected to the server
            if len(self.clients) > 0:
                for client in self.clients:
                    try:
                        # Receive a message from each client
                        config = client.recv(BUFFER_SIZE)
                        # Load data from bytes to Python object
                        config_data = pickle.loads(config)

                        operation_mode = 'CREATE' if config_data.operation == 2 else 'DELETE'

                        logging.info(f'{operation_mode}: Client {client.getpeername()}, file \'{config_data.file_name}\', {config_data.file_size} bytes')

                        #bytes_expected = config_data.file_size
                        #amount_packages = math.ceil(bytes_expected/BUFFER_SIZE)


                        #if int(config_data.operation) == 2:
                            #file = open(f'\home\{client.getpeername()}_{config_data.file_name}', 'wb')
                            #file_data = client.recv(BUFFER_SIZE)
                            #file.write(pickle.loads(file_data))
                            #file.close()
                        #file = open(THIS_DIR + f'\home\{client.getpeername()}_{config_data.file_name}', 'wb')
                        print('file opened')
                        while True:
                            print('receiving data...')
                            data = client.recv(1024)
                            print('data=%s', (data))
                            if not data:
                                break
                            #if pickle.loads(data).operation == 3:
                            #    break
                            # write data to a file
                            #file.write(data)

                        #file.close()
                        #print('Successfully get the file')
                        #    count = 1
                        #    amount_received = 0
                        #    amount_expected = loaded_data.file_size
#
                        #    while True:
                        #        data = client.recv(BUFFER_SIZE)
                        #        amount_received += len(data)
                        #        
                        #        logging.info(f'Receiving {len(data)} bytes from {client.getpeername()} | {count}/{amount_packages} | {amount_received}/#{amount_expected}')
#
                        #        file.write(data)
                        #        count += 1
#
                        #        if data:
                        #            client.sendall(data)
                        #        else:
                        #            logging.info(f'Client {client.getpeername()} successfully sent {loaded_data.file_size} bytes - {loaded_data.#file_name}')
                        #            file.close()
                        #            break
#
                            #self.send_to_all(data, client)

                    except:
                        pass

    
    def send_to_all(self, data : bytes, client):
        for c in self.clients:
            try:
                if c != client:
                    # Send a message to each client
                    c.sendall(data)
            except Exception as msg:
                logging.info(Fore.RED + str(c) + ': ' + str(msg))
                # If something wrong happens remove the client from the active list
                self.clients.remove(c)


if __name__ == "__main__":
    # Initialize the colorama instance
    init(autoreset=True)

    logging.basicConfig(format="[%(asctime)s] %(message)s", level=logging.INFO, datefmt='%m/%d/%Y %H:%M:%S')
    s = Server(socket.gethostbyname(socket.gethostname()), 5511)