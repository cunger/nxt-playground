#!/usr/bin/env python

from time       import sleep
from pydispatch import dispatcher
from nxt.sensor import *
from signaling  import *


class Sniffer(object):
    'Object for collecting data samples and monitoring sensor output'

    def __init__(self,brick):
        
        # Brick
        self.brick = brick

        # Sensors 
        self.touch       = Touch(brick,PORT_2)
        self.ultrasonic  = Ultrasonic(brick,PORT_4)
        self.color       = Color20(brick,PORT_3)
        self.light       = Light(brick,PORT_3,False)        
        self.light.set_illuminated(False)
        #self.color.set_light_color(COLORNONE)

        # Profile
        self.samples = []


    ## Collect 

    def get_distance(self):
        try: 
            return self.ultrasonic.get_sample()
        except: 
            return 0

    def get_color(self):
        try:
            return self.color.get_sample()
        except: 
            return 0

    ## Store 

    def store_profiles(self,room='unknown'):
        open('../target/'+room+'.profile','w').write(str(self.samples))

    ## Analyse 

    def analyse_sample(self,sample):
        # TODO additional input: trained model
        print 'Not implemented yet!'
