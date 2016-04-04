#!/usr/bin/python
#
# created by Ray on 2016-04-03
#
# Definition of class "TTS" which take a text string as input, and request an wave file using apiai interface.
# Function 'setup' and 'clean_up' should be called at the beginning and end of any TTS process.
# process
#

import time, os
import json
import requests
import wave, pyaudio
from configs.global_para import API_AI_CREDENTIAL,TTS_OUTPUT_WAVE,TTS_URL
from tools.print_debug import print_debug

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 22050
CHUNK = 1024

class TTS(object):
  def __init__(self):
    self.audio = None
    self.stream = None
    self.credential_file = API_AI_CREDENTIAL
    with open(self.credential_file) as fin:
      data = json.load(fin)
      self.access_token = data['apiai']['CLIENT_ACCESS_TOKEN']
      self.access_key = data['apiai']['SUBSCRIPTION_KEY']
    self.http_header = {'Authorization' : 'Bearer '+self.access_token,
                        'ocp-apim-subscription-key' : self.access_key,
                        'Accept-language' : 'en-US'}
    # self.http_para = {'v' : '20150910'}
    self.text = ''
    self.result = False
    return

  def setup(self):
    self.audio = pyaudio.PyAudio()
    self.stream = self.audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, start=False)
    return

  def clean_up(self):
    self.stream.close()
    self.audio.terminate()
    return

  def play(self):
    # make sure the wave file exist
    if not os.path.exists(TTS_OUTPUT_WAVE): return
    wav = wave.open(TTS_OUTPUT_WAVE, 'rb')
    # start stream
    self.stream.start_stream()
    # play stream
    data = wav.readframes(CHUNK)
    while data != '':
      self.stream.write(data)
      data = wav.readframes(CHUNK)
    # stop stream
    self.stream.stop_stream()

  def loop(self):
    if self.text:
      # self.http_para['text'] = self.text
      text = '+'.join(self.text.split())
      with open(TTS_OUTPUT_WAVE, 'wb') as outfile:
        # response = requests.get(TTS_URL, headers=self.http_header, data=self.http_para, stream=True)
        url = TTS_URL+'&text='+text
        response = requests.get(url, headers=self.http_header, stream=True)
        if not response.ok:
          # Something went wrong
          print_debug('tts | fail to download wave file ({0})\n'.format(response.status_code))
        else:
          for block in response.iter_content(1024):
            outfile.write(block)
          self.result = True
          # print_debug('tts | wave file downloaded\n')
    time.sleep(0.01)
    return


# main function of the tts process
def tts_process(pipe):
  print_debug('tts | process started\n')
  tts = TTS()
  while True:
    # process input command if any
    if pipe.poll():
      text = pipe.recv()
      if text=='exit': break
      tts.text = text
    tts.loop()
    # play the returned wave only once
    if tts.result:
      # pipe.send('something')
      print_debug('tts | playing back...\n')
      tts.play()
      tts.result = False
  pipe.close()
  print_debug('tts | process terminated\n')
  return


if __name__ == '__main__':
  TTS_OUTPUT_WAVE = '../tmp/tts.wav'
  API_AI_CREDENTIAL = '../configs/credential.json'
  _tts = TTS()
  _tts.setup()
  _tts.text = 'it\'s 26 degree, with shower rain.'
  _tts.loop()
  if _tts.result:
    print_debug('tts | playing back...\n')
    _tts.play()
  _tts.clean_up()

