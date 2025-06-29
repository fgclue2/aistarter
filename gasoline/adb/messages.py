from ctypes import c_uint32
from gasoline.adb import SystemIdentityString
from gasoline.adb import (
    PROTOCOL_VERSION,
    MAX_ADB_DATA,
    A_CNXN,
    A_OPEN,
    A_OKAY,
    A_WRTE,
    A_CLSE,
    A_SYNC,
)


class Message:
    def __init__(
        self,
        command: c_uint32,
        arg0: c_uint32 = c_uint32(0),
        arg1: c_uint32 = c_uint32(0),
        payload: str = "",
    ):
        self.command: c_uint32 = command
        self.arg0: c_uint32 = arg0
        self.arg1: c_uint32 = arg1
        self.payload = payload
        self.data_length: c_uint32 = c_uint32(len(payload))
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
        self.payload = str(systemIdentityString)

        # If a CONNECT message is received with an unknown version or insufficiently
        # large maxdata value, the connection with the other side must be closed.

        self.systemIdentityString = systemIdentityString
        self.version = PROTOCOL_VERSION
        self.maxdata = MAX_ADB_DATA


class Open(Message):
    def __init__(self, localId: c_uint32, destination: str):
        if localId == 0:
            raise ValueError("localId must not be 0.")

        self.command = A_OPEN
        self.arg0 = localId

        self.payload = destination

        self.localId = localId
        self.destination = destination


class Ready(Message):
    def __init__(self, localId: c_uint32, remoteId: c_uint32):
        if localId == 0:
            raise ValueError("localId must not be 0.")
        if remoteId == 0:
            raise ValueError("remoteId must not be 0.")

        self.command = A_OKAY
        self.arg0 = localId
        self.arg1 = remoteId


class Write(Message):
    def __init__(self, remoteId: c_uint32, data: str):
        self.command = A_WRTE
        self.arg1 = remoteId
        self.payload = data


class Close(Message):
    def __init__(self, localId: c_uint32, remoteId: c_uint32):
        if remoteId == 0:
            raise ValueError("remoteId must not be 0.")

        self.command = A_CLSE
        self.arg0 = localId
        self.arg1 = remoteId


class Sync(Message):
    def __init__(self, online: c_uint32, sequence: c_uint32):
        self.command = A_SYNC
        self.arg0 = online
        self.arg1 = sequence
