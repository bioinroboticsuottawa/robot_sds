import os
import sys

# path = 'named_pipe.fifo'
# while True:
#   print('waiting...')
#   fifo = open(path, 'r')
#   msg = fifo.readline()
#   print 'received: ' + msg
#   fifo.close()
#   if msg=='exit': break

import wave, pyaudio
fn = 'tts.wav'
_wav = wave.open(fn,'rb')
_audio = pyaudio.PyAudio()
_sample_width = _wav.getsampwidth()
_format = _audio.get_format_from_width(_sample_width)
_channels = _wav.getnchannels()
_rate = _wav.getframerate()

print _sample_width
print _format
print _channels
print _rate


