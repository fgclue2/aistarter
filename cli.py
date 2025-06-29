#!/bin/python

from argparse import ArgumentParser
from os import environ
from os.path import join, exists
from pathlib import Path
from gasoline import start

def abort(message: str):
    print(message)
    exit(1)

parser = ArgumentParser(
    prog='openaistarter-cli',
    description='Open App Inventor CLI',
    epilog='by Clue <lost@biitle.nl>'
)

parser.add_argument('emulator', help='Emulator name (usually @Emulator_Name)')
parser.add_argument('-a', '--android', default=environ.get('ANDROID_HOME'), help='Android Home (usually $ANDROID_HOME)')
parser.add_argument('-c', '--cors', default="https://ai2.appinventor.mit.edu", help='CORS Rule (usually https://ai2.appinventor.mit.edu)')

args = parser.parse_args()

EMULATOR = join(args.android, "emulator/emulator")
ADB = join(args.android, "platform-tools/adb")

print("⛽️🚜 Open App Inventor Starter\n")

print("Found emulator:", EMULATOR)
print("Found ADB:", ADB)

print()

if exists(EMULATOR) == False: abort("I couldn't find the emulator (is it installed?)")
if exists(ADB) == False: abort("I couldn't find ADB (is it installed?)")

print("Emulator name:", args.emulator)
print()

print("App Inventor should be waiting on port 8004.")
print("All is okay, so I'll start the webserver now:")

start(Path(ADB), Path(EMULATOR), args.emulator, args.cors)