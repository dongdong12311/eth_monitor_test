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
from controller import Risk_controller
from controller import Signal_controller
from Logger import Log
from param import Risk_Port ,Signal_Port
import json
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
            dic = {'type':event.type,'tradeside':event.tradeside,
                   'price':event.price,
                   'amount':event.amount}
            mylog.write(json.dumps(dic))
            socket.send_json(dic)    
        time.sleep(sleeptime)
        
if __name__ == '__main__':
    
    #启动风控进程
    thread1 = threading.Thread(target=Mymonitor, args=(Risk_controller,Risk_Port,1))
    
    #启动信号进程
    thread2 = threading.Thread(target=Mymonitor, args=(Signal_controller,Signal_Port,0.1))
    
    
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
