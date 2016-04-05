#!/usr/bin/python
#
# created by Ray on 2016-04-03
#
# Definition of class 'SLU'
#
#

import time
import json
import apiai
from tools.global_fn import print_debug
from configs.global_para import API_AI_CREDENTIAL

UNKNOWN,QUESTION,ACTION = 0,1,2

class SLU(object):
  def __init__(self):
    self.credential_file = API_AI_CREDENTIAL
    with open(self.credential_file) as fin:
      data = json.load(fin)
      self.access_token = data['apiai']['CLIENT_ACCESS_TOKEN']
      self.access_key = data['apiai']['SUBSCRIPTION_KEY']
    self.ai = apiai.ApiAI(self.access_token, self.access_key)
    self.result = {}
    self.text = ''

  # classify input text to get dialog act
  # currently only consider 'command' and 'question'
  def classify(self):
    if self.text:
      return QUESTION

  # exit in 10 sec
  def loop_test(self):
    self.text += 'a'
    self.result = {'mod':'tts' if len(self.text)%2 else 'act', 'data':self.text}
    time.sleep(1)

  def loop(self):
    if self.text:
      cls = self.classify()
      if cls==QUESTION:
        request = self.ai.text_request()
        request.lang = 'en'  # optional, default value equal 'en'
        request.query = self.text
        resp = request.getresponse().read()
        data = json.loads(resp)
        speech = data['result']['fulfillment']['speech']
        self.result = {'mod':'tts','data':speech}
      else:
        # perform recognition to determine the action, should include 'none' action when the confidence is low
        self.result = {'mod': 'act', 'data': 'some action'}
      self.text = ''

# main function of the asr process
def slu_process(pipe):
  print_debug('slu | process started\n')
  slu = SLU()
  while True:
    # process input command if any
    if pipe.poll():
      text = pipe.recv()
      if text=='exit': break
      slu.text = text
    slu.loop()
    # send result back to dialog manager
    if slu.result:
      pipe.send(slu.result)
      print_debug('slu | %s | %s\n' % (slu.result['mod'],slu.result['data']))
      slu.result = None
  pipe.close()
  print_debug('slu | process terminated\n')
  return


if __name__ == '__main__':
  _slu = SLU()
  _slu.text = 'how is the weather in Vancouver'
  _slu.loop()
  # while True:
  #   # _gsr.loop_test()
  #   _slu.loop_test()
  #   if _slu.result:
  #     print _slu.result
  #     if _slu.result['data']=='a'*10: break
