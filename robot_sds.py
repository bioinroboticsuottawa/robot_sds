#!/usr/bin/python
#
# created by Ray on 2016-03-31
#
# Main program of the spoken dialog system, requires controller to be running.
#

import os
import time
from dialog_manager import DialogManager


NP_PATH = 'named_pipe.fifo'

if __name__ == '__main__':
  # make sure the controller is running
  if not os.path.exists(NP_PATH):
    print '=> missing named pipe, please run the controller first'
    exit()

  # initialize dialog manager
  dm = DialogManager()
  print '=> dialog manager started'

  # main loop, receive commands from named pipeto and relay to dialog manager
  while True:
    # print('waiting...')
    fifo = open(NP_PATH, 'r')
    # receive command from controller through named pipe
    cmd = fifo.readline()
    print 'controller | ' + cmd
    fifo.close()
    ret = dm.handle(cmd)
    if not ret: break
    # leave time for controller to open the named pipe first
    time.sleep(0.1)

  print '=> dialog manager closed'

