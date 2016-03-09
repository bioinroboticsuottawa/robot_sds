# Project: Spoken Dialog System for Robots
# Date Created: 06/03/2016
# Author: Ray Shen
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import requests
import json
from requests.auth import HTTPBasicAuth as Auth


class WatsonDlg:
  def __init__(self):
    # declaration
    self.base_url = None
    self.username = None
    self.password = None
    self.conversation_id = None
    self.client_id = None
    self.dlg_name = None
    self.dialog_url = None
    self.conversation_url = None
    self.auth = None
    self.dialogs = {}
    # configuration
    self.credential_file = '../configs/credential.json'
    self.configure_file = '../configs/dialog.json'
    self.configure()

  def configure(self):
    with open(self.credential_file) as fin:
      data = json.load(fin)
      self.base_url = data['credentials']['url']
      self.username = data['credentials']['username']
      self.password = data['credentials']['password']
    self.auth = Auth(self.username, self.password)
    self.dialog_url = self.base_url+'/dialogs'
    self.list_dialogs()
    with open(self.configure_file) as fin:
      data = json.load(fin)
      self.dlg_name = data['dlg_name']
    self.conversation_url = self.dialog_url+'/'+self.dialogs[self.dlg_name]+'/conversation'

  def list_dialogs(self):
    resp = requests.get(self.dialog_url, auth=self.auth)
    # self.print_resp(resp)
    data = resp.json()
    for dlg in data['dialogs']:
      self.dialogs[dlg['name']] = dlg['dialog_id']
    # print self.dialogs

  def converse(self, sen):
    if not sen: return
    if not self.conversation_id: para = { 'input': sen }
    else: para = {'conversation_id':self.conversation_id, 'client_id':self.client_id, 'input':sen}
    resp = requests.post(self.conversation_url, data = para, auth = self.auth)
    # self.print_resp(resp)
    data = resp.json()
    if not self.conversation_id:
      self.conversation_id = data['conversation_id']
      self.client_id = data['client_id']
    # print non-empty response sentences
    print '=> watson:'
    for rep in data['response']:
      if rep: print rep

  @staticmethod
  def print_resp(resp):
    print '----'
    print resp.status_code
    print resp.headers['content-type']
    print resp.encoding
    print resp.text
    if resp.headers['content-type']=='application/json':
      print resp.json()
    print '----'


if __name__ == '__main__':
  wdlg = WatsonDlg()
  wdlg.converse('hi hello')
  sent = raw_input("=> input:\n")
  while sent!='exit':
    wdlg.converse(sent.strip())
    sent = raw_input("=> input:\n")

