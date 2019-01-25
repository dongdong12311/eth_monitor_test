# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 21:18:29 2019

@author: Administrator
"""
import okex.account_api as account
import okex.ett_api as ett
import okex.futures_api as future
import okex.lever_api as lever
import okex.spot_api as spot
import okex.swap_api as swap
from param import Instrument_id,BEISHU
from Logger import Log
import requests
from order import Order
from loser import Loser
import datetime
from  dateutil.parser import parse
import dbm
class Market_info_API:
    def __init__(self):
        self.instrument_id = Instrument_id
        api_key = 'cc94168a-060d-409c-81b5-bbb3e329bf15'
        seceret_key = '5F21098F1D113AA02A00FFDEF31761A2'
        passphrase = 'Market_info_API'
        self.futureAPI = future.FutureAPI(api_key, seceret_key,passphrase, True)  
        self.log = Log("Market_info_API.txt")
        db = dbm.open(self.instrument_id, 'c')
        if b'latest' not in db.keys():
            db['latest'] = '2019-01-22T19:00:21.000Z'
        db.close()
    def GetLoser(self):
        "获取最新的爆仓订单   "
        try:
            get = requests.get('https://www.okex.me/api/futures/v3/instruments/'+self.instrument_id+'/liquidation?status=1&from=1&limit=50')
        except:
            self.log.write("获取爆仓单失败")
            return []
        return  get.json()
    def GetDepth(self,depth = 2):
        "获取市场深度数据 返回字典 list"
        result={}
        result['order_info'] = []
        try:
            result = self.futureAPI.get_depth(self.instrument_id,depth)
        except:
            self.log.write("无法获取市场数据")
        return result   
    

    
    def best_ask(self,defaultprice):
        try:
            return self.GetDepth()['asks'][0][0]
        except:
            return defaultprice
    def best_bid(self,defaultprice):
        try:
            return self.GetDepth()['bids'][0][0]
        except:
            return defaultprice
    def get_market_orders(self):
        "获取没有成交的订单"
        results = self.__get_my_order_list()
        orders = []
        for result in results['order_info']:
            "order_id,price,timestamp,ordertype):"
            order = Order(result['order_id'],result['price'],result['timestamp'],result['type'])
            orders.append(order)
        return orders
    def __get_my_order_list(self):
        #获取没有成交的订单
        results = {}
        results['order_info'] = []
        try:
            results = self.futureAPI.get_order_list(0,1,2,50,self.instrument_id)
        except:
            self.log.write("获取未成交订单失败")
        return results
    def get_local_loser_time(self):
        db = dbm.open(self.instrument_id, 'c')
        losertime =  db['latest']
        db.close()
        return losertime  #返回str
    def update_loser_time(self,time):
        db = dbm.open(self.instrument_id, 'c')
        db['latest'] = time
        db.close()        
    def NewLosers(self):
        losers = []
        lastloser_time = parse(self.get_local_loser_time())
        "获取最新的爆仓订单"
        potential_losers = self.GetLoser()
        s=''
        for i in range(len(potential_losers)-1,-1,-1):            
            losetime =  parse(potential_losers[i]['created_at'])
            if  losetime > lastloser_time:
                "如果爆仓订单的时间比现在的新"
                price = float(potential_losers[i]['price'])
                losers.append(Loser(losetime,price,potential_losers[i]['size'],potential_losers[i]['type']))
                
                s+="新增爆仓订单:\n爆仓价格：%.2f\n爆仓方向：%s\n爆仓时间:%s\n"%(price,potential_losers[i]['type'],potential_losers[i]['created_at'])
                self.log.write(s)
                self.update_loser_time(potential_losers[i]['created_at'])
        return losers

    
class Position_info_API:
    def __init__(self):
        self.instrument_id = Instrument_id
        api_key = 'a81e9a56-6cc0-4f7a-a146-a9fc590b3d63'
        seceret_key = '5C59BB0410BE0989D3C8861E00CD70BF'
        passphrase = 'Position_info_API'  
        self.futureAPI = future.FutureAPI(api_key, seceret_key,passphrase, True)  
        self.log = Log("Position_info_API.txt")    
    def get_positions(self):
        #获取持仓数据
        try:
            results = self.futureAPI.get_specific_position(self.instrument_id) 
        except:
            self.log.write("获取持仓数据失败")
            return None 
        return results
    def GetDepth(self,depth = 2):
        "获取市场深度数据 返回字典 list"
        result={}
        result['order_info'] = []
        try:
            result = self.futureAPI.get_depth(self.instrument_id,depth)
        except:
            self.log.write("无法获取市场数据")
        return result   
    

    
    def best_ask(self,defaultprice):
        try:
            return self.GetDepth()['asks'][0][0]
        except:
            return defaultprice
    def best_bid(self,defaultprice):
        try:
            return self.GetDepth()['bids'][0][0]
        except:
            return defaultprice

class Take_order_API:
    def __init__(self):
        self.instrument_id = Instrument_id
        self.beishu = BEISHU
        api_key = '50efe898-4ee3-4f7e-bc5a-05e6b955f441'
        seceret_key = '44CB9460F6FB6C906D647390AB650E55'
        passphrase = 'Take_order_API'  
        self.futureAPI = future.FutureAPI(api_key, seceret_key,passphrase, True)  
        self.log = Log("Take_order_API.txt")
        
    def takeOrder(self,price,size,otype):
        "开仓"
        "match_price	String	否	是否以对手价下单(0:不是 1:是)，默认为0，当取值为1时。price字段无效"
        "leverage	Number	是	要设定的杠杆倍数，10或20"
        try:
            self.futureAPI.take_order("ccbce5bb7f7344288f32585cd3adf357", self.instrument_id,otype, price, size, '0', str(self.beishu))     
        except :
            self.log.write("otype=%s交易失败"%otype)
    def cancel_order(self,orderid):
        "撤单"
        try:
            self.futureAPI.revoke_order(self.instrument_id,orderid)
        except:
            self.log.write("撤单失败")
            return False
        return True