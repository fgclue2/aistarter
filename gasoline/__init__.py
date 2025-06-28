from os import PathLike
from pathlib import Path
from subprocess import call, check_output
from re import match
from flask import Flask
from gasoline.emulator import isRunning

# TODO: replace rall calls to adb with the adb protocol

app = Flask(__name__)

adb: PathLike[str] | None = None
emulator: PathLike[str] | None = None

emulatorName: str | None = None

# this makes no fucking sense but it works: https://github.com/mit-cml/appinventor-sources/blob/master/appinventor/misc/emulator-support/config.py
VERSION = "%d.%d.%d%s" % (26, 255, 0, "")


@app.after_request
def add_headers(response):
    response.headers["Access-Control-Allow-Origin"] = (
        "*"  # todo: set to https://ai2.appinventor.mit.edu
    )
    response.headers["Access-Control-Allow-Headers"] = "origin, content-type"
    response.headers["Content-Type"] = "application/json"

    return response


@app.route("/ping/")
def ping():
    return {"status": "OK", "version": VERSION}

@app.route('/utest/')
def utest():
    device = isRunning(emulatorName, adb)
    if device:
        return {
            "status": "OK",
            "device": device,
            "version": VERSION
        }
    else:
        return {
            "status": "NO",
            "version": VERSION
        }

def start(adb_: PathLike[str], emulator_: PathLike[str], name: str):
    global adb
    global emulator
    global emulatorName
    
    adb = Path(adb_)
    emulator = Path(emulator_)
    emulatorName = name

    app.run(port=8004)