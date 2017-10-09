# -*- coding: utf-8 -*-
'''
@author: Yalei Meng    E-mail: yaleimeng@sina.com
@license: (C) Copyright 2017, HUST Corporation Limited.
@desc:
@DateTime: Created on 2017/10/6，at 22:29            '''
import requests as rq
from  bs4 import BeautifulSoup as bs

def  requestPage(page ,want_Text = True ):
    ua = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3192.0 Safari/537.36'
    head = {'User-Agent': ua}
    try:
        r = rq.get(page , headers = head)
    except Exception as e:
        print(e.args)
        return None
    return bs(r.content, 'lxml')

def get_ip181():
    httpList = set()
    soup = requestPage('http://www.ip181.com')
    if soup is None:
        return [],[]
    infos = soup.select('table tr')
    if len(infos) < 1:
        print('没有得到内容。')
        return [],[]
    for info in infos[1:]:
        item = info.select('td')
        if item[2].text != '高匿':   #如果不是高匿代理，不收集。
            continue
        address = 'http://' + item[0].text + ':' + item[1].text
        if item[3].text.startswith('HTTP'):
            httpList.append(address)
        if item[3].text.endswith('PS'):
            httpsList.add(address)
    print(httpList)
    return httpList

