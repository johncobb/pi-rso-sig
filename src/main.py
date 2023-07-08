import pyaudio
import wave

FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "dtmf.wav"


def open_device():
    return pyaudio.PyAudio()

def open_file(file_name):
    return wave.open(file_name)

def play_file(file_name, device_index):
    audio_src = open_device()
    audio_file = open_file(file_name)

    audio_framerate = audio_file.getframerate()
    audio_channels = audio_file.getnchannels()
    audio_format = audio_src.get_format_from_width(audio_file.getsampwidth())

    stream_out = audio_src.open(rate=audio_framerate, channels=audio_channels,
                                format=audio_format, output=True, output_device_index=device_index, frames_per_buffer=1024)

    audio_out = audio_file.readframes(5 * audio_framerate)
    stream_out.write(audio_out)


def main():
    play_file("dtmf.wav", 6)

if __name__ == "__main__":
    main()
    # play_file("dtmf.wav", 6)
    # enum_devices() # open_device()
    # main()
    # print("running soundcard file.")
