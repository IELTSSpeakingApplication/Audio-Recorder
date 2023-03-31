import sys
import os
import sounddevice as sd
import soundfile as sf
from queue import Queue

SAMPLE_RATE = 24000
OUTPUT_FOLDER = os.path.join("sound")

q = Queue()

def get_available_devices():
    print(f"\n")
    print(f"*" * 60)
    print(f"Available devices:")
    print(sd.query_devices())

def get_input_device():
    print(f"\n")
    print(f"*" * 60)
    print(f"Input device:")
    print(f"\n* Choose input device (1/2 in, 0 out)")
    print(f"* Default microphone (>)")

    try:
        num_device = int(input(f"\nDevice number: "))
    except ValueError:
        sys.exit(f"\nInput device must be integer (1/2/3/..)\n")
    
    return num_device

def get_device_info(num_device):
    device_info = sd.query_devices()

    if num_device < len(device_info):
        print(f"\nDevice information:")

        device =  device_info[int(num_device)]
        device_name = device["name"]
        device_channels = device["max_input_channels"]
        default_samplerate = device["default_samplerate"]

        print(f"Device name:", device_name)
        print(f"Device input channels:", device_channels, f"(Mono)" if device_channels==1 else f"(Stereo)")
        print(f"Device Sample Rate:", default_samplerate)

        return device
    else:
        sys.exit(f"\nDevice is index out of range\n")

def get_filename():
    print(f"\n")
    print(f"*" * 60)
    print(f"Filename:")

    print(f"\n* Filename format is name-date (hafid-100423)")
    print(f"* File will be save in sound folder")

    filename = input(f"\nFile name: ")

    return filename

def get_ready(device, filename):
    filename = filename+".wav"

    print(f"\n")
    print(f"*" * 60)
    print(f"Overview:")
    print(f"\nDevice name is", device["name"])
    print(f"Device channels is", device["max_input_channels"])
    print(f"Sample Rate is", str(SAMPLE_RATE))
    print(f"File Name is", filename)
    print(f"File Path is", os.path.join(OUTPUT_FOLDER, filename))

    print(f"\n=======================")
    print(f"Get ready for recording")
    print(f"=======================\n")

    confirmation = input(f"Type (Y/y) if you ready: ")

    if confirmation=="y" or confirmation=="Y":
        recording(device, filename)
    else:
        sys.exit(f"\nOpps, recording process aborted\n")

def callback(indata, frames, time, status):
    if status:
        print(f"\nRecording...\n", flush=True)
    q.put(indata.copy())

def recording(device, filename):
    try:
        with sf.SoundFile(os.path.join(OUTPUT_FOLDER, filename), mode="x", samplerate=SAMPLE_RATE,
                          channels=device["max_input_channels"], subtype="PCM_16") as file:
            with sd.InputStream(samplerate=SAMPLE_RATE, device=device["name"],
                                channels=device["max_input_channels"], callback=callback):
                print(f"\n")
                print(f"*" * 60)
                print(f"\nGet ready for recording...")
                print(f"Control + C for stop recording\n")
                print(f"*" * 60)
                while True:
                    file.write(q.get())
    except KeyboardInterrupt:
        print(f"\nYes, Recording finished!")
        print(f"Audio file saved in", os.path.join(OUTPUT_FOLDER, filename))
        sys.exit(f"\nThank you for using this app\n")
    except Exception as e:
        sys.exit(f"\nOpss, Something went wrong:", str(e), f"\n")

def main():
    try:
        print(f"\n")
        print(f"*" * 22, f"Audio Recorder", f"*" * 22)
        get_available_devices()
        device_number = get_input_device()
        device = get_device_info(device_number)
        filename = get_filename()
        get_ready(device, filename)
    except Exception as e:
        sys.exit(f"\nOpss, Something went wrong:", str(e), f"\n")

if __name__ == "__main__":
    main()