# -*- coding: utf-8 -*-
'''
@author: Yalei Meng    E-mail: yaleimeng@sina.com
@license: (C) Copyright 2017, HUST Corporation Limited.
@desc:抓取码农很忙的免费代理。10页500条。
@DateTime: Created on 2017/10/12，at 12:55            '''
import time
from proxy import requestPage, write_file, verify_Proxies
import re


def proxy_DB():
    urls = ['http://proxydb.net/?offset={}'.format(str(i)) for i in range(0, 410, 20)]
    output = set()
    for url in urls:
        soup = requestPage(url, wait=3)
        if soup is None:
            return output
        infos = soup.select('table  tbody tr')

        express = re.compile('var.+=.+\d+.+\d+')
        for info in infos:
            item = info.select('td script')
            address = item[0].text
            art = express.findall(address)
            ip = art[0].split("'")[-1][::-1] + art[1].split("'")[-1]
            left = art[2].split('=')[-1].split(' ')[1]
            right = art[2].split('=')[-1].split(' ')[3]
            port = str( int(left) + int(right))
            final = ip + ':' + port
            if final not in output:
                output.add(final)
        print('已找到IP数量：', len(output))
        time.sleep(1.1)
    print(output, '\n最终找到IP总数：', len(output))
    return output


if __name__ == '__main__':
    proxies = proxy_DB()
    good = verify_Proxies(proxies)
    print('有价值数量：%d，占比：%.2f'%(len(good),len(good)/len(proxies)*100))
    file_name = 'Proxy_DB.txt'
    write_file(good, file_name)  # 把良好的代理按JSON格式写入到txt文件。
