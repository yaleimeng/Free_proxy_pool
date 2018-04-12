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
        self.__get_seo_FangFa()  # 总量380左右。每分钟更新。
        self.__get_code_busy()  # 总量550上下。15到20分钟更新一次。
        self.__get_Ai_Jia()  # 6篇文章总量500多。每小时更新1篇文章。
        # self.__get_All66()     # 数量自定义。抓取到的代理越多，验证用时越长。
        # self.__get_All89()     # 考虑验证耗时因素，后面几个可以选择性启用。
        # self.__get_kai_xin()   # 每小时更新一篇文章，100个代理。
        return self.proxies_got

    def crawl_for_init(self):
        self.__get_code_busy()  # 更新很频繁，适合初次启动时更新一下。
        self.__get_qq_room()  # 该站每天更新一次，只适合在第一次启动时更新。不需要反复运行
        return self.proxies_got

    def __rows_from(self, url, exp=None):  # 从网页表格中提取，seo方法、codeBusy采用了这种方式。
        express = 'table tbody tr' if exp is None else exp
        soup = self.request_page(url, wait=3)
        return None if soup is None else soup.select(express)

    def __get_seo_FangFa(self):
        for info in self.__rows_from('http://ip.seofangfa.com/'):
            item = info.select('td')
            address = item[0].text + ':' + item[1].text
            if address not in self.proxies_got:
                self.proxies_got.add(address)
        print('已采集seoFF，代理池IP总数：', len(self.proxies_got))

    def __get_code_busy(self):
        urls = ['https://proxy.coderbusy.com/classical/anonymous-type/highanonymous.aspx?page={}'.format(str(i)) for i in range(1, 12)]
        for url in urls:
            for info in self.__rows_from(url):
                item = info.select('td')
                address = item[0].text.strip() + ':' + item[1].text[16:-3]
                if address not in self.proxies_got:
                    self.proxies_got.add(address)
            time.sleep(0.8)
        print('已采集code_busy，代理池IP总数：', len(self.proxies_got))

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

    def __get_qq_room(self):
        page_list, output = [], set()
        host = 'http://ip.qqroom.cn/'
        news = self.request_page(host).select('section.article-list h2 a')  # 标题必须包含‘代理ip’
        for info in news:
            if info.text.__contains__('代理ip'):
                page_list.append(host + info.get('href'))
        ip_exp = re.compile('\d+\.\d+\.\d+\.\d+:\d+')  # 文字描述太多。不能使用\w代替。
        for page in page_list[:2]:  # 只收集包含"代理ip"的前2篇文章
            self.proxies_got.update(self.__parse_by_re(page, ip_exp))
            print('已采集QQ_room，代理池IP总数：', len(self.proxies_got))
            time.sleep(0.8)

    def __get_kai_xin(self):
        page_list = []
        soup = self.request_page('http://www.kxdaili.com/daili.html')
        news = soup.select('div.clear_div > div.ui a')[:9:2]  # 获取最新的5篇文章。
        for info in news:
            link = 'http://www.kxdaili.com' + info.get('href')
            page_list.append(link)
        for page in page_list:
            self.proxies_got.update(self.__parse_by_re(page))
            print('已采集开心代理，代理池IP总数：', len(self.proxies_got))
            time.sleep(0.8)

    def __get_Ai_Jia(self):  # 爱家网，每小时更新国内国外代理IP。可用率不成。
        page_list = []
        soup = self.request_page('http://www.ajshw.net/news/?list_9.html')
        for info in soup.select('dd.listBox5')[0].select('a')[:6]:  # 国内代理最新的6篇文章。
            link = 'http://www.ajshw.net' + info.get('href')[2:]  # href开头有两个点..，要去掉。
            page_list.append(link)

        for info in soup.select('dd.listBox5')[1].select('a')[:3]:  # 国外代理最新的3篇文章。
            link = 'http://www.ajshw.net' + info.get('href')[2:]  # href开头有两个点..，要去掉。
            page_list.append(link)

        ip_exp = re.compile('\d+\.\w+\.\w+\.\w+:\d+')
        for page in page_list:
            soup, ports = self.request_page(page), []
            address = soup.select('div#newsContent p')[0]
            ips = ip_exp.findall(address.text)
            self.proxies_got.update(ips)
            print('已采集ajshw，代理池IP总数：', len(self.proxies_got))
            time.sleep(0.8)
