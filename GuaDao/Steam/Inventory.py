from . import SteamRequestsSession
from .Constants import SteamUrl

class Inventory:
    def __init__(self):
        self.session = SteamRequestsSession.SteamRequestsSession()
    
    def getInventory(self, appid, inventory_code, user_id64=None, language='schinese'):
        params = {
            'l':language,
            'count':5000
        }
        self.session.get(SteamUrl.Community+f'/inventory/{user_id64}/{appid}/{inventory_code}',params=params)
        pass

    def getGooValue(self):
        pass