#!/usr/bin/python
#
# created by ray on 2016-03-16
#
# Function "list_devices" detects available audio input/output devices.
#
# Function "amplitude_testing" displays the input signal amplitude by calculating the
# root mean square of the data chunk. Terminate the program with keyboard interrupt.
#

import pyaudio
import audioop
import sys
import time

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 4096
DEPTH = 16 # signal depth in bits
MAX_AMP = 800
MAX_LINE = 50
SLOPE = MAX_AMP/MAX_LINE
# DEVICE = 0 # for laptop's mic
DEVICE = 3 # for lab's mic
# SEC = 30


#
# amplitude testing
#
def print_debug(s):
  sys.stdout.write('\r'+' '*80+'\r'+s)
  sys.stdout.flush()

def amplitude_testing():
  audio = pyaudio.PyAudio()
  stream = audio.open(format = FORMAT,
                      channels = CHANNELS,
                      rate = RATE,
                      input = True,
                      frames_per_buffer = CHUNK,
                      input_device_index = DEVICE)
  print '=> testing...'

  # for i in xrange(SEC * RATE / CHUNK ):
  #     data = stream.read(CHUNK)
  #     print_debug(' | rms: '+str(audioop.rms(data, 2)))
  #     time.sleep(0.01)
  utter,thres = 0,200
  while True:
    try:
      data = stream.read(CHUNK)
      rms = audioop.rms(data, DEPTH / 8)
      if rms>thres: utter+=1
      progress = min(MAX_LINE,rms/SLOPE)
      print_debug('['+'|'*progress+' '*(MAX_LINE-progress)+'] rms:'+str(rms))
      time.sleep(0.01)
    except KeyboardInterrupt:
      print ; break

  stream.stop_stream()
  stream.close()
  audio.terminate()
  print 'number of utter: %d' % utter
  print 'utter: %g sec' % (float(utter*CHUNK)/RATE)
  print '=> end'

if __name__ == '__main__':
  amplitude_testing()
