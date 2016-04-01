import os
import sys

path = 'named_pipe.fifo'
while True:
  print('waiting...')
  fifo = open(path, 'r')
  msg = fifo.readline()
  print 'received: ' + msg
  fifo.close()
  if msg=='exit': break

