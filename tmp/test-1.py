import os
import sys

# path = 'named_pipe.fifo'
# while True:
#   print('waiting...')
#   fifo = open(path, 'r')
#   msg = fifo.readline()
#   print 'received: ' + msg
#   fifo.close()
#   if msg=='exit': break

class ACTIONS:
  NONE = 0
  HAND_UP = 1
  HAND_DOWN = 2
  BYE = 3

if __name__ == '__main__':
  a = None
  print a==ACTIONS.NONE
  print not a
  print not ACTIONS.NONE


