#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path, sys

try:
    import apiai
except ImportError:
    sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
    import apiai

CLIENT_ACCESS_TOKEN = '9c52fe4976ef4f069a450919edd6356a'
SUBSCRIPTION_KEY = '24391266-d12e-4f62-bb85-c1118fe4e6c2' 

def main():
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN, SUBSCRIPTION_KEY)

    request = ai.text_request()

    request.lang = 'en' # optional, default value equal 'en'

    request.query = "how is the weather in Vancouver"

    response = request.getresponse()

    print (response.read())

if __name__ == '__main__':
    main()
