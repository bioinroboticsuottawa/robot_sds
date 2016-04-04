#!/usr/bin/python
#
# created by Ray on 2016-04-04
#
# Definition of class 'Action'.
#

import os, time
from tools.print_debug import print_debug
from configs.global_para import ACTION_SCRIPT

# define enum structure 'ACTION' as a class
class ACTION:
  NONE = 0
  HAND_UP = 1
  HAND_DOWN = 2
  BYE = 3

class ACT(object):
  def __init__(self):
    self.cmd = ''
    self.result = False
    self.cmd2str = {ACTION.HAND_UP:'hand-up', ACTION.HAND_DOWN:'hand-down', ACTION.BYE:'bye'}
    return

  def loop_test(self):
    if self.cmd:
      self.result = self.cmd2str[int(self.cmd)]
      self.cmd = ''
    time.sleep(0.01)
    return

  def loop(self):
    if self.cmd:
      shell_cmd = ACTION_SCRIPT+' '+self.cmd
      os.system(shell_cmd)
      # the 'result' variable return the name of the action as a string
      # but it can also be used to return the action performing status later
      self.result = self.cmd2str[int(self.cmd)]
      self.cmd = ''
    time.sleep(0.01)
    return

def act_process(pipe):
  print_debug('act | process started\n')
  act = ACT()
  while True:
    # process input command if any
    if pipe.poll():
      text = pipe.recv()
      if text == 'exit': break
      act.text = text
    act.loop_test()
    # play the returned wave only once
    if act.result:
      # pipe.send('something')
      print_debug('act | performing action \'%s\'...\n'%act.result)
      act.result = ''
  pipe.close()
  print_debug('act | process terminated\n')
  return

if __name__ == '__main__':
  _act = ACT()
  _act.cmd = '1'
  _act.loop_test()
  if _act.result:
    print_debug('act | performing action \'%s\'...\n' % _act.result)
    _act.result = ''


