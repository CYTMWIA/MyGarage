import requests
import time

class SteamRequestsSession(requests.sessions.Session):
    def __init__(self):
        self.last_request_time = 0
        self.request_interval = 10

        super().__init__()
        self.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'
        })
    
    def request(self, *args,**kwargs):
        while time.time()<self.last_request_time+self.request_interval:
            time.sleep(0.001)
        self.last_request_time=time.time()

        rsp = super().request(*args,**kwargs)
        if rsp.status_code == 429:
            raise Exception('Too Many Requests')

        return rsp