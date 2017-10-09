# -*- coding: utf-8 -*-
'''
@author: Yalei Meng    E-mail: yaleimeng@sina.com
@license: (C) Copyright 2017, HUST Corporation Limited.
@desc:
@DateTime: Created on 2017/10/7，at 20:10            '''

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

def get_ip3366():
    httpList = set()        #type =1 是国内高匿。type =3是国外高匿。都很好
    url_list = ['http://www.ip3366.net/free/?stype=1&page={}'.format(str(i)) for i in range(1,8)]
    for u in url_list:
        soup = requestPage(u)
        if soup is None:
            return [],[]
        infos = soup.select('table.table tr')
        if len(infos) < 1:
            print('没有得到内容。')
            return [],[]
        for info in infos[1:]:
            item = info.select('td')
            address = 'http://' + item[0].text + ':' + item[1].text
            if item[3].text.endswith('TP'):
                httpList.add(address)
    print(httpList)
    return httpList