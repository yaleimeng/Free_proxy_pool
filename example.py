# -*- coding: utf-8 -*-
'''
@author: yaleimeng@sina.com
@license: (C) Copyright 2017
@desc: 本IP池使用示例。
@DateTime: Created on 2017/10/16，at 11:38            '''

import proxy_pool, requests
from bs4 import BeautifulSoup as bs

my_pro = proxy_pool.Free_proxy_pool()
a_pro = my_pro.get_a_proxy()
print('当前代理为：',a_pro)

r = requests.get('http://www.ipip.net/',proxies = a_pro)
info = bs(r.text,'lxml').select('div.location')[0].text.rstrip()
print(info)

# 实际使用时，可以首先运行proxy_pool.py，保障数据库在持续更新。
# 其他程序调用，只需要导入，简单地使用get_a_proxy()即可。
# HTTP请求结果无效时，需要重新获取代理。请自行添加try catch语句。