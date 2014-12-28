
from pydispatch import dispatcher
from motors     import Steerer
from sensors    import Sniffer
from monitoring import *

import thread
import sys
import time


class Controller(object):
    'Object for control flow'

    def __init__(self,brick,target=2):
        
        self.steerer = Steerer(brick) 
        self.sniffer = Sniffer(brick) 

        # target number of samples
        self.enough  = target

        ## init monitoring

        # collision-free driving
        dispatcher.connect(self.steerer.stop,signal=Signal.Proximity,sender=dispatcher.Any)
        dispatcher.connect(self.steerer.stop,signal=Signal.Collision,sender=dispatcher.Any)        
        thread.start_new_thread(monitor_distance,(self.sniffer,))

        # default abort condition
        #dispatcher.connect(self.abort,signal=dispatcher.Any,sender='monitoring.monitor_key_strokes')
        #thread.start_new_thread(monitor_key_strokes,())

    def abort(self):
        self.steerer.stop()
        self.steerer.motor_head.idle()
        self.sniffer.store_profiles()
        sys.exit()


    def explore(self):

        while True: 
            try:    self.drive_until_horizon()
            except: self.steerer.unblock_all() 

    def drive_until_horizon(self):

        # 1. Turn (if necessary)
        if self.sniffer.get_distance() < prox_threshold:
           self.steerer.turn()

        # 2. Drive (until motors are stopped)
        self.steerer.start()
        while True:
              if self.steerer.get_power() == 0: break
              time.sleep(1)

        # 3. Sample
        self.look_around()

    def look_around(self,verbose=True):

        color  = self.sniffer.get_color()
        depthL = []
        depthR = []

        # look left

        for i in 3 * [90]:
            self.steerer.turn_head(power=15,degree=i)
            depthL.append(self.sniffer.get_distance())
        
        self.steerer.turn_head(power=-15,degree=160)

        # look right

        for i in 3 * [70]:
            self.steerer.turn_head(power=-15,degree=i)
            depthR.append(self.sniffer.get_distance())

        self.steerer.turn_head(power=15,degree=140)

        # store sample 

        sample = (color,depthL,depthR)
        self.sniffer.samples.append(sample)

        if verbose: print 'Collected sample: ' + str(sample)
        print '(' + str(len(self.sniffer.samples)) + ' of ' + str(self.enough) + ')'

        # custom abort condition
        if len(self.sniffer.samples) >= self.enough:
           self.abort()


    def test(self):

        print '--------------- TEST ----------------------------'
        print '\nTouch: '
        try: print str(self.sniffer.touch.get_sample())
        except Exception, e: print 'Exception: ' + str(e)
        print '\nColor:'  
        try: print str(self.sniffer.color.get_sample())
        except Exception, e: print 'Exception: ' + str(e)  
        print '\nUltrasonic: ' 
        try: print str(self.sniffer.ultrasonic.get_sample())
        except Exception, e: print 'Exception: ' + str(e) 
        
        print '\nLeft motor: '
        try: print str(self.steerer.motor_left._get_state())
        except Exception, e: print 'Exception: ' + str(e)
        print '\nRight motor: '
        try: print str(self.steerer.motor_right._get_state())
        except Exception, e: print 'Exception: ' + str(e)
        print '\nHead motor: '
        try: print str(self.steerer.motor_head._get_state())
        except Exception, e: print 'Exception: ' + str(e)
        print '--------------------------------------------------'