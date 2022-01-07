# -*- coding: utf-8 -*-
'''
@author: yaleimeng@sina.com  (C) Copyright 2017.
@desc:   爬虫类。为代理池提供抓取代理IP功能。
@DateTime: Created on 2017/10/16，at 8:47            '''
import chardet, re, time
import requests as rq
from  bs4 import BeautifulSoup as bs


class Proxy_Spider(object):
    proxies_got = set()

    def request_page(cls, page, proxy=None, wait=2):
        head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML,'
                              ' like Gecko) Chrome/55.0.2883.75 Safari/537.36'}
        try:
            r = rq.get(page, headers=head, proxies=proxy, timeout=wait)
            r.encoding = chardet.detect(r.content)['encoding']
            return bs(r.text, 'lxml')
        except Exception:
            print('……无法获取网页。', end='\t')
            return None

    def crawl(self):        
        self.__get_All66()     # 数量自定义。抓取到的代理越多，验证用时越长。
        self.__get_All89()     # 考虑验证耗时因素，后面几个可以选择性启用。
        return self.proxies_got

    def crawl_for_init(self):
        self.__xiao_shu()      # 每天更新2篇文章。只适合一次性采集
        # self.__ihuan() 站点压力大，不要频繁抓取。
        self.__zhima()
        self.__kaixin()
        return self.proxies_got

    def __rows_from(self, url, exp=None):  # 从网页表格中提取，seo方法、codeBusy采用了这种方式。
        express = 'table tbody tr' if exp is None else exp
        soup = self.request_page(url, wait=3)
        return None if soup is None else soup.select(express)
            
    def __ihuan(self):
        urls = ['https://ip.ihuan.me/?page={}&anonymity=2'.format(str(i)) for i in range(1, 31)]
        for url in urls:
            for info in self.__rows_from(url):
                item = info.select('td')
                address = item[0].text + ':' + item[1].text
                if address not in self.proxies_got:
                    self.proxies_got.add(address)
            print('已采集小幻代理，代理池IP总数：', len(self.proxies_got))   
            
    def __parse_by_re(self, url, reg_exp=re.compile('\w+\.\w+\.\w+\.\w+:\w+')):  # 正则提取， 66ip、89ip、QQ_room、开心代理采用了这种解析方式
        article = None if self.request_page(url) is None     else self.request_page(url).__unicode__()
        return reg_exp.findall(article)

    def __get_All66(self):
        urls = ['http://www.66ip.cn/nmtq.php?getnum=300&isp=0&anonymoustype={}&start=&ports=&export=&ipaddress='
                '&area=1&proxytype=0&api=66ip '.format(str(i)) for i in range(3, 5)]
        # 采集国内的，高匿、超匿2种HTTP代理。如果想采集国外的，area改为2。【如果要采集HTPPS，proxytpye = 1 】
        for url in urls:
            self.proxies_got.update(self.__parse_by_re(url))  # 把找到的代理IP添加到集合里面
            print('已采集66ip.cn，代理池IP总数：', len(self.proxies_got))
            time.sleep(1.1)

    def __get_All89(self):
        url = 'http://www.89ip.cn/tiqv.php?sxb=&tqsl=400&ports=&ktip=&xl=on&submit=%CC%E1++%C8%A1'
        find_out = self.__parse_by_re(url)
        self.proxies_got.update(find_out)
        print('已采集89ip.cn，代理池IP总数：', len(self.proxies_got))

    def __xiao_shu(self):
        page_list = []
        soup = self.request_page('http://www.xsdaili.com/')
        news = soup.select('div.title a')[:6]  # 获取最新的4篇文章。
        for info in news:
            link = 'http://www.xsdaili.com' + info.get('href')
            page_list.append(link)
        for page in page_list:
            self.proxies_got.update(self.__parse_by_re(page))
            print('已采集小舒代理，代理池IP总数：', len(self.proxies_got))
            time.sleep(0.5)      
            
    def __zhima(self):
        #  芝麻代理，每小时更新国内代理IP。
        page_list = []
        soup = self.request_page('https://h.zhimaruanjian.com/free/')
        
        for info in soup.select('div.titles a')[:4]:  # 只抓取首页的4篇文章
            link = 'https://h.zhimaruanjian.com{}'.format(info.get('href'))                   
            page_list.append(link)
       
        for page in page_list:
            self.proxies_got.update(self.__parse_by_re(page))
            print('已采集zhima代理，代理池IP总数：', len(self.proxies_got))
            time.sleep(0.5)

    def __kaixin(self):
        #  开心代理，每天更新一篇国内代理IP。 div.cont_list > ul > li:nth-child(1) > a.title
        page_list = []
        soup = self.request_page('http://www.kxdaili.com/daili.html')

        for info in soup.select('div.cont_list a.title')[:1]:      # 只抓取首页的前2篇文章
            link = 'http://www.kxdaili.com{}'.format(info.get('href'))
            page_list.append(link)

        for page in page_list:
            self.proxies_got.update(self.__parse_by_re(page))
            print('已采集kaixin代理，代理池IP总数：', len(self.proxies_got))
            time.sleep(0.5)
   
