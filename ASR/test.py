
import os
import multiprocessing


path = 'named_pipe.fifo'
os.unlink(path)
# if os.path.isfile(path):
#   os.remove(path)
os.mkfifo(path)

while True:
  fifo = open(path, 'w')
  msg = raw_input('message: ')
  fifo.write(msg)
  fifo.close()
  if msg=='exit': break



# while True:
#   cmd = raw_input('command: ')
#   if cmd=='exit': break
#   elif not cmd: continue
#   else: print cmd
