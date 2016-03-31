#!/usr/bin/python
import pyaudio
import audioop
import wave
import speech_recognition as sr
from os import path
import time
import os
import sys

# Wait in silence to begin recording(<=2secs); wait in silence(>=2secs) to terminate

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
SILENT_CHUNKS = 2 * RATE / CHUNK  # about 2.5sec
# RECORD_SECONDS = 10
THRESHOLD = 60 # shall adjust to the voice card on a particular devices
WAVE_OUTPUT_FILENAME = "recording.wav"


class RingBufferFull:
    def __init__(self, n):
        self.max = n
        #self.data = [ for i in xrange(self.max)]
        self.data = []
        self.cur=0

    def append(self,x):
        """append an element at the end of the buffer"""
        self.data.append(x)

        if len(self.data) == self.max:
            self.cur=0
            self.data.pop(0)
        self.cur = (self.cur+1) % self.max

    def get(self):
        return self.data[self.cur]


def is_silent(data_chunk):
    # returns 'True' if not greater than the silent threshold
    # compute RMS
    rms = audioop.rms(data_chunk, 2)
    return rms < THRESHOLD


def save_speech(data, p):
    # write to file and close
    # rec_data = record()
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    # except wave.Error:
    # print("Nothing to be process")
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(data))
    waveFile.close()


def transcribe_asr():
    # obtain path to "recording.wav" in the same folder as this script
    WAV_FILE = path.join(path.dirname(path.realpath(__file__)), "recording.wav")

    # use "english.wav" as the audio source
    r = sr.Recognizer()
    with sr.WavFile(WAV_FILE) as source:
        audio = r.record(source)  # read the entire WAV file

    print "waiting ..."
    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        #  instead of `r.recognize_google(audio)`
        print("GSR thought you said: "),
        print r.recognize_google(audio)
        #print r.recognize_google(audio, show_all=True)
    except sr.UnknownValueError:
        print("GSR could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

# start Recording
audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
print ("recording...")
frames = []
x=RingBufferFull(2)
silent_chunks = 0
audio_started = False


# START: detect sound and start writing to file;
# TERMINATION: if 3secs silence
while True:
    data = stream.read(CHUNK)
    silent = is_silent(data)
    if audio_started:
        if silent:
            frames.append(data)
            silent_chunks += 1
            if silent_chunks > SILENT_CHUNKS:
                # write to file and close
                save_speech(frames, audio)
                transcribe_asr()
                frames = []
                silent_chunks = 0
                audio_started = False
                print "recording..."
                time.sleep(0.1)
        else:
            silent_chunks = 0
            frames.append(data)
    elif not silent:
        audio_started = True
        #append the buffer.current data into frame
        if len(frames) != 0:
            frames.append(x.get())
    else:
        x.append(data)

print("finished recording")

# close the stream
# #stop Recording
stream.stop_stream()
stream.close()
audio.terminate()