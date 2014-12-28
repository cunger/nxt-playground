#!/usr/bin/env python

import pyttsx


class Voice(object):
    'Object for talking'

    def __init__(self):
        self.engine = pyttsx.init()
        self.engine.setProperty('rate',100)
 
    def say(self,string):
        self.engine.say(string)
        self.engine.runAndWait()
