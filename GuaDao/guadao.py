import json
import os
import time
import traceback
import urllib
import winsound

import urllib3
from colorama import Fore, Style, init

import Market3rd
import SimpleTable
import Steam


def logLastException(title=''):
    os.makedirs('log',exist_ok=True)

    title = ''.join([c for c in title if c not in r'<>:"/\|?*'])
    filename = time.strftime('log\\[%Y-%m-%d][%H-%M-%S] ') + title[:60]
    with open(filename,'w',encoding='utf-8') as f:
        traceback.print_exc(file=f)

# colorama
init()

CONFIG = {
    # "Buff": {
    #     "InitArgs": [
    #         "1-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    #     ],
    #     "QueryString": "game=dota2#tab=selling&page_num=1"
    # },
    "ExpectedRatio": 0.65,
    "ExpectedVolume": 20,
    "EnableSteamMarketApi": [
        # "ItemOrder"
    ],
    "SteamRequestsInterval": 8,
    "SteamCopyPriceRatio": [
        # 0.65,
        # 0.7
    ],
    "PrintUnexpected": True,
    "VerifySteamCertificate": True
}
with open('config.json','r',encoding='utf-8') as f:
    CONFIG.update(json.load(f))

colsorder = [
    ('平台物品链接', 55),
    ('平台内名称',30),
    '平台最低',
    'ST最低出售',
    'ST最低出售税后比例',
    'ST最高收购',
    'ST最高收购税后比例',
    'ST中位数',
    'ST中位数税后比例',
    'ST成交量(24h)',
    'ST成交量(7d)'
]

# 若要不显示某一列, 请修改 cols
cols = [('平台物品链接', 55), ('平台内名称',30),'平台最低']
if 'ItemPriceOverview' in CONFIG['EnableSteamMarketApi']:
    cols += ['ST最低出售','ST最低出售税后比例','ST中位数','ST中位数税后比例','ST成交量(24h)']
if 'ItemOrder' in CONFIG['EnableSteamMarketApi']:
    cols += ['ST最低出售','ST最低出售税后比例','ST最高收购','ST最高收购税后比例','ST成交量(24h)','ST成交量(7d)']
for ratio in CONFIG['SteamCopyPriceRatio']:
    cols.append(f'ST复制售价({ratio})')

headrow = sorted(
    set(cols),
    key = lambda col: colsorder.index(col) if col in colsorder else len(colsorder) + cols.index(col)
)

STABLE = SimpleTable.SimpleTable(headrow)
STABLE.printHeadRow()

M3S = []
M3GENS = []

if 'Buff' in CONFIG:
    M3S.append(Market3rd.Buff(*CONFIG['Buff']['InitArgs']))
    M3GENS.append(M3S[-1].walkItems(CONFIG['Buff']['QueryString']))

SM = Steam.Market()
SM.session.request_interval = CONFIG['SteamRequestsInterval']
if not CONFIG['VerifySteamCertificate']:
    SM.session.verify = False
    urllib3.disable_warnings()

for gen in M3GENS:
    vis = {}
    while True:
        try:
            i3 = next(gen)
        except StopIteration:
            continue
        
        if i3.url3rd in vis:
            continue
        else:
            vis[i3.url3rd]=True

        row = {
            '平台': i3.market3rd,
            '平台物品链接': i3.url3rd,
            '平台内名称': i3.name_in_market3rd,
            '平台最低': i3.lowest_sell_price,
            'ST路由': f'/{i3.appid}/{i3.market_hash_name}',
        }

        for ratio in CONFIG['SteamCopyPriceRatio']:
            row.update({f'ST复制售价({ratio})': round((1.15 * i3.lowest_sell_price) / ratio, 2)})

        def updateRow_IPO():
            ipo = SM.getItemPriceOverview(i3.appid, i3.market_hash_name)
            row.update({
                    'ST最低出售': ipo.lowest_sell_price,
                    'ST最低出售税后比例':round(row['平台最低']/(ipo.lowest_sell_price/1.15),2) if ipo.lowest_sell_price != 0 else 1,
                    'ST中位数':ipo.median_sell_price,
                    'ST中位数税后比例':round(row['平台最低']/(ipo.median_sell_price/1.15),2) if ipo.median_sell_price != 0 else 1,
                    'ST成交量(24h)':ipo.volume_24h
            })
        
        def updateRow_IO():
            nid = SM.getNameidByHashName(i3.appid, i3.market_hash_name)
            
            iph = SM.getItemPriceHistory(i3.appid, i3.market_hash_name)
            row.update({
                'ST成交量(24h)': iph.getVolumeSumInTime(60*60*24),
                'ST成交量(7d)': iph.getVolumeSumInTime(60*60*24*7),
            })

            io = SM.getItemOrder(nid)
            row.update({
                    'ST最低出售': io.lowest_sell_price,
                    'ST最低出售税后比例':round(row['平台最低']/(io.lowest_sell_price/1.15),2) if io.lowest_sell_price != 0 else 1,
                    'ST最高收购': io.highest_buy_price,
                    'ST最高收购税后比例': round(row['平台最低']/(io.highest_buy_price/1.15),2) if io.highest_buy_price != 0 else 1,
            })

        
        api2func = {
            'ItemPriceOverview':updateRow_IPO,
            'ItemOrder':updateRow_IO
        }

        excs = []
        for api in CONFIG['EnableSteamMarketApi']:
            try:
                api2func[api]()
                ok = True
            except Exception as e:
                excs.append(str(e))
                logLastException(str(e))
        
        color = Fore.LIGHTBLACK_EX
        for k in row:
            if '比例' in k and row[k] <= CONFIG['ExpectedRatio']:
                color = min([Fore.YELLOW, color])
                if 'ST成交量(24h)' in row and CONFIG['ExpectedVolume'] <= row['ST成交量(24h)']:
                    color = min([Fore.GREEN, color])
        
        if color != Fore.LIGHTBLACK_EX or CONFIG['PrintUnexpected']:
            STABLE.printRowByDict(row,prefix=color, newline=False)
            if len(excs)!=0:
                print(f'{Fore.RED}{",".join(excs)}{Style.RESET_ALL}')
            else:
                print(f'{Style.RESET_ALL}')
        
        if color == Fore.YELLOW:
            winsound.Beep(500,700)
        elif color == Fore.GREEN:
            winsound.Beep(2000,700)
