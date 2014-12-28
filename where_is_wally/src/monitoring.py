
from enum       import Enum
from pydispatch import dispatcher

import time


# Proximity threshold
prox_threshold = 40


class Signal(Enum): 

      Proximity = 'PROXIMITY'
      Collision = 'COLLISION'
      Done      = 'DONE'


def monitor_distance(sniffer,threshold=prox_threshold,pause=0.01):

    while True: 
        try:
          if sniffer.ultrasonic.get_sample() < threshold: 
             dispatcher.send(signal=Signal.Proximity,sender='monitoring.monitor_distance')
          if sniffer.touch.get_sample() == 1:
             dispatcher.send(signal=Signal.Collision,sender='monitoring.monitor_distance')
          time.sleep(pause)
        except Exception, e:
          print '[monitor_distance] Exception: ' + str(e)

def monitor_key_strokes():
    # TODO use Tkinter?
    # dispatcher.send(signal=raw_input('Press any key to abort.'),sender='monitoring.monitor_key_strokes')
    pass


## Logging

def log_events():
    dispatcher.connect(show,signal=dispatcher.Any,sender=dispatcher.Any)

def show(signal,sender):
    print signal + '! from ' + sender + ' (' + str(time()) + ')'
