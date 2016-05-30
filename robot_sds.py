#!/usr/bin/python
#
# created by ray on 2016-03-31
#
# Main program of the spoken dialog system, requires controller to be running.
# Received commands from controller through named pipe, and send to dialog manager for processing.
#

import os, time
from multiprocessing import Process,Pipe
from dialog_manager import dm_process
from tools.global_fn import print_debug
from configs.global_para import NAMED_PIPE


print 'named pipe: %s' % NAMED_PIPE

if __name__ == '__main__':
  # make sure the controller is running
  if not os.path.exists(NAMED_PIPE):
    print '=> missing named pipe, please run the controller first'
    exit()

  # create dialog manager process
  parent,child = Pipe()
  dmp = Process(target=dm_process, args=(child,))
  dmp.start()

  # main loop, receive commands from named pipeto and relay to dialog manager
  while True:
    # print('waiting...')
    fifo = open(NAMED_PIPE, 'r')
    # receive command from controller through named pipe
    cmd = fifo.readline()
    print_debug('controller | '+cmd)
    fifo.close()
    # send command to dialog manager
    parent.send(cmd)
    if cmd=='exit':
      # wait for dialog manager to terminate
      dmp.join()
      # close parent pipe, child pipe will be close in child process
      parent.close()
      break
    # leave time for controller to open the named pipe first
    time.sleep(0.1)

