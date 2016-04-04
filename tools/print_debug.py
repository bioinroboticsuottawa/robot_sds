#!/usr/bin/python
#
# created by Ray on 2016-03-31
#
# clean current line anyway
# if given a string, print at the same line
#

import sys,time

LINE_LEN = 80

def print_debug(s=None):
  sys.stdout.write('\r' + ' ' * LINE_LEN + '\r')
  if s: sys.stdout.write(s)
  sys.stdout.flush()
  return

if __name__ == '__main__':
  print_debug('abc')
  time.sleep(1)
  print_debug('cde')
  time.sleep(1)
  print_debug('efg')
