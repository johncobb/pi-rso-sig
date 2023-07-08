import pyaudio
import wave
import math
import numpy as np
import sys
import time

FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "dtmf.wav"


""" source credit : https://github.com/repoalpha/DTMF_encoder/blob/master/dtmf.py """

def sine_sine_wave(f1, f2, length, rate):

    s1 = sine_wave(f1, length, rate)
    s2 = sine_wave(f2, length, rate)
    ss = s1+s2
    sa = np.divide(ss, 2.0)
    return sa
""" source credit : https://github.com/repoalpha/DTMF_encoder/blob/master/dtmf.py """
def sine_wave(frequency, length, rate):

    length = int(length * rate)
    factor = float(frequency) * (math.pi * 2) / rate
    return np.sin(np.arange(length) * factor)

""" source credit : https://github.com/repoalpha/DTMF_encoder/blob/master/dtmf.py """
def play_frequency(stream, frequency=440, length=0.10, rate=44100):
    frames = []
    frames.append(sine_wave(frequency, length, rate))
    chunk = np.concatenate(frames) * 0.25
    stream.write(chunk.astype(np.float32).tobytes())

""" source credit : https://github.com/repoalpha/DTMF_encoder/blob/master/dtmf.py """
def play_dtmf_tone(stream, digits, length=0.2, rate=44100):
    dtmf_freqs = {'1': (1209,697), '2': (1336, 697), '3': (1477, 697), 'A': (1633, 697),
                  '4': (1209,770), '5': (1336, 770), '6': (1477, 770), 'B': (1633, 770),
                  '7': (1209,852), '8': (1336, 852), '9': (1477, 852), 'C': (1633, 852),
                  '*': (1209,941), '0': (1336, 941), '#': (1477, 941), 'D': (1633, 941)}
    dtmf_digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '*', '0', '#', 'A', 'B', 'C', 'D']
    if type(digits) is not type(''):
        digits=str(digits)[0]
    digits = ''.join ([dd for dd in digits if dd in dtmf_digits])
    joined_chunks = []
    for digit in digits:
        digit=digit.upper()
        frames = []
        frames.append(sine_sine_wave(dtmf_freqs[digit][0], dtmf_freqs[digit][1], length, rate))
        chunk = np.concatenate(frames) * 0.25
        joined_chunks.append(chunk)
        
        # fader section
        fade = 200 # 200ms
        fade_in = np.arange(0., 1., 1/fade)
        fade_out = np.arange(1., 0., -1/fade)

        chunk[:fade] = np.multiply(chunk[:fade], fade_in) # fade sample wave in
        chunk[-fade:] = np.multiply(chunk[-fade:], fade_out) # fade sample wave out
        time.sleep(0.1)
        
    X = np.array(joined_chunks, dtype='float32') # creates an one long array of tone samples to record
    stream.write(X.astype(np.float32).tobytes()) # to hear tones

def _open_stream(audio_src, format=pyaudio.paFloat32, rate=RATE, channels=1, output=1,output_device_index=None, frames_per_buffer=CHUNK):
    return audio_src.open(format=format, channels=1, rate=rate, output=1, output_device_index=output_device_index, frames_per_buffer=CHUNK)

def open_device():
    return pyaudio.PyAudio()

def open_file(file_name):
    return wave.open(file_name)



def play_file(file_name):

    """ open the soundcard (device). """
    audio_src = open_device()
    """ open the audio file (.wav) """
    audio_file = open_file(file_name)

    """ calculate file meta. """
    audio_framerate = audio_file.getframerate()
    audio_channels = audio_file.getnchannels()
    audio_format = audio_src.get_format_from_width(audio_file.getsampwidth())

    """ open the device (audio) stream interface. """
    stream = _open_stream(audio_src, format=audio_format, rate=audio_framerate, channels=audio_channels)

    """ read audio data into buffer. """
    audio_buffer = audio_file.readframes(5 * audio_framerate)

    """ write buffer to stream. """
    stream.write(audio_buffer)

    """ housekeeping :( """
    audio_file.close()
    stream.close()

    """ release the device. """
    audio_src.terminate()

def play_tone(digits, device_index=None):

    """ open the soundcard (device). """
    audio_src = open_device()

    """ open the device (audio) stream interface. """
    stream = _open_stream(audio_src)

    play_dtmf_tone(stream, digits)

    """ housekeeping :( """
    stream.close()

    """ release the device. """
    audio_src.terminate()


def main():
    play_tone("8128675309")
    # play_file("dtmf.wav", 6)

if __name__ == "__main__":
    main()
    print("running soundcard file.")
