#!/usr/bin/python
#
# created by Ray on 2016-03-16
#
# Definition of class 'GSR' which recognize speech with Google Speech Recognizer.
# The class contains a loop function which is supposed to be called iteratively.
# This behavior can be refactored to perform iteration inside the function.
#
#

import os, time
import pyaudio, audioop, wave
import speech_recognition as sr
from tools.global_fn import print_debug
from configs.global_para import ASR_OUTPUT_WAVE

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
DEVICE = 0 # for laptop's mic
MAX_AMP = 800
MAX_LINE = 50
SLOPE = MAX_AMP / MAX_LINE


class GSR(object):
  def __init__(self):
    self.audio = None
    self.stream = None
    self.silence = [None]*SIL_BEG
    self.text = ''

    self.p_rb = 0
    self.p_sil = 0
    self.utterance = []
    self.rb_full = False
    self.recording = False
    return

  def reset(self):
    self.p_rb = 0
    self.p_sil = 0
    self.utterance = []
    self.rb_full = False
    self.recording = False

  def setup(self):
    self.audio = pyaudio.PyAudio()
    self.stream = self.audio.open(format=FORMAT,
                                  channels=CHANNELS,
                                  rate=RATE,
                                  frames_per_buffer=CHUNK,
                                  input_device_index=DEVICE,
                                  input=True)
    print_debug('asr | listening...\n')
    return

  def clean_up(self):
    self.stream.close()
    self.audio.terminate()
    return

  def save_speech(self, _data):
    # write to file and close
    waveFile = wave.open(ASR_OUTPUT_WAVE, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(_data))
    waveFile.close()
    return

  # save utterance as wave file and submit to GSR and save the returned text
  def transcribe(self):
    # obtain path to "recording.wav" in the same folder as this script
    # wave_file = os.path.join(path.dirname(path.realpath(__file__)), WAVE_OUTPUT_FILENAME)
    wave_file = os.path.join(ASR_OUTPUT_WAVE)
    recognizer = sr.Recognizer()
    with sr.WavFile(wave_file) as source:
      _data = recognizer.record(source)  # read the entire WAV file
    # recognize speech using Google Speech Recognition
    try:
      self.text = recognizer.recognize_google(_data)
      # print recognizer.recognize_google(_data, show_all=True)
    except sr.UnknownValueError:
      # print(" | error: could not understand audio (empty input?)")
      self.text = '(empty)'
    except sr.RequestError as e:
      print_debug('asr | error: could not request results from service; {0}\n'.format(e))
      self.clean_up()
      exit()
    return

  # record utterance to wave file and submit it to GSR
  def process(self):
    # suspend mic
    self.stream.stop_stream()
    print_debug('asr | processing...\n')

    # (deprecated) for processing ring buffer that could be not full
    # if self.rb_full:
    #   _data = self.silence[self.p_rb:] + self.silence[:self.p_rb] + self.utterance
    # else:
    #   _data = self.silence[:self.p_rb] + self.utterance

    # ring better is guaranteed to be full
    data = self.silence[self.p_rb:] + self.silence[:self.p_rb] + self.utterance
    # save as wave file
    self.save_speech(data)
    # submit to GSR
    self.transcribe()
    print_debug('asr | speech: %s\n' % self.text)
    self.reset()
    self.stream.start_stream()
    print_debug('asr | listening...\n')
    return

  # terminate after 10 sec
  def loop_test(self):
    self.p_rb += 1
    print 'asr | loop test %d...' % self.p_rb
    if self.p_rb==10: self.text='exit'
    time.sleep(1)
    return

  # not recording and silent: append to ring buffer
  # not recording and not silent: append to utterance
  # recording and silent: append to utterance
  # recording and not silent: append to utterance
  def loop(self):
    # record new data chunk from mic
    data = self.stream.read(CHUNK)
    # calculate amplitude based on root mean square
    amp = audioop.rms(data, DEPTH/8)
    # display amplitude bar
    bar_len = min(MAX_LINE, amp/SLOPE)
    print_debug('['+'|'*bar_len+' '*(MAX_LINE-bar_len)+'] rms:'+str(amp))
    # determine silent or not based on threshold
    silent = amp < THRESHOLD
    if silent and not self.recording:
      # append data to ring buffer
      self.silence[self.p_rb] = data
      self.p_rb = (self.p_rb + 1) % SIL_BEG
      if not self.p_rb: self.rb_full = True
    else:
      # ensure 1 sec of beginning silence for the first utterance
      if not self.rb_full: return
      # append data to utterance
      self.utterance.append(data)
      if not self.recording:
        # implies that it's not silent
        self.recording = True
      elif silent:
        # implies that it's recording
        self.p_sil += 1
        if self.p_sil == SIL_END:
          # utterance collected, process!
          self.process()
      else:
        # recording and not silent
        self.p_sil = 0
    return


# main function of the asr process
def asr_process(pipe):
  print 'asr | process started'
  gsr = GSR()
  # setup gsr
  gsr.setup()
  while True:
    # process input command if any
    if pipe.poll():
      cmd = pipe.recv()
      print_debug('asr | received: %s\n' % cmd)
      if cmd=='exit': break
    # loop gsr
    # gsr.loop_test()
    gsr.loop()
    # send recognized text if any
    if gsr.text:
      pipe.send(gsr.text)
      if gsr.text=='exit': break
      gsr.text = ''
  # clean up gsr
  gsr.clean_up()
  pipe.close()
  print 'asr | process terminated'
  return


if __name__ == '__main__':
  _gsr = GSR()
  _gsr.setup()
  while True:
    # _gsr.loop_test()
    _gsr.loop()
    if _gsr.text=='exit': break
  _gsr.clean_up()
