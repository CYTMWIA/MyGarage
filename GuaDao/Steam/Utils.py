import re
import urllib
import functools
import time

import requests

encodeQueryString = functools.partial(urllib.parse.urlencode,quote_via=urllib.parse.quote)

def parsePriceText(text):
    return float(re.search(r'\d+\.?\d*',text.replace(',',''))[0])

def parseQueryString(qs):
    return {pair[0]:pair[1] for pair in urllib.parse.parse_qsl(qs)}

def getMaskedRequestsSession():
    s = requests.session()
    s.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'
    })
    return s

def lower_bound(lst, value, key=lambda x:x):
    # just like 'lower_bound' in c++
    l, r = 0, len(lst)
    while l<r:
        mid = (l+r)//2
        #print(l,mid,r)
        if key(lst[mid]) < value:
            l = mid+1
        else:
            r = mid
    return l

if __name__ == "__main__":
    pass