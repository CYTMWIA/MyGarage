import json
import time

import requests

from . import Utils
from . import Item3rd
    
class Buff:
    session = Utils.getMaskedRequestsSession()

    def __init__(self,buff_session):
        self.session.cookies.update({
            'session':buff_session
        })

    def _parseResponseText(self,text):
        jsn = json.loads(text)

        res = []
        for item in jsn['data']['items']:
            bi = Item3rd.Item3rd()

            bi.lowest_sell_price = float(item['sell_min_price'])
            #bi.sell_orders_amount = int(item['sell_num'])
            #bi.highest_buy_price = float(item['buy_max_price'])
            #bi.buy_orders_amount = int(item['buy_num'])

            bi.appid = str(item['appid'])
            bi.market_hash_name = str(item['market_hash_name'])

            bi.market3rd = 'buff'
            bi.name_in_market3rd = item['name']
            bi.url3rd = 'https://buff.163.com/market/goods?goods_id='+str(item['id'])    

            res.append(bi)
        
        return res

    def walkItems(self,query_string):
        params = Utils.parseQueryString(query_string.replace('#','&'))

        if 'page_num' not in params.keys():
            params['page_num'] = 0
        else:
            params['page_num'] = int(params['page_num'])-1
            
        while True:
            params['_'] = int(time.time()*1000)
            params['page_num'] += 1

            rsp = self.session.get('https://buff.163.com/api/market/goods?', params=params)

            items = self._parseResponseText(rsp.text)

            for i in items:
                yield i
            
            if len(items)<20:
                break
