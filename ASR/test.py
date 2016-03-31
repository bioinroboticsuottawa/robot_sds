import sys
import time

def print_debug(s):
  sys.stdout.write('\r' + ' ' * 20 + '\r' + s)
  sys.stdout.flush()

for i in xrange(1,21):
  print_debug('|'+'.'*i+' '*(20-i)+'| %d%%'%i)
  time.sleep(0.2)
