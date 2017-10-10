# -*- coding: utf-8 -*-
'''
@author: Yalei Meng    E-mail: yaleimeng@sina.com
@license: (C) Copyright 2017, HUST Corporation Limited.
@desc:
@DateTime: Created on 2017/10/8，at 15:16            '''

import requests as rq
from  bs4 import BeautifulSoup as bs
import time

def  requestPage(page ,want_Text = True ):
    ua = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3192.0 Safari/537.36'
    head = {'User-Agent': ua}
    try:
        r = rq.get(page , headers = head)
    except Exception as e:
        print(e.args)
        return None
    return bs(r.text, 'lxml')


def get_66ip_cn():       #这个函数要访问几十上百个网页。效率比较低。
    httpList ,full= set()  ,[]
    url_list = ['http://www.66ip.cn/areaindex_{}/'.format(str(i))
                for i in range(1, 35)]  # 共34个地区
    for url in url_list:
        new_list = [url + '{}.html'.format(str(i)) for i in range(1, 4)]
        full += new_list
    for u in full:
        soup = requestPage(u)
        if soup is None:
            continue
        rows = soup.select('div.footer table tr')
        for row in rows[1:]:
            item = row.select('td')
            address = item[0].text+':'+item[1].text
            if address not in httpList:       #使用集合来排除重复。
                 httpList.add(address)
                 print(address,end = '\t')
        time.sleep(0.5)
    return httpList         #以集合形式传递出去。