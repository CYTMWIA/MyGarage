import requests
import re
import urllib

def parsePriceText(text):
    return float(re.search(r'\d+\.?\d*',text.replace(',',''))[0])

def parseQueryString(qs):
    return {pair[0]:pair[1] for pair in urllib.parse.parse_qsl(qs)}

def getAppid(game):
    table = {
        'csgo':'730',
        'dota2':'570',
        'steam':'753'
    }
    return table[game.lower()]

def getMaskedRequestsSession():
    s = requests.session()
    s.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'
    })
    return s

if __name__ == "__main__":
    pass