#!/usr/bin/env python3
"""
This script allows managing input devices on a Linux system using xinput through command-line arguments.
It supports listing devices, disabling specific devices or all devices at once, and enabling specific devices.

Features:
- List all input devices.
- Disable one or more specific devices by ID.
- Disable all devices.
- Enable one or more specific devices by ID.

Usage examples:
- List all devices: python script_name.py --list
  Example: `python script_name.py --list`
- Disable a specific device or devices by ID: python script_name.py --disable ID[,ID2,ID3,...]
  Example: `python script_name.py --disable 13` or `python script_name.py --disable 13,14`
- Disable all devices: python script_name.py --disable-all
  Example: `python script_name.py --disable-all`
- Enable a specific device or devices by ID: python script_name.py --enable ID[,ID2,ID3,...]
  Example: `python script_name.py --enable 13` or `python script_name.py --enable 13,14`

Each argument's function:
- -l, --list: Lists all input devices.
- -d, --disable: Disables specific device(s) by ID. Multiple IDs can be separated by commas.
- -da, --disable-all: Disables all devices.
- -e, --enable: Enables specific device(s) by ID. Similar to disable, multiple IDs can be separated by commas.
- -h, --help: Shows the help message and exits.

Note: Use caution when disabling devices, especially when disabling all devices, as it might leave you unable to interact with your system normally.
"""

import argparse
import subprocess

def run_command(command):
    """Executes a given shell command and returns its output and error, if any."""
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    return output.decode('utf-8'), error.decode('utf-8')

def list_devices():
    """Lists all input devices by running the `xinput list` command."""
    output, _ = run_command("xinput list")
    print(output)

def disable_device(device_ids):
    """Disables one or more devices specified by a comma-separated list of IDs."""
    for device_id in device_ids.split(','):
        _, error = run_command(f"xinput disable {device_id.strip()}")
        if error:
            print(f"Error disabling device ID {device_id}: {error}")
        else:
            print(f"Device ID {device_id} has been disabled.")

def enable_device(device_ids):
    """Enables one or more devices specified by a comma-separated list of IDs."""
    for device_id in device_ids.split(','):
        _, error = run_command(f"xinput enable {device_id.strip()}")
        if error:
            print(f"Error enabling device ID {device_id}: {error}")
        else:
            print(f"Device ID {device_id} has been enabled.")

def disable_all_devices():
    """Disables all devices by parsing the `xinput list` output and disabling each found device."""
    output, _ = run_command("xinput list")
    for line in output.split('\n'):
        if 'id=' in line:
            device_id = line.split('id=')[1].split()[0]
            disable_device(device_id)

def main():
    """Parses command-line arguments and invokes corresponding functions based on the arguments."""
    parser = argparse.ArgumentParser(description="Manage input devices using xinput.")
    parser.add_argument("-l", "--list", help="List all input devices", action="store_true")
    parser.add_argument("-d", "--disable", help="Disable specific devices by ID(s), separated by commas", type=str)
    parser.add_argument("-da", "--disable-all", help="Disable all devices", action="store_true")
    parser.add_argument("-e", "--enable", help="Enable specific devices by ID(s), separated by commas", type=str)

    args = parser.parse_args()

    if args.list:
        list_devices()
    elif args.disable:
        disable_device(args.disable)
    elif args.disable_all:
        disable_all_devices()
    elif args.enable:
        enable_device(args.enable)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
