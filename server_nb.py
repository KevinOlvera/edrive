import socket
import sys
import pickle
import threading
import logging

from colorama import init, Fore, Style

import math

BUFFER_SIZE = 1024
MAX_CONNECTIONS = 2


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
    def __init__(self, host: str = 'localhost', port: int = 5511):
        # Define an array to save the active clients connected to the server_address
        self.clients = []
        self.server_address = (host, port)

        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to the port
        self.sock.bind(self.server_address)
        # Listen for incoming connections
        self.sock.listen(MAX_CONNECTIONS)
        # Set as non blocking socket mode
        self.sock.setblocking(False)

        # Define threads for accepting and processing connections in the server
        accept_thread = threading.Thread(target=self.accept_connections)
        process_thread = threading.Thread(target=self.process_connections)
        # Attach the threads to the main process
        accept_thread.daemon = True
        process_thread.daemon = True
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
        while True:
            # Condition to start receiving messages if there are one or more clients connected to the server
            if len(self.clients) > 0:
                for client in self.clients:
                    try:
                        # Receive a message from each client
                        data = client.recv(BUFFER_SIZE)
                        # Load data from bytes to Python object
                        loaded_data = pickle.loads(data)

                        logging.info(f'Client {client.getpeername()} is sending {loaded_data.file_size} bytes - {loaded_data.file_name}')

                        amount_packages = math.ceil(loaded_data.file_size/BUFFER_SIZE)

                        if loaded_data.operation == 2:
                            file = open(f'{client.getpeername()}_{loaded_data.file_name}', 'wb')
                            count = 1
                            amount_received = 0
                            amount_expected = loaded_data.file_size

                            while True:
                                data = client.recv(BUFFER_SIZE)
                                amount_received += len(data)
                                
                                logging.info(f'Receiving {len(data)} bytes from {client.getpeername()} | {count}/{amount_packages} | {amount_received}/{amount_expected}')

                                file.write(data)
                                count += 1

                                if data:
                                    client.sendall(data)
                                else:
                                    logging.info(f'Client {client.getpeername()} successfully sent {loaded_data.file_size} bytes - {loaded_data.file_name}')
                                    file.close()
                                    break

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

    logging.basicConfig(format="%(asctime)s: %(message)s", level=logging.INFO, datefmt="%H:%M:%S")

    s = Server()