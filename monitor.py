# -*- coding: utf-8 -*-
"""
Created on Sun Jan 20 21:58:32 2019

@author: dongdong
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Jan 20 13:09:47 2019

@author: dongdong
"""
import threading
import time
import zmq
from queue import Queue
from controller import Cancel_Order_controller,Signal_controller,Risk_controller
from Logger import Log
from param import Cancel_Order_Port ,Signal_Port,Risk_controller_Port
import json
from param import Cancel_Order_sleep_time,Signal_sleep_time,Risk_controller_sleep_time
# Prepare our context and sockets


def Mymonitor(controller_func,port,sleeptime):
    #日志的名称
    filename =  controller_func.__name__ + '.txt'
    mylog = Log(filename)
    
    #端口
    portstr = "tcp://*:"+port
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind(portstr)
    
    events = Queue()  
    
    controller = controller_func(events)    
    while 1:
        controller.monitor()
        while True:
            # 获取待处理的事件，如果队列空就结束循环
            if  events.qsize() == 0:
                break
            else:
                event = events.get(False)
            dic = event.dic()
            mylog.write(str(dic))
            socket.send_json(dic)    
        time.sleep(sleeptime)
        
if __name__ == '__main__':
    threads = []
    #启动订单监控模块
    threads.append(threading.Thread(target=Mymonitor, args=(Cancel_Order_controller,Cancel_Order_Port,Cancel_Order_sleep_time)))    
    #启动信号进程
    threads.append(threading.Thread(target=Mymonitor, args=(Signal_controller,Signal_Port,Signal_sleep_time)))    
    #启动分控监控进程
    threads.append(threading.Thread(target=Mymonitor, args=(Risk_controller, Risk_controller_Port , Risk_controller_sleep_time)))
    
    
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
