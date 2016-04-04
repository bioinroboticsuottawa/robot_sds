#!/usr/bin/python
#
# created by Ray on 2016-04-01
#
# A controller for sending commands to the main process of the spoken dialog system.
# Communicate with the main process by sending text strings through named pipe.
# This can be replaced with sockets if remote control is required.
#
# Note: this program should be run before the main process, and it will block
# until the main process starts.
#

import os

# path to the named pipe
NP_PATH = '../named_pipe.fifo'

if __name__ == '__main__':
  # create name pipe, remove first if already exist
  if os.path.exists(NP_PATH):
    os.remove(NP_PATH)
  os.mkfifo(NP_PATH)
  print '=> controller started'

  # main loop of controller
  while True:
    fifo = open(NP_PATH, 'w')
    msg = raw_input('command: ')
    # send to main program
    fifo.write(msg)
    fifo.flush()
    fifo.close()
    # exit with command 'exit'
    if msg=='exit': break

  # remove named pipe to prevent main program running without controller
  if os.path.exists(NP_PATH):
    os.remove(NP_PATH)
  print '=> controller closed'
