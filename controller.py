    # -*- coding: utf-8 -*-
"""
Created on Sun Jan 20 13:34:01 2019

@author: dongdong
"""
from event import RiskEvent
from event import SignalEvent
from okex_api import Market_info_API

market_infor_api = Market_info_API()
class controller:
    def __init__(self,events):
        self.events = events
        
class Risk_controller(controller):
    
    def __init__(self,events):
        super().__init__(events)
        
    def monitor(self):
        orders  = market_infor_api.get_market_orders()
        for order in orders:
            print(order.order_time_relative())
            if order.order_time_relative() > 2:
                "订单时间超过两秒钟"
                self.events.put(RiskEvent('CANCEL',order.orderid))
        
        
class Signal_controller(controller):
    def __init__(self,events):
        super().__init__(events)
    def monitor(self):
        """eventtype:type,price":str,"size":str,"otype":str}:"""
        "平仓 type	String	是	1:开多2:开空3:平多4:平空 "
        self.events.put(SignalEvent('TAKE_ORDER','100','1','1'))
        self.events.put(SignalEvent('TAKE_ORDER','130','1','2'))

        
        