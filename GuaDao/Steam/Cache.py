import time
import functools

class CachePool:
    '''
    cache = {
        'key': {
            'data': ...,
            'time': float,
        }
    }
    '''
    expire_time = -1 # seconds

    def __init__(self):
        self.cache = {}

    def isCached(self,key):
        return key in self.cache
    
    def isExpired(self,key):
        return self.expire_time<0 or time.time() <= self.cache[key]['time']+self.expire_time
    
    def isOk(self,key):
        return self.isCached(key) and self.isExpired(key)
    
    def cacheData(self,key,obj):
        self.cache[key] = {
            'data': obj,
            'time': time.time()
        }

        return self.cache[key]['data']
    
    def getCache(self, key):
        assert self.isCached(key)

        return self.cache[key]['data']

class CacheFunc:
    def __init__(self, func_main=None, func_key=None):
        #print('init')
        self.cache_pool = CachePool()
        self._func_main = func_main
        if func_key == None:
            self._func_key = lambda *args, **kwargs: f'{args};{[(k, kwargs[k]) for k in sorted(kwargs.keys())]}'
    
    def __get__(self,obj,objtype=None):
        def wraper(*args,**kwargs):
            key = self._func_key(obj, *args,**kwargs)
            if self.cache_pool.isOk(key):
                return self.cache_pool.getCache(key)
            else:
                res = self._func_main(obj, *args,**kwargs)
                self.cache_pool.cacheData(key, res)
                return res
        return wraper

    def cache_key(self,func_key):
        return type(self)(self._func_main, func_key)

def cacheFunc(expire_time):
    def dec(func):
        cf = CacheFunc(func)
        cf.cache_pool.expire_time = expire_time
        #print(cf)
        return cf
    return dec

if __name__ == "__main__":
    pass