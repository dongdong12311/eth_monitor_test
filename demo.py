import okex.account_api as account
import okex.ett_api as ett
import okex.futures_api as future
import okex.lever_api as lever
import okex.spot_api as spot
import okex.swap_api as swap
import json,sys
import traceback

api_key ='50efe898-4ee3-4f7e-bc5a-05e6b955f441'
seceret_key = '44CB9460F6FB6C906D647390AB650E55'
passphrase = 'Take_order_API'  

class Account(object):
    def __init__(self,futureapi):
        self.futureAPI = futureapi
    def get_accountss(self,name):
        "获取币种的持仓数据"
        try:    
            return self.futureAPI.get_accounts()['info'][name]['contracts'][0]['available_qty']
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print("*** print_tb:")
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
    def buy(self,amount):
        pass 
class ETHAccount(Account):
    def __inti__(self,futureapi):
        self.name = "ETH"
        super().__init__(futureapi)
    def get_account(self,name):
        return self.get_accountss(name)
    
    def buy(self,price,amount):
        "买入开仓"
        pass
    def sell(self,price,amount):
        "卖出开仓"
        pass
"获取可用数量"
futureAPI = future.FutureAPI(api_key, seceret_key, passphrase, True)
a = futureAPI.get_accounts()['info']['eth']['contracts'][0]['available_qty']

"测试下单"

client_oid = 'ccbce5bb7f7344288f32585cd3adf357'
instrument_id = 'ETH-USD-181228'
"otype	String	是	1:开多2:开空3:平多4:平空"
otype = str(2)
price = str(2)
size = str(1)

"match_price	String	否	是否以对手价下单(0:不是 1:是)，默认为0，当取值为1时。price字段无效"
match_price  = str(1)

"leverage	Number	是	要设定的杠杆倍数，10或20"
leverage = str(10)
"买入开仓"
while 1:
    try:        
        instrument_id = 'ETH-USD-190329'
        result = futureAPI.take_order(client_oid, instrument_id, otype, price, size, match_price, leverage)
    except  Exception as e:
        pass
