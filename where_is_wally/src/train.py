#!/usr/bin/env python

import nxt.bluesock
import time 

from speaking   import Voice 
from signaling  import log_events
from controller import Controller
from motors     import Direction

brick = nxt.bluesock.BlueSock('00:16:53:0C:86:B5').connect()

# voice   = Voice()

# voice.say('Hallo!')


controller = Controller(brick)
controller.test()

raw_input('Test finished. Press any key to continue.')

log_events()

try: 
    controller.explore()
except Exception,e:
    print 'Exception: ' + str(e) 
    controller.abort()

