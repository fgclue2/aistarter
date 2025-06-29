from os import PathLike, system
from pathlib import Path
from subprocess import call
from re import match
from atexit import register as onexit
from flask import Flask
from gasoline.emulator import isRunning

class CleanupOptions():
    def __init__(self, killEmulator: bool, killServer: bool):
        self.killEmulator = killEmulator
        self.killServer = killServer

#TODO: TEST USB SUPPORT
# TODO: replace rall calls to adb with the adb protocol

cleanup = CleanupOptions(True, True)

app = Flask(__name__)

adb: PathLike[str] | None = None
emulator: PathLike[str] | None = None
corsRule: str = '*'

emulatorName: str | None = None

# this makes no fucking sense but it works: https://github.com/mit-cml/appinventor-sources/blob/master/appinventor/misc/emulator-support/config.py
VERSION = "26.255.0"

@app.after_request
def add_headers(response):
    response.headers["Access-Control-Allow-Origin"] = (
        corsRule
    )
    response.headers["Access-Control-Allow-Headers"] = "origin, content-type"
    response.headers["Content-Type"] = "application/json"

    return response


@app.route("/ping/")
def ping():
    return {"status": "OK", "version": VERSION}


@app.route("/echeck/")
def etest():
    device = isRunning(True, emulatorName, adb)
    if device:
        return {"status": "OK", "device": device, "version": VERSION}
    else:
        return {"status": "NO", "version": VERSION}

@app.route("/ucheck/")
@app.route("/utest/")
def utest():
    device = isRunning(False, emulatorName, adb)
    if device:
        return {"status": "OK", "device": device, "version": VERSION}
    else:
        return {"status": "NO", "version": VERSION}

@app.route("/start/")
def run():
    call([emulator, emulatorName])


@app.route("/replstart/<string:device>")
def companionstart(device: str):
    if match("emulator.*", device):  # Only fake the menu key for the emulator
        call(f'{adb} -s {device} shell input keyevent 82', shell=True)
    call(
        f'{adb} -s {device} shell am start -a android.intent.action.VIEW -n edu.mit.appinventor.aicompanion3/.Screen1 --ez rundirect true',
        shell=True,
    )
    return ""


@app.route('/emulatorreset/')
def emulatorreset():
    call(f"{adb} emu restart", shell=True)
    return ''


def shutdown():
    print("==> BYE BYE! <==")
    if cleanup.killEmulator: call(f"{adb} emu kill", shell=True)
    if cleanup.killServer: call(f"{adb} kill-server", shell=True)
    exit(0)

@app.route('/reset/')
def reset():
    call(f"{adb} emu kill", shell=True)
    return {
        "status": "OK",
        "version": VERSION
    }

def start(adb_: PathLike[str], emulator_: PathLike[str], name: str, cors: str, cleanupOptions: CleanupOptions):
    global adb
    global emulator
    global emulatorName
    global corsRule
    global cleanup

    adb = Path(adb_)
    emulator = Path(emulator_)
    emulatorName = name
    corsRule = cors
    cleanup = cleanupOptions

    call(f"{adb} start-server", shell=True)

    onexit(shutdown)

    app.run(port=8004)
