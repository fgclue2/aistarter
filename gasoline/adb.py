from typing import Any

A_SYNC = 0x434e5953
A_CNXN = 0x4e584e43
A_OPEN = 0x4e45504f
A_OKAY = 0x59414b4f
A_CLSE = 0x45534c43
A_WRTE = 0x45545257

class Message:
    def __init__(self, command, arg0, arg1, data_length, data_crc32):
        self.magic = command ^ 0xffffffff