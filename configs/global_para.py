#!/usr/bin/python
#
# created by Ray on 2016-04-04
#
# Definition of global parameters.
#

import os,sys

ROOT_PATH = os.path.dirname(sys.argv[0])
TMP_PATH = ROOT_PATH+'/tmp/'
CONFIG_PATH = ROOT_PATH+'/configs/'

NAMED_PIPE = TMP_PATH+'named_pipe.fifo'

ASR_OUTPUT_WAVE = TMP_PATH+'asr.wav'
TTS_OUTPUT_WAVE = TMP_PATH+'tts.wav'

API_AI_CREDENTIAL = CONFIG_PATH+'credential.json'

TTS_URL = 'https://api.api.ai/v1/tts?v=20150910'
