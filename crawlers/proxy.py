# -*- coding: utf-8 -*-
'''
@author: Yalei Meng    E-mail: yaleimeng@sina.com
@license: (C) Copyright 2017, HUST Corporation Limited.
描述：收集到的地址和端口一律不带【http://】，用list类型返回。在验证和使用的时候加上前缀进行验证。
@DateTime: Created on 2017/9/13，at 9:40            '''

import json, chardet
import requests as rq
from  bs4 import BeautifulSoup as bs


def requestPage(page ,proxy = None , wait = 2):
    ua = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36'
    head = {'User-Agent': ua}
    try:
        r = rq.get(page ,headers = head)  if proxy is None else rq.get(page ,headers = head,
                                                                       proxies = proxy, timeout = wait)
        r.encoding = chardet.detect(r.content)['encoding']
        return bs(r.text, 'lxml')
    except Exception as e:
        print('……获取网页异常。')
        return None

def verify_Proxies(pro_list):
    if len(pro_list)<1 :      #如果列表为空，什么都不做
        print('列表为空，无法验证！');        return []
    good = set()
    for np in pro_list:
        pro = {'http':'http://'+np,}    #这里前半截要去掉
        if np in good:        continue #如果代理已经存在，不再验证。
        try:
            soup = requestPage('http://ip.chinaz.com/',pro)
            if soup is None:         continue
            addr = soup.select('p.getlist')[0].text.split('：')[1][:-6]
            if addr ==  np.split(':')[0]:
                good.add(np)  # 把代理加入到good中去。
                print('\n当前代理：%s是高匿类型！已收集总数：%d'%(np,len(good)))
        except Exception as ex:
            print('……解析失败……',end='；\t')
    print('优质HTTP代理数量：%d\n'%len(good),good)
    return  list(good)

def write_file( gList,fName):
    if not gList:            #如果是空列表，不处理。
        return
    with open('E:/'+fName, 'w', encoding='utf-8')as f:
       json.dump(gList,fp=f,indent=4)

def read_file(file):
    with open('E:/' + file, 'r', encoding='utf-8')as fp:
        return set(json.load(fp))

if __name__ == '__main__':
    file_name = 'Good_Proxy.txt'
    full =  read_file(file_name) | read_file('IP89_Proxy.txt')   # 多个集合取并集get_Xici()
    print('累计有 %d 个代理需要验证！'%len(full))
    good = verify_Proxies(full)
    write_file(good,file_name)     #把良好的代理按JSON格式写入到txt文件。