from subprocess import check_output
from gasoline import adb
from os import PathLike

def isRunning(name: str, adb: PathLike[str]) -> bool | str:
    #TODO: REPLACE WITH ADB CONNECTION
    """
    Returns False if there is no device running or an str with the name of the device.
    """
    result = check_output('%s devices' % adb, shell=True)

    lines = result.decode("utf-8").split('\n')[1:]

    for line in lines:
        deviceName = line.split('\t')[0]
        if deviceName == '': continue

        adbName = check_output('%s -s %s emu avd name' % (adb, deviceName), shell=True).decode('utf-8').split('\r')[0]
        if adbName == name.removeprefix("@"): return deviceName
    
    return False