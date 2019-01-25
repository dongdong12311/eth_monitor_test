# -*- coding: utf-8 -*-
"""
Created on Sun Jan 20 13:35:49 2019

@author: dongdong
"""

class Event:
    def __init__(self):
        pass
    
class Cancel_Order_Event(Event):
    def __init__(self,eventtype,orderid):
        self.type = eventtype
        self.orderid = orderid
    def __str__(self):
        s= {"type":self.type,"orderid":self.orderid}
        return str(s)
        
class SignalEvent(Event):
    def __init__(self,eventtype,price,size,otype):
        """eventtype:"type",price":str,"size":str,"otype":str}:"""
        self.type = eventtype
        self.price = price
        self.size = size
        self.otype = otype
    def __str__(self):
        
        s =  {"type":self.type,"price":self.price,"size":self.size,"otype":self.otype}
        return str(s)
        