# -*- coding: utf-8 -*-
'''
@author: Yalei Meng    E-mail: yaleimeng@sina.com
@license: (C) Copyright 2017, HUST Corporation Limited.
@DateTime: Created on 2017/10/9，at 9:16            '''
from proxy import requestPage,write_file,verify_Proxies
import re

def get_All66():
      ip_exp = re.compile('\d+\..+\d+:\d+')     #采集国内的，高匿、超匿2种HTTP代理。
      urls = ['http://www.66ip.cn/nmtq.php?getnum=500&isp=0&anonymoustype={}&start=&ports=' 
              '&export=&ipaddress=&area=1&proxytype=0&api=66ip'.format(str(i)) for i in range(3,5)]
      output = set()
      for url in urls:
          article = requestPage(url).__unicode__()
          out = ip_exp.findall(article)
          output .update(out)          #把800个添加到集合里面
      print(output, '找到IP数量：', len(output))
      return output

if __name__ == '__main__':
    proxies = get_All66()
    good = verify_Proxies(proxies)
    print('有价值数量：%d，占比：%.2f'%(len(good),len(good)/len(proxies)*100))
    file_name = 'IP66_Proxy.txt'
    write_file(good, file_name)  # 把良好的代理按JSON格式写入到txt文件。