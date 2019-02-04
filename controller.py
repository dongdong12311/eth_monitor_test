    # -*- coding: utf-8 -*-
"""
Created on Sun Jan 20 13:34:01 2019

@author: dongdong
"""
from event import Cancel_Order_Event
from event import SignalEvent
from api.okex_api import Market_info_API
from account import Account
from Logger import Log
import zmq
import time
from param import Cancel_Order_sleep_time,Signal_sleep_time,Risk_controller_sleep_time
from param import Cancel_Order_Port ,Signal_Port,Risk_controller_Port

market_infor_api = Market_info_API()
class controller: 
    def __init__(self,port,porttype):


        #端口
        self.portstr = "tcp://*:"+port
        self.context = zmq.Context()
        self.socket = self.context .socket(zmq.PUB)
        self.socket.bind(self.portstr)        
        
class Cancel_Order_controller(controller):
    
    def __init__(self,port,porttype):
        super().__init__(port,porttype)
        self.filename =  self.__class__.__name__ + '.txt'
        self.mylog = Log(self.filename)        
    def monitor(self):
        orders  = market_infor_api.get_market_orders()
        orderlist = []
        for order in orders:
            if order.order_time_relative() > 2:
                "订单时间超过两秒钟"
                orderlist.append(Cancel_Order_Event('CANCEL',order.orderid))
        del orders
        return orderlist
    def run(self):
        while  1:
            orders = self.monitor()            
            self.socket.send_pyobj(orders)   
            time.sleep(Cancel_Order_sleep_time)
            del orders
class Risk_controller(controller):
    #风控模块
    def __init__(self,port,porttype):
        super().__init__(port,porttype)
        self.account =  Account()
        self.filename =  self.__class__.__name__ + '.txt'
        self.mylog = Log(self.filename)
    def monitor(self):
        signals = []
        positions = self.account.get_positions()
        for position in positions:
            if abs(position.ratio) > 8 and position.size > 0 :
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
                signals.append(SignalEvent('TAKE_ORDER',price,size,otype))
        del positions
        return signals
    def run(self):
        while  1:
            signals = self.monitor()            
            self.socket.send_pyobj(signals)
            time.sleep(Risk_controller_sleep_time)    
            del signals

        
class Signal_controller(controller):
    def __init__(self,port,porttype):
        super().__init__(port,porttype)
        self.filename =  self.__class__.__name__ + '.txt'
        self.mylog = Log(self.filename)
    def monitor(self):
        
        size = '10'
        losers = market_infor_api.NewLosers()
        signals = []
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
            signals.append(SignalEvent('TAKE_ORDER',price,size,otype))
        del losers
        return signals
    def run(self):
        while  1:
            signals = self.monitor()  
            self.socket.send_pyobj(signals)   
            time.sleep(Signal_sleep_time) 
            del signals
import threading

def cancel_Order():
    
    cancel_Order_controller =Cancel_Order_controller(Cancel_Order_Port,zmq.PUB)
    cancel_Order_controller.run()
def risk_controller():
    
    risk_controller = Risk_controller(Risk_controller_Port,zmq.PUB)
    risk_controller.run()
def signal_conller():
    
    signal_controller = Signal_controller(Signal_Port,zmq.PUB)
    signal_controller.run()
threads = []
#启动订单监控模块
threads.append(threading.Thread(target=cancel_Order, args=()))    
#启动信号进程
threads.append(threading.Thread(target=risk_controller, args=()))   
#启动分控监控进程
threads.append(threading.Thread(target=signal_conller, args=()))       

for thread in threads:
    thread.start()
for thread in threads:
    thread.join()        