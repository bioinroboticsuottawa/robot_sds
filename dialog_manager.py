#!/usr/bin/python
#
# created by Ray on 2016-03-31
#
# Definition of DialogManager class.
#

import time
from multiprocessing import Process,Pipe
from ASR.asr import asr_process
from SLU.slu import slu_process
from tools.tts import tts_process
from tools.act import act_process
from tools.global_fn import print_debug,enum

NUM_MODULES = 4
MODULE = enum('ASR','SLU','TTS','ACT','ALL')
PROCESS_FN = {MODULE.ASR:asr_process,
              MODULE.SLU:slu_process,
              MODULE.TTS:tts_process,
              MODULE.ACT:act_process}


class DialogManager(object):
  def __init__(self):
    self.processes = [None]*NUM_MODULES # process pool, escape module 'all'
    self.pipes = [None]*NUM_MODULES # parent pipe of each process, escape module 'all'
    self.mod2id = {'all':MODULE.ALL, 'asr':MODULE.ASR, 'slu':MODULE.SLU, 'tts':MODULE.TTS, 'act':MODULE.ACT}
    self.id2mod = {MODULE.ALL:'all', MODULE.ASR:'asr', MODULE.SLU:'slu', MODULE.TTS:'tts', MODULE.ACT:'act'}
    return

  # start module with module id
  def start_module(self, mod_id):
    if mod_id == MODULE.ALL:
      self.start_all()
      return
    if not self.processes[mod_id]:
      parent, child = Pipe()
      self.pipes[mod_id] = parent
      # self.processes[mid] = Queue()
      try:
        self.processes[mod_id] = Process(target=PROCESS_FN[mod_id], args=(child,))
        self.processes[mod_id].start()
      except Exception as e:
        print_debug('manager | unable to start {0} ({1})\n'.format(self.id2mod[mod_id],e))
    else:
      print_debug('manager | %s already started\n' % self.id2mod[mod_id])
    return

  # terminate module with module id
  def terminate_module(self, mod_id):
    if mod_id==MODULE.ALL:
      self.terminate_all()
      return
    if self.processes[mod_id]:
      if self.processes[mod_id].is_alive():
        self.pipes[mod_id].send('exit')
        self.processes[mod_id].join()
      else:
        print_debug('manager | %s terminated\n' % self.id2mod[mod_id])
      self.processes[mod_id] = None
    if self.pipes[mod_id]:
      self.pipes[mod_id].close()
      self.pipes[mod_id] = None
    else:
      print_debug('manager | %s already terminated\n' % self.id2mod[mod_id])
    return

  # start all modules
  def start_all(self):
    # escape the last module which is system itself
    for mod_id in PROCESS_FN:
      self.start_module(mod_id)

  # terminate all modules
  def terminate_all(self):
    # escape the last module which is system itself
    for mod_id in PROCESS_FN:
      self.terminate_module(mod_id)

  # send message to a module specified by id
  def send_msg(self, mod_id, msg):
    # escape module 'all'
    if mod_id==MODULE.ALL or not self.pipes[mod_id]: return
    # self.queue[mid].put(msg)
    self.pipes[mod_id].send(msg)
    return

  # check if there is data available from pipes
  # process according to module
  def loop(self):
    if self.pipes[MODULE.ASR] and self.pipes[MODULE.ASR].poll():
      # message from ASR are text to SLU
      msg = self.pipes[MODULE.ASR].recv()
      if self.pipes[MODULE.SLU]: self.pipes[MODULE.SLU].send(msg)
    if self.pipes[MODULE.SLU] and self.pipes[MODULE.SLU].poll():
      # message from SLU are actions to TTS or ACT
      # message content is dictionary of format: { 'mod':'tts'/'act', 'data':'content' }
      msg = self.pipes[MODULE.SLU].recv()
      mod_id = self.mod2id[msg['mod']]
      if self.pipes[mod_id]: self.pipes[mod_id].send(msg['data'])
    # currently there's no data from TTS and ACT process, but later maybe
    # if self.pipes[TTS].poll(): pass
    # if self.pipes[ACT].poll(): pass
    time.sleep(0.01)

  # handle commands from controller
  def handle(self, command):
    # high priority command
    if command == 'exit':
      self.terminate_all()
      return False
    # extract module, command, message
    tmp = command.split(':')
    for _ in xrange(len(tmp),3): tmp.append(None)
    mod,cmd,msg = tmp[0],tmp[1],tmp[2]
    # check module validity
    if mod not in self.mod2id:
      print_debug('manager | unable to recognize module: %s\n' % command)
      return True
    else: mod = self.mod2id[mod]
    # map command into function
    if cmd=='start':
      self.start_module(mod)
    elif cmd=='exit':
      self.terminate_module(mod)
    elif cmd=='msg':
      if not msg: print_debug('manager | empty message: %s\n' % command)
      else: self.send_msg(mod,msg)
    else:
      print_debug('manager | unrecognized command: %s\n' % command)
    return True


# main function of the dialog manager process
def dm_process(pipe):
  # initialize dialog manager
  dm = DialogManager()
  print '=> dialog manager started'
  # main loop
  while True:
    if pipe.poll():
      cmd = pipe.recv()
      print_debug('controller | %s\n' % cmd)
      ret = dm.handle(cmd)
      if not ret: break
    dm.loop()
  pipe.close()
  print '=> dialog manager closed'
  return

if __name__ == '__main__':
  pass
