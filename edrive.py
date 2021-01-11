import platform
import os

# Constants for the operation mode of the message
CTRL_CREATE = 0
CTRL_DELETE = 1
CTRL_SYNC = 2
CTRL_FINISH = 3

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

# Buffer size of each message
BUFFER_SIZE = 1024
# Maximum of connections allowed by the server
MAX_CONNECTIONS = 2

# Operative system name
SYSTEM = platform.system()
THIS_DIR = os.path.dirname(os.path.abspath(__file__))