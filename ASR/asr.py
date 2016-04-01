#!/usr/bin/python
#
# created by ray on 2016-03-16
#
# Definition of class "GSR" which recognize speech with Google Speech Recognizer.
# The class contains a loop function which is supposed to be called iteratively.
# This behavior can be refactored to perform iteration inside the function.
#
#

import pyaudio
import audioop
import wave
import speech_recognition as sr
from os import path
import sys
import time

FORMAT = pyaudio.paInt16
DEPTH = 16
CHANNELS = 1
RATE = 44100
CHUNK = 4096
SIL_BEG = 1 * RATE / CHUNK  # <= 1 sec
SIL_END = 2 * RATE / CHUNK  # <= 2 sec
# RECORD_SECONDS = 10
THRESHOLD = 500  # shall adjust to the voice card on a particular devices
# DEVICE = 3 # for lab's mic
DEVICE = 1 # for laptop's mic
WAVE_OUTPUT_FILENAME = "recording.wav"


class GSR(object):
  def __init__(self):
    self.audio = None
    self.stream = None
    self.silence = [None] * SIL_BEG
    self.utterance = []
    self.p_rb = 0
    self.p_sil = 0
    self.text = ''
    self.rb_full = False
    self.recording = False

  # def __del__(self):
  #   self.stream.close()
  #   self.audio.terminate()

  def save_speech(self, _data):
    # write to file and close
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(_data))
    waveFile.close()

  # def run(self):
  #   while True:
  #     print self.status
  #     if self.status & STAT_EXIT: break
  #     time.sleep(2)

  def setup(self):
    self.audio = pyaudio.PyAudio()
    self.stream = self.audio.open(format=FORMAT,
                                  channels=CHANNELS,
                                  rate=RATE,
                                  input=True,
                                  frames_per_buffer=CHUNK,
                                  input_device_index=DEVICE)
    print '=> asr started'

  def cleanup(self):
    self.stream.close()
    self.audio.terminate()
    print '=> asr terminated'

  @staticmethod
  def transcribe():
    # obtain path to "recording.wav" in the same folder as this script
    wave_file = path.join(path.dirname(path.realpath(__file__)), WAVE_OUTPUT_FILENAME)
    recognizer = sr.Recognizer()
    with sr.WavFile(wave_file) as source:
      _data = recognizer.record(source)  # read the entire WAV file
    # recognize speech using Google Speech Recognition
    text = ''
    try:
      text = recognizer.recognize_google(_data)
      # print recognizer.recognize_google(_data, show_all=True)
    except sr.UnknownValueError:
      # print(" | error: could not understand audio (empty input?)")
      text = '(empty)'
    except sr.RequestError as e:
      print(" | error: could not request results from service; {0}".format(e))
      exit()
    return text

  # callback function for record event
  def record_cb(self):
    self.stream.stop_stream()
    self.print_debug()
    print(" | processing... ")
    if self.rb_full:
      _data = self.silence[self.p_rb:] + self.silence[:self.p_rb] + self.utterance
    else:
      _data = self.silence[:self.p_rb] + self.utterance
    self.save_speech(_data)
    text = self.transcribe()
    print(" | text: "), text
    if text == 'exit': return False
    self.p_rb = 0
    self.p_sil = 0
    self.text = ''
    self.utterance = []
    self.rb_full = False
    self.recording = False
    self.stream.start_stream()
    print('=> listening...')
    return True

  @staticmethod
  def print_debug(s=None):
    spaces = ' ' * 20
    sys.stdout.write('\r' + spaces + '\r')
    if s: sys.stdout.write(s)
    sys.stdout.flush()

  def loop_test(self):
      print('running...')
      time.sleep(2)

  def loop(self):
    print('=> listening...')
    while True:
      # if self.status & STAT_EXIT: break
      data = self.stream.read(CHUNK)
      amp = audioop.rms(data, DEPTH / 8)
      self.print_debug(' | rms: ' + str(amp))
      silent = amp < THRESHOLD
      if silent and not self.recording:
        # append data to ring buffer
        self.silence[self.p_rb] = data
        self.p_rb = (self.p_rb + 1) % SIL_BEG
        if not self.p_rb: self.rb_full = True
      else:
        # ensure 1 sec of beginning silence for the first utterance
        if not self.rb_full: continue
        # append data to utterance
        self.utterance.append(data)
        if not self.recording:
          # implies that it's not silent
          self.recording = True
        elif silent:
          # implies that it's recording
          self.p_sil += 1
          if self.p_sil == SIL_END and not self.record_cb(): break
        else:
          # recording and not silent
          self.p_sil = 0
    print('=> end')
    return True

def asr_process(queue):
  gsr = GSR()
  gsr.setup()
  while True:
    if not queue.empty():
      cmd = queue.get()
      print 'cmd: %s'%cmd
      if cmd=='exit': break
    gsr.loop_test()
  gsr.cleanup()

# not rec and sil: append to rb
# not rec and not sil: append to frame
# rec and sil: append to frame
# rec and not sil: append to frame
if __name__ == '__main__':
  gsr = GSR()
  gsr.loop()
