from enum import Enum
from ctypes import c_uint32

MAX_ADB_DATA = 4096
PROTOCOL_VERSION = 0x01000000

AUTH_TOKEN = 1
AUTH_SIGNATURE = 2
AUTH_RSAPUBLICKEY = 3

A_SYNC = c_uint32(0x434E5953)
A_CNXN = c_uint32(0x4E584E43)
A_OPEN = c_uint32(0x4E45504F)
A_OKAY = c_uint32(0x59414B4F)
A_CLSE = c_uint32(0x45534C43)
A_WRTE = c_uint32(0x45545257)


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