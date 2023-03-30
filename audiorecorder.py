import sys
import os
import sounddevice as sd
import soundfile as sf
from queue import Queue

def get_available_devices():
    print(f"\nAvailable devices:")
    print(sd.query_devices())

def main():
    get_available_devices()

if __name__ == "__main__":
    main()