import socket
import sys

from colorama import init, Fore, Style

if __name__ == "__main__":
    init(autoreset=True)

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = ('localhost', 10000)
    print(Fore.GREEN + 'Starting up on {} port {}'.format(*server_address))
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)

    while True:
        # Wait for a connection
        print(Fore.YELLOW + 'Waiting for a connection')
        connection, client_address = sock.accept()

        file = open('to_recv.jpeg','wb')

        try:
            print('Connection from {}'.format(client_address))
            count = 0
            # Receive the data in small chunks and retransmit it
            while True:
                data = connection.recv(1412)
                count += 1
                #print('Data received {!r}'.format(data))
                print('Receiving data {} ...'.format(count))
                file.write(data)
                if data:
                    #print('Sending data back to the client')
                    connection.sendall(data)
                else:
                    print('All done from {}'.format(client_address))
                    file.close()
                    break
        finally:
            # Clean up the connection
            connection.close()