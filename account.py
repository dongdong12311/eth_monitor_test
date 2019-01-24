# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 16:35:07 2019

@author: Administrator
"""
from param import BEISHU
from api.okex_api import Position_info_API 
class Position:
    def __init__(self,price,ratio,size,otype,best_ask,best_bid):
        self.price = price
        self.ratio = ratio
        self.size = int(size)
        self.otype = otype
        self.best_ask = float(best_ask)
        self.bset_bid = float(best_bid)
        
class Account:
    def __init__(self):
        self.position_info_api  = Position_info_API()
    
    def get_positions(self):
        positions = []
        results = self.position_info_api.get_positions()
        if results is None or len(results['holding']) == 0:
            return positions
        res = results['holding'][0]
        bestbid = self.position_info_api.best_bid(float(res['long_avg_cost']))
        bestask = self.position_info_api.best_bid(float(res['short_avg_cost']))
        if res['long_qty'] != '0':
            "持有多头"
            
            price = float(res['long_avg_cost'])
            rate = (bestbid-price)/price*100*BEISHU
            #"(self,price,ratio,size,otype,best_ask,best_bid)"
            positions.append(Position(price,rate,res['long_avail_qty'],1,bestask,bestbid))
        if res['short_qty'] != '0':
            "持有空头"

            price = float(res['short_avg_cost'])
            rate = -(bestask-price)/price*100*BEISHU
            positions.append(Position(price,rate,res['short_avail_qty'],2,bestask,bestbid))
                
            
        return  positions