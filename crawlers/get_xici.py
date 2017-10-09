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

def getXici():     #固定访问前面5页，从中获取代理。
    url_list = ['http://www.xicidaili.com/nn/{}'.format(str(n)) for n in range(1,6) ] #高匿名代理是nn
    httpList = [];      httpsList= []
    for url in url_list:
        soup = requestPage(url)
        if soup is None:
            time.sleep(1.5);            continue
        infos = soup.select('tr.odd')
        if len(infos)>0:
            for info in infos:
                item = info.select('td')
                if len(item)>5 :
                    address = 'http://' + item[1].text + ':' + item[2].text
                    if item[5].text == 'HTTP':
                        httpList.append(address)
                    elif item[5].text == 'HTTPS':
                        httpsList.append(address)
        else:
            print('没有得到内容，可能服务器限制访问。')
        time.sleep(1.5)
    print (httpList,'\n\n')
    return httpList         #这个是用列表返回。自己可以选择是否采用集合形式。

