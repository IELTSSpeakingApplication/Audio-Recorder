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

def main():
    try:
        get_available_devices()
        device_number = get_input_device()
        print(device_number)
    except Exception as e:
        sys.exit(f"\nOpss, Something went wrong:", str(e))

if __name__ == "__main__":
    main()