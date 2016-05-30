#!/usr/bin/python
#
# created by ray on 2016-04-03
#
# Definition of class 'SLU'
# Given the transcribed text string from ASR, recognize user's intent using pre-trained HMM sequence classifier.
# The output is either action commands to a robot or speech answers for questions.
#

import time
import json
import apiai
from tools.global_fn import print_debug, enum
from configs.global_para import API_AI_CREDENTIAL, HMM_MODEL_PATH
from hmm_sequence_recognizer import predefined_hmm


from tools.act import ACTION

class SLU(object):
  def __init__(self):
    self.SENT_TYPE = enum('DECLARATIVE','IMPERATIVE','INTERROGATIVE')
    self.credential_file = API_AI_CREDENTIAL
    with open(self.credential_file) as fin:
      data = json.load(fin)
      self.access_token = data['apiai']['CLIENT_ACCESS_TOKEN']
      self.access_key = data['apiai']['SUBSCRIPTION_KEY']
    self.ai = apiai.ApiAI(self.access_token, self.access_key)
    self.result = {}
    self.text = ''
    self.hmm_seq_recognizer = None
    self.load_hmm()
    return

  # load HMM models
  # pickle load objects based on the reference of where it dump
  def load_hmm(self):
    # very ugly hard-coded setting, fix it later
    # set True to train new model and False to load from pre-trained
    print_debug('slu | initializing recognizer...\n')
    self.hmm_seq_recognizer = predefined_hmm(HMM_MODEL_PATH, False)
    return

  # exit in 10 sec
  def loop_test(self):
    self.text += 'a'
    self.result = {'mod':'tts' if len(self.text)%2 else 'act', 'data':self.text}
    time.sleep(1)

  # this is really a quick and dirty implementation of action recognition
  # but i will re-implement it later using nearest neighbor algorithm
  # with verb bow, tf-idf and wordnet similarity as features
  def recognize_action(self):
    if self.text.find('rectangle')!=-1:
      # return str(ACTION.RECTANGLE)
      return 'rectangle'
    elif self.text.find('circle')!=-1:
      # return str(ACTION.CIRCLE)
      return 'circle'
    elif self.text.find('triangle')!=-1:
      # return str(ACTION.TRIANGLE)
      return 'triangle'
    elif self.text.find('wave')!=-1:
      # return str(ACTION.BYE)
      return 'wave'
    elif self.text.find('rotate')!=-1:
      # return str(ACTION.ROTATE)
      return 'rotate'
    else:
      return ''
  # def recognize_action(self):
  #   if self.text.find('one')!=-1:
  #     return str(ACTION.HAND_UP)
  #   elif self.text.find('two')!=-1:
  #     return str(ACTION.HAND_DOWN)
  #   elif self.text.find('three')!=-1:
  #     return str(ACTION.BYE)
  #   else:
  #     return str(ACTION.NONE)

  # main loop function of the slu process
  def loop(self):
    if self.text:
      sent_type = self.hmm_seq_recognizer.predict_sentence(self.text)
      if sent_type==self.SENT_TYPE.IMPERATIVE:
        # this utterance is a command
        # perform further recognition to determine the action
        # should include 'none' action when the confidence is low
        action = self.recognize_action()
        if action: self.result={'mod': 'act', 'data': action}
        else: self.result = {'mod': 'tts', 'data': 'sorry that is beyond my ability'}
      else:
        # this utterance is a question or statement
        request = self.ai.text_request()
        request.lang = 'en'  # optional, default value equal 'en'
        request.query = self.text
        resp = request.getresponse().read()
        data = json.loads(resp)
        speech = data['result']['fulfillment']['speech']
        self.result = {'mod': 'tts', 'data': speech}
      self.text = ''




# main function of the asr process
def slu_process(pipe):
  slu = SLU()
  print_debug('slu | process started\n')
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
