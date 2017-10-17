# -*- coding: utf-8 -*-
'''
@author: Yalei Meng    E-mail: yaleimeng@sina.com
@license: (C) Copyright 2017, HUST Corporation Limited.
@desc:
@DateTime: Created on 2017/10/8，at 15:16            '''

import time
from proxy import requestPage,write_file,verify_Proxies

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
    print('最终累积收集数量',len(httpList))
    return httpList         #以集合形式传递出去。


if __name__ == '__main__':
    proxies = get_66ip_cn()
    good = verify_Proxies(proxies)
    print('有价值数量：%d，占比：%.2f'%(len(good),len(good)/len(proxies)*100))
    file_name = 'Proxy_IP66.txt'
    write_file(good, file_name)  # 把良好的代理按JSON格式写入到txt文件。