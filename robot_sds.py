#!/usr/bin/python
#
# created by ray on 2016-3-31
#
# main program of the spoken dialog system
#
from multiprocessing import Queue
from dialog_manager import DialogManager


if __name__ == '__main__':
  dm = DialogManager()
  while True:
    cmd = raw_input('command: ')
    if not cmd:
      continue
    elif cmd == 'exit':
      break
    elif cmd == 'exit asr':
      dm.exit_asr()
    elif cmd == 'start asr':
      dm.start_asr()
    else:
      dm.send_msg(cmd)

