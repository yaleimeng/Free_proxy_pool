# -*- coding: utf-8 -*-
'''
@author: yaleimeng@sina.com  (C) Copyright 2017.
@desc:代理池主调度类。对外提供服务接口。
@DateTime: Created on 2017/10/16，at 11:33
 '''
import threading, multiprocessing
import json, spiders


class Free_proxy_pool(object):
    '''
    代理IP池的主类。对外提供代理IP。当前代理池默认是HTTP代理。HTTPS的后面再另外扩充。
    属性：min_limit：设置代理池的下限，达到下限时自动更新代理池。确保数量一直高于下限。默认值15个。
    对外方法： get_a_proxy()
    参数：返回一个高匿的HTTP代理地址。是 {'http': 'http://' + pro, }字典形式可直接使用。
    类内使用的代理，都是单纯的“IP地址+端口”形式。
    '''

    def __init__(self):
        self.__datafile = 'HTTP_Proxy_pool.txt'
        self.__proxies_ok = []  # 对它的操作主要是write_file，读取并清空。
        self.min_limit = 24
        self.__spider = spiders.Proxy_Spider()

    def pro_count(self):  # 代理池中的数量，以文件中剩余数量为准。
        return len(self.__read_file())

    def light_update(self):  # 轻度更新，读取文件中的代理，校验可用性。将有效代理写回去。
        print('更新前，代理池数量：', self.pro_count())
        self.__write_file(self.verify_Proxies(self.__read_file()))
        print('更新后，代理池数量：%d\n' % self.pro_count())
        if self.pro_count() < self.min_limit:  # 当可用数量低于下限时，在新的线程执行深度更新。
            pp = multiprocessing.Process(target= self.update_all())
            pp.start()   # 要保证安全库存代理全部失效以前，批量爬取的代理能够验证完，写入文件。
        global A_timer, free_p  # 循环启动定时器，每隔10分钟重新检测已保存代理有效性。
        A_timer = threading.Timer(600, free_p.light_update)
        A_timer.start()

    def get_a_proxy(self):  # 对外给出的是直接可用的代理形式。
        tmp, good = self.__read_file(), []
        if tmp:
            while len(good) < 1:
                good = self.verify_Proxies([tmp.pop()])
                if not tmp:
                    break
        if len(tmp) < self.min_limit:  # 如果没有获取到有效代理。需要大量更新。
            th = threading.Thread(target=self.light_update)
            th.start()
        self.__write_file(tmp)
        return {'http': 'http://' + good.pop(), }

    def __write_file(self, gList=None):
        with open(self.__datafile, 'w', encoding='utf-8')as f:
            if gList:
                json.dump(gList, fp=f, indent=4)
            else:
                json.dump(self.__proxies_ok, fp=f, indent=4)
        self.__proxies_ok.clear()

    def __read_file(self):
        with open(self.__datafile, 'r', encoding='utf-8')as fp:
            return json.load(fp)

    def verify_Proxies(self, pro_set):
        output = []
        #print('待验证代理总数：%d\n' % len(pro_set))
        for one_p in pro_set:
            pro = {'http': 'http://' + one_p, }            
            # 因为代理匿名性验证比较麻烦，取消验证直接收集
            try:
               soup = self.__spider.request_page('http://ip111.cn/', pro)
               if soup is None:         continue
               output.append(one_p)  # 把代理加入到.proxies_ok中去。
            #    ip = soup.select('p.getlist')[0].text.split('：')[1][:-6]
            #    if ip == one_p.split(':')[0] and one_p not in output:
            #        output.append(one_p)  # 把代理加入到.proxies_ok中去。
            #        print('当前代理：%s是高匿类型！已收集总数：%d' % (one_p, len(output)))
            # except Exception as ex:pass
            #    #print('……解析失败……', end='\t')
        print('验证完毕！HTTP代理总数：%d\n' % len(output))
        return output

    def update_all(self):  # 深度更新函数。
        tmp = self.__spider.crawl()
        tmp.update(self.__read_file())
        self.__write_file(self.verify_Proxies(tmp))

    def first_crawl(self):
        tmp = self.__spider.crawl_for_init()
        tmp.update(self.__read_file())
        self.__write_file(self.verify_Proxies(tmp))


if __name__ == '__main__':
    free_p = Free_proxy_pool()  # 定时器回调。刚启动会执行1次轻度更新，从库中剔除失效代理。后面每隔10分钟更新1次。
    A_timer = threading.Timer(0.5, free_p.light_update)
    A_timer.start()
    pp = multiprocessing.Process(target= free_p.first_crawl)
    pp.start()         # 另外开启一个新的进程执行深度更新。
