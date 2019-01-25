# -*- coding: utf-8 -*-
"""
Created on Sun Jan 20 13:13:46 2019

@author: dongdong
执行模块
"""

import zmq
import time
from Logger import Log
import sys
from param import Cancel_Order_Port ,Signal_Port,Risk_controller_Port
import threading
from api.okex_api import Take_order_API


# 执行模块日志
excution_log = Log("excution_log.txt")
take_order_api = Take_order_API()
def process(messages):
    '''
    message = {"type":"CANCEL","price":str,"size":str,"otype":str,orderid:str}:
    TAKE_ORDER:交易
    "CANCEL":撤单    
    '''
    for message in messages:        
        if message.type == 'CANCEL':
            take_order_api.cancel_order(message.orderid)
        elif message.type == 'TAKE_ORDER': 
            take_order_api.takeOrder(message.price,message.size,message.otype)
        excution_log.write(str(message))




def main():
    
    
    
    #  Socket to talk to server
    context = zmq.Context()
    # Initialize poll set
    poller = zmq.Poller()

    sockets = {'signal_socket':{"socket":context.socket(zmq.SUB),"port":Signal_Port},
           'cancel_order_socket'  :{"socket":context.socket(zmq.SUB),"port":Cancel_Order_Port},
           'risk_socket':{"socket":context.socket(zmq.SUB),"port":Risk_controller_Port}}
    
    
    # 接收交易信号 
    for socket in sockets.values():
        socket["socket"].connect("tcp://localhost:"+socket["port"])
        # 默认接收所有的信号
        socket["socket"].setsockopt_string(zmq.SUBSCRIBE,"")
        poller.register(socket["socket"], zmq.POLLIN)
    while 1:    
        try:
            socks = dict(poller.poll())
        except KeyboardInterrupt:
            break
        thread_list = []
        for socket in socks:
            message = socket.recv_pyobj()
            mytread = threading.Thread(target=process, args=(message,))
            mytread.start()
            thread_list.append(mytread)
        for t in thread_list:
            if t.is_alive():
                t.join()            

main()
