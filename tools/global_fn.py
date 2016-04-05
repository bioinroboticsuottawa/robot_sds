#!/usr/bin/python
#
# created by Ray on 2016-03-31
#
# Definition of global available functions.
#

import sys,time


LINE_LEN = 80
def print_debug(s=None):
  sys.stdout.write('\r' + ' ' * LINE_LEN + '\r')
  if s: sys.stdout.write(s)
  sys.stdout.flush()
  return

def enum(*enums):
  enums = dict(zip(enums,range(len(enums))))
  return type('EnumType', (), enums)


if __name__ == '__main__':
  MODULE = enum('ACT','BBC','CVF')
  print MODULE.ACT
  print MODULE.CVF
  print MODULE.BBC
  print_debug('abc')
  time.sleep(1)
  print_debug('cde')
  time.sleep(1)
  print_debug('efg')
