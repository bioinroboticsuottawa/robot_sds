#!/usr/bin/python
#
# created by ray on 2016-03-16
#
# Detects available audio input/output devices.
#

import pyaudio

#
# list devices
#
def list_devices():
  ret = {'in_dev': [], 'out_dev': [], 'sel_dev': None}
  p = pyaudio.PyAudio()
  info = p.get_host_api_info_by_index(0)
  num_devices = info.get('deviceCount')
  # for each audio device, determine if is an input or an output and add it to the appropriate list and dictionary
  for id in range(0, num_devices):
    dev_info = p.get_device_info_by_host_api_device_index(0, id)
    dev_name = dev_info.get('name')
    if dev_info.get('maxInputChannels') > 0:
      ret['in_dev'].append((id,dev_name))
    if dev_info.get('maxOutputChannels') > 0:
      ret['out_dev'].append((id, dev_name))
  ret['sel_dev'] = (1,p.get_device_info_by_index(1).get('name'))
  p.terminate()
  return ret


if __name__ == '__main__':
  devices = list_devices()
  print 'Input Devices:'
  for id,name in devices['in_dev']:
    print '| id: %d, name: %s' % (id,name)
  print 'Output Devices:'
  for id, name in devices['out_dev']:
    print '| id: %d, name: %s' % (id, name)
  print 'Selected Devices:'
  print '| id: %d, name: %s' % (devices['sel_dev'][0], devices['sel_dev'][1])
