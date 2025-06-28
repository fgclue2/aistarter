from zlib import crc32
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


class Message:
    def __init__(self, command: c_uint32, arg0: c_uint32, arg1: c_uint32, payload: c_uint32 | None = None):
        self.command: c_uint32 = command
        self.arg0: c_uint32 = arg0
        self.arg1: c_uint32 = arg1
        self.data_length: c_uint32
        self.magic: c_uint32 = c_uint32(command.value ^ 0xFFFFFFFF)


class Connect(Message):
    def __init__(
        self,
        systemIdentityString: SystemIdentityString,
        version=PROTOCOL_VERSION,
        maxdata=MAX_ADB_DATA,
    ):
        self.command = A_CNXN
        self.arg0 = version
        self.arg1 = maxdata
        # self.data = str(systemIdentityString)

        self.systemIdentityString = systemIdentityString
        self.version = PROTOCOL_VERSION
        self.maxdata = MAX_ADB_DATA


class Open(Message):
    def __init__(self, localId: int, destination: str):
        if localId == 0:
            raise ValueError("localId must not be 0.")
        
        self.command = A_OPEN
        self.arg0 = localId
        # self.arg1 = destination

        self.localId = localId
        self.destination = destination

class Ready(Message):
    def __init__(self, localId: int, destination: str):
        pass
