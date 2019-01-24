    # -*- coding: utf-8 -*-
"""
Created on Sun Jan 20 13:34:01 2019

@author: dongdong
"""
from event import Cancel_Order_Event
from event import SignalEvent
from api.okex_api import Market_info_API
from account import Account
market_infor_api = Market_info_API()
class controller:
    def __init__(self,events):
        self.events = events
        
class Cancel_Order_controller(controller):
    
    def __init__(self,events):
        super().__init__(events)
        
    def monitor(self):
        orders  = market_infor_api.get_market_orders()
        for order in orders:
            print(order.order_time_relative())
            if order.order_time_relative() > 2:
                "订单时间超过两秒钟"
                self.events.put(Cancel_Order_Event('CANCEL',order.orderid))
        
class Risk_controller(controller):
    #风控模块
    def __init__(self,events):
        super().__init__(events)
        self.account =  Account()
    def monitor(self):
        positions = self.account.get_positions()
        for position in positions:
            print(position.ratio)
            if abs(position.ratio) > 0.8 and position.size > 0 :
                "如果收益超过+-10%"
                #	1:开多2:开空3:平多4:平空 
                size = position.size 
                if position.otype == 1:
                    price = position.best_ask - 0.001
                    otype = '3'
                elif position.otype == 2:
                    "空头平仓  获取最优买价"
                    price  = position.best_bid+ 0.001
                    otype = '4'
                else:
                    raise TypeError
                self.events.put(SignalEvent('TAKE_ORDER',price,size,otype))
    

        
class Signal_controller(controller):
    def __init__(self,events):
        super().__init__(events)
    def monitor(self):
        size = '10'
        losers = market_infor_api.NewLosers()
        for loser in losers:  
            if float(loser.size) < 10:
                continue
            #	1:开多2:开空3:平多4:平空 
            if loser.otype == 4:
                #如果是多头空仓 就开空仓
                price = str(loser.price * 0.99)
                otype = '2'
            elif loser.otype == 3:
                price = str(loser.price * 1.01)
                otype = '1'
            self.events.put(SignalEvent('TAKE_ORDER',price,size,otype))
                
        