from subprocess import check_output
from gasoline.adb import AdbClient, AdbError
from os import PathLike


def isRunning(isEmulator: bool, name: str, adb: PathLike[str]) -> bool | str:
    """
    Returns False if there is no device running or an str with the name of the device.
    """

    client = AdbClient("127.0.0.1", 5037)

    client.send_command("host:devices")

    code = client.connection.recv(4).decode()
    if code != "OKAY":
        raise AdbError("Code isn't OKAY")

    data = [
        x
        for x in client.connection.recv(int(client.connection.recv(4).decode(), 16))
        .decode()
        .split("\n")
        if x
    ]
    print("Data:", data)
    return False