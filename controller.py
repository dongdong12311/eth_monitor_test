    # -*- coding: utf-8 -*-
"""
Created on Sun Jan 20 13:34:01 2019

@author: dongdong
"""
from event import RiskEvent
from event import SignalEvent

class controller:
    def __init__(self,events):
        self.events = events
        
class Risk_controller(controller):
    
    def __init__(self,events):
        super().__init__(events)
        
    def monitor(self):
        self.events.put(RiskEvent('CLOSE',1,1,1))
        
        
class Signal_controller(controller):
    def __init__(self,events):
        super().__init__(events)
    def monitor(self):
        self.events.put(SignalEvent('SIGNAL',1,1,1))
    

        
        