# -*- coding: utf-8 -*-
"""
Created on Sun Jan 20 13:35:49 2019

@author: dongdong
"""

class Event:
    def __init__(self):
        pass
    
class RiskEvent(Event):
    def __init__(self,eventtype,tradeside,price,amount):
        self.type = eventtype
        self.price = price
        self.amount = amount
        self.tradeside = tradeside
        
        
        
class SignalEvent(Event):
    def __init__(self,eventtype,tradeside,price,amount):
        self.type = eventtype
        self.price = price
        self.amount = amount
        self.tradeside = tradeside