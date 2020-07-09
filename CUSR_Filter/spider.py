'''
学科排名信息来源
https://souky.eol.cn/api/newapi/assess_result

高校地址信息来源
https://gkcx.eol.cn
'''

import requests
import time
import jinja2
import logging
import json
import os
import re
from urllib.parse import quote as encode_url

path_schools_addr = './schools_addr.json'
path_cusr_result = './cusr_result.json'

def read_json(path,default):
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return default

def save_json(obj, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)


web_session = requests.session()
web_session.headers.update({ 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0' })

# Get CUSR
cusr = read_json(path_cusr_result,{
        'result': {},
        'xid_ok': [],
        'xid_null': []
    })
'''cusr结构
{
    'result': {
        '专业': [
            {
                'code': '高校代码',
                'name': '高校名称',
                'result': '评估结果'
            }
            // 以评估结果由高到低排序
        ]
    },
    'xid_ok': [], // 已获取内容的xid
    'xid_null': [] // 空的xid
}
'''

xid = 0
while True:
    xid += 1
    if xid in cusr['xid_ok'] or xid in cusr['xid_null']:
        continue
    elif xid == 112:
        break

    print(f'[GET] CUSR {xid}')
    rsp = web_session.get(f'https://souky.eol.cn/api/newapi/assess_result?xid={xid}&flag=1').json()
    if rsp[0] == None:
        cusr['xid_null'].append(xid)
        continue

    subject = rsp[0]['name']
    results = [{
        'code': school['scode'],
        'name': school['sname'],
        'result': school['result']
        } for school in rsp[1]]
    
    cusr['result'][subject] = results
    cusr['xid_ok'].append(xid)

    # 避免高频请求
    time.sleep(0.5)

save_json(cusr, path_cusr_result)

# Get schools' address
schools_addr = read_json(path_schools_addr,{})
'''
{
    '高校': '地址'
}
'''

for sub in cusr['result']:
    for sch in cusr['result'][sub]:
        name = sch['name']
        if name in schools_addr:
            continue

        print(f'[GET] ADDR {name}')
        try:
            url = f'https://api.eol.cn/gkcx/api/?access_token=&keyword={encode_url(name)}&page=1&signsafe=&size=20&sort=view_total&uri=apidata/api/gk/school/lists'
            web_session.options(url)
            rsp = web_session.post(url).json()
            
            schools_addr[name] = 'NONE' # 确保每个校名都有对应地址
            for idx in range(len(rsp['data']['item'])):
                school = rsp['data']['item'][idx]
                addr = school['city_name']+school['county_name']
                if school['province_name'] not in addr:
                    addr = school['province_name'] + addr
            
                if idx == 0:
                    schools_addr[name]=addr+'*' # 确保每个校名都有对应地址
                schools_addr[school['name']]=addr
        except Exception as e:
            print(e)

        time.sleep(1)

save_json(schools_addr,path_schools_addr)