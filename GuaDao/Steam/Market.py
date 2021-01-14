import json
import re
import time
import urllib

import requests

from . import Cache, SteamRequestsSession, Utils
from .Constants import SteamUrl
from .MarketCollections import ItemOrder, ItemPriceOverview, ItemPriceHistory


class Market:

    def __init__(self):
        self.session = SteamRequestsSession.SteamRequestsSession()

    @Cache.cacheFunc(60*60)
    def getItemPage(self, appid, market_hash_name):
        router = f'/market/listings/{appid}/{market_hash_name}'
        return self.session.get(SteamUrl.Community + router).text

    @Cache.cacheFunc(-1)
    def getNameidByHashName(self, appid, market_hash_name):
        rsp = self.getItemPage(appid, market_hash_name)

        res =  re.search(r'(Market_LoadOrderSpread\( )(.*?)( \))',rsp)

        if res != None:
            return res[2]
        else:
            raise Exception(f'Fail To Get Nameid')
    
    @Cache.cacheFunc(60*60)
    def getItemPriceHistory(self, appid, market_hash_name):
        text = self.getItemPage(appid, market_hash_name)

        lst_string = re.search(r'=(\[\[.*?\]\])',text)
        
        if lst_string == None:
            #raise Exception('Fail To Get Item Price History')
            return ItemPriceHistory('[]')
        else:
            return ItemPriceHistory(lst_string[1])
    
    
    
    @Cache.cacheFunc(30*60)
    def getItemOrder(self,item_nameid, country='CN', language='schinese', currency=23, two_factor=0):
        params = {
            'item_nameid':item_nameid,
            'country':country,
            'language':language,
            'currency':currency,
            'two_factor':two_factor
        }

        rsp = self.session.get(SteamUrl.Community + '/market/itemordershistogram', params=params)

        return ItemOrder.parseResponseText(rsp.text)
    
    @Cache.cacheFunc(30*60)
    def getItemPriceOverview(self,appid,market_hash_name,country='CN',currency='23'):
        params = {
            'appid':appid,
            'country':country,
            'currency':currency,
            'market_hash_name':market_hash_name
        }

        rsp = self.session.get(SteamUrl.Community + '/market/priceoverview/', params=params)

        return ItemPriceOverview.parseResponseText(rsp.text)

if __name__ == "__main__":
    pass
