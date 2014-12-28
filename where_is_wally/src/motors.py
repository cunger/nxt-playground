#!/usr/bin/env python

from pydispatch import dispatcher
from nxt.motor  import *
from signaling  import *

import time


class Direction(Enum):
      Left  = [-100,400]
      Right = [ 100,400]


class Steerer(object):
    'Object for controlling the motors (for driving and turning the head)'

    def __init__(self,brick):

        # Brick
        self.brick = brick

        # Motors
        self.motor_left  = Motor(brick,PORT_C)
        self.motor_right = Motor(brick,PORT_B)
        self.motor_head  = Motor(brick,PORT_A)


    def get_power(self):
        return self.motor_left._get_state().power + self.motor_right._get_state().power
        
    def start(self): 
        self.motor_left.run()
        self.motor_right.run()

    def stop(self):
        self.motor_left.idle()
        self.motor_right.idle()

    def draw_back(self):
        self.motor_left.run(-80)
        self.motor_right.run(-80)
        time.sleep(0.5)
        self.motor_left.idle()
        self.motor_right.idle()

    def turn(self,direction=Direction.Right):
        self.draw_back()
        self.motor_left.turn(direction[0],direction[1])

    def turn_head(self,power=10,degree=140):
        self.motor_head.idle()
        self.motor_head.turn(power,degree)
        self.motor_head.brake()

    def unblock_all(self):
        self.motor_left.idle()
        self.motor_right.idle()
        self.motor_head.idle()

