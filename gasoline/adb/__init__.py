from enum import Enum
from socket import create_connection

class AdbError(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class SystemType(Enum):
    Bootloader = "bootloader"
    Device = "device"
    Host = "host"

class SystemIdentityString:
    def __init__(self, systemType: SystemType, serialNumber: str, banner: str):
        self.systemType = systemType
        self.serialNumber = serialNumber
        self.banner = banner

    def __str__(self):
        return f"{self.systemType}:{self.serialNumber}:{self.banner}"

class AdbClient():
    def __init__(self, host: str, port: int):
        self.connection = create_connection((host, port))

    def send_command(self, command: str):
        self.connection.send(f"{len(command):04x}".encode() + command.encode())