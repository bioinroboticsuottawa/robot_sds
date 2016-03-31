import pyaudio
import audioop
import sys
import time
import wave
import speech_recognition as sr
from os import path

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 2048
DEVICE = 3
SEC = 30

#
# list device
#
# p = pyaudio.PyAudio()
# info = p.get_host_api_info_by_index(0)
# num_devices = info.get('deviceCount')
# #for each audio device, determine if is an input or an output and add it to the appropriate list and dictionary
# for i in range (0, num_devices):
#     if p.get_device_info_by_host_api_device_index(0,i).get('maxInputChannels')>0:
#         print "Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0,i).get('name')
#     if p.get_device_info_by_host_api_device_index(0,i).get('maxOutputChannels')>0:
#         print "Output Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0,i).get('name')
# dev_info = p.get_device_info_by_index(1)
# print "Selected device is ", dev_info.get('name')
# p.terminate()

#
# threshold testing
#
audio = pyaudio.PyAudio()
stream = audio.open(format = FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    input = True,
                    frames_per_buffer = CHUNK,
                    input_device_index = DEVICE)
print '=> testing...'

def print_debug(s):
    sys.stdout.write('\r                                      \r'+s)

for i in xrange(SEC * RATE / CHUNK ):
    data = stream.read(CHUNK)
    print_debug(' | rms: '+str(audioop.rms(data, 2)))
    time.sleep(0.01)

stream.stop_stream()
stream.close()
audio.terminate()
print '\n=> end'

