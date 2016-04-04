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
from tools.print_debug import print_debug


NUM_MODULES = 5
ASR,SLU,TTS,ACT,ALL = tuple(range(NUM_MODULES))
PROCESS_FN = (asr_process,slu_process,tts_process,act_process)

class DialogManager(object):
  def __init__(self):
    self.processes = [None]*(NUM_MODULES-1) # escape module 'all'
    self.pipes = [None]*(NUM_MODULES-1) # escape module 'all'
    self.mod2id = {'asr':ASR, 'slu':SLU, 'tts':TTS, 'act':ACT, 'all':ALL}
    self.id2mod = {ASR:'asr', SLU:'slu', TTS:'tts', ACT:'act', ALL:'all'}
    return

  # start module with module id
  def start_module(self, mod_id):
    if mod_id == ALL:
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
    if mod_id==ALL:
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
    for mod_id in xrange(NUM_MODULES-1):
      self.start_module(mod_id)

  # terminate all modules
  def terminate_all(self):
    # escape the last module which is system itself
    for mod_id in xrange(NUM_MODULES-1):
      self.terminate_module(mod_id)

  # send message to a module specified by id
  def send_msg(self, mod_id, msg):
    # escape module 'all'
    if mod_id==ALL or not self.pipes[mod_id]: return
    # self.queue[mid].put(msg)
    self.pipes[mod_id].send(msg)
    return

  # check if there is data available from pipes
  # process according to module
  def loop(self):
    if self.pipes[ASR] and self.pipes[ASR].poll():
      # message from ASR are text to SLU
      msg = self.pipes[ASR].recv()
      if self.pipes[SLU]: self.pipes[SLU].send(msg)
    if self.pipes[SLU] and self.pipes[SLU].poll():
      # message from SLU are actions to TTS or ACT
      # message content is dictionary of format: { 'mod':'tts'/'act', 'data':'content' }
      msg = self.pipes[SLU].recv()
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
