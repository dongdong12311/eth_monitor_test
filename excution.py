# -*- coding: utf-8 -*-
"""
Created on Sun Jan 20 13:13:46 2019

@author: dongdong
执行模块
"""

import zmq
import time
from Logger import Log
# Prepare our context and sockets
import sys
from param import Risk_Port ,Signal_Port
# 执行模块日志
excution_log = Log("excution_log.txt")

#  Socket to talk to server
context = zmq.Context()

sockets = {'signal_socket':context.socket(zmq.SUB),
       'risk_socket'  :context.socket(zmq.SUB)}
# 接收交易信号 
sockets['signal_socket'].connect("tcp://localhost:"+Signal_Port)
# 接收策略信号
sockets['risk_socket'].connect("tcp://localhost:"+Risk_Port)
# Initialize poll set
poller = zmq.Poller()
for sockets in sockets.values():
    # 默认接收所有的信号
    sockets.setsockopt_string(zmq.SUBSCRIBE,"")
    poller.register(sockets, zmq.POLLIN)

import threading


def process(message):
    print(message)
    excution_log.write(str(message))
if __name__ == '__main__':
    while 1:    
        try:
            socks = dict(poller.poll())
        except KeyboardInterrupt:
            break
        thread_list = []
        for socket in socks:
            message = socket.recv_json()
            mytread = threading.Thread(target=process, args=(message,))
            mytread.start()
            thread_list.append(mytread)
        for t in thread_list:
            if t.is_alive():
                t.join()            


