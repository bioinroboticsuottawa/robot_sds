import pyaudio
import audioop
import sys
import wave
import speech_recognition as sr
from os import path
import time


FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
SILENT_CHUNKS = 2 * RATE / CHUNK  # about 2 sec
THRESHOLD = 24  # NEED adjust to the voice card on a particular devices
WAVE_OUTPUT_FILENAME = "test.wav"

audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
print '=> recording...'

frames = []
silent_chunks = 0
audio_started = False


def print_debug(s):
    sys.stdout.write('\r                                      \r'+s)

def is_silent(data_chunk):
    rms = audioop.rms(data_chunk, 2)
    print_debug(' | rms: '+str(rms))
    return rms < THRESHOLD

# while True:
for i in xrange(10 * RATE / CHUNK ):
    data = stream.read(CHUNK)
    silent = is_silent(data)
    time.sleep(0.01)
    # if audio_started:
    #     if silent:
    #         silent_chunks += 1
    #         if silent_chunks > SILENT_CHUNKS:
    #             # write to file and close
    #             save_speech(frames, audio)
    #             transcribe_asr()
    #             frames = []
    #             silent_chunks = 0
    #             audio_started = False
    #             time.sleep(0.1)
    #     else:
    #         silent_chunks = 0
    #         frames.append(data)
    # elif not silent:
    #     audio_started = True

stream.stop_stream()
stream.close()
audio.terminate()

print '\n=> end'

