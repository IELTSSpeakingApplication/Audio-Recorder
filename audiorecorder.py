import sys
import os
import sounddevice as sd
import soundfile as sf
from queue import Queue

def get_available_devices():
    print(f"\nAvailable devices:")
    print(sd.query_devices())

def get_input_device():
    print(f"\n* Choose input device (1/2 in, 0 out)")
    print(f"* Default microphone (>)")

    try:
        device = int(input(f"\nDevice number: "))
    except ValueError:
        sys.exit("Input device must be integer (1/2/3/..)")
    
    return device

def get_device_info(device):
    device_info = sd.query_devices()

    if device < len(device_info):
        print(f"\nDevice information:")

        device =  device_info[int(device)]
        device_name = device["name"]
        device_channels = device["max_input_channels"]

        print("Device name:", device_name)
        print("Device input channels:", device_channels, "(Mono)" if device_channels==1 else "(Stereo)")

        return device
    else:
        sys.exit("Device is index out of range")

def get_filename():
    filename = input(f"\nFile name: ")

    return filename

def main():
    try:
        get_available_devices()
        device_number = get_input_device()
        get_device_info(device_number)
        filename = get_filename()
        print(filename)
    except Exception as e:
        sys.exit(f"\nOpss, Something went wrong:", str(e))

if __name__ == "__main__":
    main()