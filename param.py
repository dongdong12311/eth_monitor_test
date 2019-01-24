# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 22:24:45 2019

@author: Administrator
"""
#交易信号传递的端口
Signal_Port = "5556"

#撤单信号传递的端口
Cancel_Order_Port = "5557"

#分控信号传递端口
Risk_controller_Port = "5558"

#交易信号更新的时间
Signal_sleep_time = 0.21

#订单监控更新的时间
Cancel_Order_sleep_time = 0.21

#风控监控时间
Risk_controller_sleep_time = 0.21

#交易的品种
Instrument_id = 'ETH-USD-190329'

#杠杆倍数
BEISHU = 10

