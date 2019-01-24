# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 14:44:58 2019

@author: Administrator
"""
from  dateutil.parser import parse
import datetime
import pytz
class TimeCal:
    def __init__(self,timestamp):
        self.__timestamp = parse(timestamp)
        

    def relativetime(self):
        "相对于现在的时间"
        temp = datetime.datetime.utcnow().replace(tzinfo=pytz.timezone('UTC')) - self.__timestamp        
        return temp.total_seconds()