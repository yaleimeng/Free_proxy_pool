# -*- coding: utf-8 -*-
'''
@author: Yalei Meng    E-mail: yaleimeng@sina.com
@license: (C) Copyright 2017, HUST Corporation Limited.
@desc:
@DateTime: Created on 2017/10/8，at 13:29            '''
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
    return bs(r.text, 'lxml')

def get_proxy360():
    httpList = set
    soup = requestPage('http://www.proxy360.cn/Proxy')
    if soup is None:
        return [],[]
    rows = soup.select('div.proxylistitem')
    for info in rows:
        item = info.select('span')
        if item[2].text.strip() != '高匿':   #如果不是高匿代理，不收集。
            continue
        address = 'http://' + item[0].text + ':' + item[1].text
        httpsList.add(address.replace('\r\n','').replace(' ',''))
    print(httpList)
    return httpList

