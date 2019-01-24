# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 12:15:58 2019

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
class Order:
    "委托订单"
    def __init__(self,orderid,price,timestamp,ordertype):
        self.price = price
        self.timestamp = TimeCal(timestamp)
        self.orderid = orderid
        self.ordertype = ordertype
        
    
    def order_time_relative(self):
        "获取订单相对现在没有成交的时间 单位是秒"
        return self.timestamp.relativetime()