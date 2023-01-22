#!/user/bin/env python3
# FlagDumper.py
## Checks for low-hanging fruit for network forensics challenges in CTF's!
## Automatically searches for the ascii and hex representation of "flag"
## Additionally searches for ascii and hex representation of strings given by user

import os
import binascii

# variable declaration
file_or_dir = ""
special = ""
special_exists = ""
checks = ["flag"]  ## keywords to search for

## initial prompts
while (special_exists != "y") and (special_exists != "n"):
    special_exists = input(
        "Would you like to enter a flag precursor other than \"flag\" (ex: THM{, HTB{, etc.)? (y/n):")

if (special_exists == "y"):
    special = input("Please enter flag precursor:")
    checks.append(special)

while (file_or_dir != "single") and (file_or_dir != "directory"):
    file_or_dir = input("Analyzing a single capture, or directory of captures? (single/directory):")


def analyze_capture(location):
    for x in checks:
        x_enc = binascii.hexlify(x.encode()).decode("utf-8")
        cmd = 'tshark -r ' + location + ' -Y "frame contains \\"' + x + '\\"" -T fields -e data | xxd -r -p'  # Check for ascii representation
        cmd_enc = 'tshark -r ' + location + ' -Y "frame contains \\"' + x_enc + '\\"" -T fields -e data | xxd -r -p | xxd -r -p'  # Check for Hex representation
        os.system(cmd)
        os.system(cmd_enc)


if (file_or_dir == "single"):
    location = input("Please Enter Capture Location:\n")
    analyze_capture(location)
else:
    location = input("Please Enter Directory:\n")
    for filename in os.listdir(location):
        print(filename + ": ")
        analyze_capture((location + filename))
        print("\n")