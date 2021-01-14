import json
import time
import calendar

from . import Utils

class ItemOrder:
    _sell_orders = []
    _buy_orders = []
    _raw_json = {}

    @property
    def sell_orders(self):
        '''销售单, 按价格升序'''
        return self._sell_orders
    
    @sell_orders.setter
    def sell_orders(self,lst:list):
        self._sell_orders = sorted(lst, key=lambda item: item['price'])
    
    @property
    def buy_orders(self):
        '''订购单, 按价格降序'''
        return self._buy_orders

    @buy_orders.setter
    def buy_orders(self,lst:list):
        self._buy_orders = sorted(lst, key=lambda item: -item['price'])

    @property
    def lowest_sell_price(self):
        return self.sell_orders[0]['price'] if len(self._sell_orders) > 0 else 0
    
    @property
    def highest_buy_price(self):
        return self.buy_orders[0]['price']  if len(self._buy_orders) > 0 else 0

    @staticmethod
    def parseResponseText(text):
        res = ItemOrder()

        res._raw_json = json.loads(text)
        assert res._raw_json['success']

        res.buy_orders = [{'price':o[0],'amount':o[0]} for o in res._raw_json['buy_order_graph']]
        res.sell_orders = [{'price':o[0],'amount':o[0]} for o in res._raw_json['sell_order_graph']]

        return res
    
    def copy(self):
        newone = ItemOrder()

        newone._raw_json = self._raw_json.copy()
        newone._buy_orders = self._buy_orders.copy()
        newone._sell_orders = self._sell_orders.copy()

        return newone
        

class ItemPriceOverview:
    median_sell_price = 0
    lowest_sell_price = 0
    volume_24h = 0
    _raw_json = {}

    @staticmethod
    def parseResponseText(text):
        res = ItemPriceOverview()
        
        res._raw_json = json.loads(text)
        assert res._raw_json['success']

        res.volume_24h = int(res._raw_json['volume'].replace(',','')) if 'volume' in res._raw_json else 0
        res.median_sell_price = Utils.parsePriceText(res._raw_json['median_price']) if 'median_price' in res._raw_json else 0
        res.lowest_sell_price = Utils.parsePriceText(res._raw_json['lowest_price']) if 'lowest_price' in res._raw_json else 0

        return res
    
    def copy(self):
        newone = ItemPriceOverview()

        newone._raw_json = self._raw_json.copy()
        newone.median_sell_price = self.median_sell_price
        newone.lowest_sell_price = self.lowest_sell_price
        newone.volume_24h = self.volume_24h

        return newone

class ItemPriceHistoryPoint:
    def __init__(self, time, median_price, volume):
        self.time = time
        self.median_price = median_price
        self.volume = volume

class ItemPriceHistory:
    def __init__(self, list_string:str):
        self._raw = list_string

        lst = json.loads(list_string)

        self.history = [ItemPriceHistoryPoint(
            calendar.timegm(time.strptime(p[0]+'000','%b %d %Y %H: %z')),
            p[1],
            int(p[2])
        ) for p in lst]
    
    def getVolumeSum(self, begin_time, end_time):
        point_time = lambda point: point.time
        ib = Utils.lower_bound(self.history,begin_time,point_time)
        ie = Utils.lower_bound(self.history,end_time,point_time)
        return sum([p.volume for p in self.history[ib:ie]])
    
    def getVolumeSumInTime(self,in_time):
        t = time.time()
        return self.getVolumeSum(t-in_time,t)
