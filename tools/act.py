#!/usr/bin/python
#
# created by Ray on 2016-04-04
#
# Definition of class 'ACT'.
# The class executes predefined shell scripts to control a robot.
#

import os, time
from tools.global_fn import print_debug, enum
from configs.global_para import ACTION_SCRIPT
from subprocess import call

# define enum structure 'ACTION' as a class
ACTION = enum('NONE','RECTANGLE','CIRCLE','TRIANGLE','WAVE','ROTATE')
ACT2STR = {ACTION.NONE:'none', ACTION.RECTANGLE:'rectangle', ACTION.CIRCLE:'circle', ACTION.TRIANGLE:'triangle', ACTION.WAVE:'wave', ACTION.ROTATE:'rotate'}

class ACT(object):
  def __init__(self):
    self.cmd = ''
    self.result = False
    return

  def loop_test(self):
    if self.cmd:
      print_debug('act | performing action \'%s\'...\n' % ACT2STR[int(self.cmd)])
      # the 'result' variable is currently not being used
      # but it can be used later to return the action performing status
      self.result = True
      self.cmd = ''
    return

  def loop(self):
    if self.cmd:
      print_debug('act | performing action ...\n')
      # shell_cmd = ACTION_SCRIPT+' '+self.cmd
      # os.system(shell_cmd)
      call([ACTION_SCRIPT, self.cmd])
      # the 'result' variable is currently not being used
      # but it can be used later to return the action performing status
      self.result = True
      self.cmd = ''
    return

def act_process(pipe):
  print_debug('act | process started\n')
  act = ACT()
  while True:
    # process input command if any
    if pipe.poll():
      text = pipe.recv()
      if text == 'exit': break
      act.cmd = text
    act.loop()
    # feed back if necessary
    if act.result:
      print_debug('act | action done')
      # pipe.send('some kind of indicator')
      act.result = False
    # less CPU occupancy
    time.sleep(0.01)
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


