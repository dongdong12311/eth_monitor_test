# -*- coding: utf-8 -*-
"""
Created on Sun Jan 20 13:35:49 2019

@author: dongdong
"""

class Event:
    def __init__(self):
        pass
    
class RiskEvent(Event):
    def __init__(self,eventtype,orderid):
        self.type = eventtype
        self.orderid = orderid
    def dic(self):
        return {"type":self.type,"orderid":self.orderid}
        
        
class SignalEvent(Event):
    def __init__(self,eventtype,price,size,otype):
        """eventtype:"type",price":str,"size":str,"otype":str}:"""
        self.type = eventtype
        self.price = price
        self.size = size
        self.otype = otype
    def dic(self):
        return {"type":self.type,"price":self.price,"size":self.size,"otype":self.otype}
    
        