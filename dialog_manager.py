#!/usr/bin/python
#
# created by ray on 2016-3-31
#
# dialog manager class
#

from multiprocessing import Process,Queue
from ASR.asr import asr_process

class DialogManager(object):
  def __init__(self):
    self.queue = Queue()
    self.asr_proc = None
  def exit_asr(self):
    self.queue.put('exit')
    self.asr_proc.join()
  def start_asr(self):
    self.asr_proc = Process(target=asr_process, args=(self.queue,))
    self.asr_proc.start()
  def send_msg(self, msg):
    self.queue.put(msg)
