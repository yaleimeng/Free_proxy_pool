# -*- coding: utf-8 -*-
'''
@author: Yalei Meng    E-mail: yaleimeng@sina.com
@license: (C) Copyright 2017, HUST Corporation Limited.
@desc:
@DateTime: Created on 2017/10/9，at 12:42            '''
from proxy import requestPage,write_file,verify_Proxies
import re

def get_All89():
      ip_exp = re.compile('\w+\.\w+\.\w+\.\w+:\w+')
      url = 'http://www.89ip.cn/tiqv.php?sxb=&tqsl=400&ports=&ktip=&xl=on&submit=%CC%E1++%C8%A1'
      output = set()
      article = requestPage(url,wait=3).__unicode__()
      out = ip_exp.findall(article)
      output .update(out)
      print('找到IP总数量：', len(output))
      return output

if __name__ == '__main__':
    proxies = get_All89()
    good = verify_Proxies(proxies)
    print('有价值数量：%d，占比：%.2f' % (len(good), len(good) / len(proxies) * 100))
    file_name = 'IP89_Proxy.txt'
    write_file(good, file_name)  # 把良好的代理按JSON格式写入到txt文件。