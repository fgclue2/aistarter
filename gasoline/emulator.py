from subprocess import check_output
from gasoline import adb
from os import PathLike

def isRunning(name: str, adb: PathLike[str]) -> bool:
    result = check_output('%s devices' % adb, shell=True)

    print(result)
    return False