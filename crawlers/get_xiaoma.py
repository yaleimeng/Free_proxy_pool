# -*- coding: utf-8 -*-
'''
@author: Yalei Meng    E-mail: yaleimeng@sina.com
@license: (C) Copyright 2017, HUST Corporation Limited.
@desc:抓取小马网络的免费代理。
@DateTime: Created on 2017/10/12，at 13:54            '''
from proxy import requestPage,write_file,verify_Proxies
import time

def get_xiaoma():
      domestic = ['http://www.yun-daili.com/free.asp?stype=1&page={}'.format(str(i)) for i in range(1,6)]
      foreign =  ['http://www.yun-daili.com/free.asp?stype=3&page={}'.format(str(i)) for i in range(1,6)]
      urls = domestic + foreign
      output = set()
      for url in urls:
          soup = requestPage(url)
          if soup is None:
              continue
          infos = soup.select('table.table tbody tr')
          for info in infos:
              item = info.select('td')
              address = item[0].text + ':' + item[1].text
              if address not in output:
                  output.add(address)
          time.sleep(1.3)
      print(output, '找到IP数量：', len(output))
      return output

if __name__ == '__main__':
    proxies = get_xiaoma()
    good = verify_Proxies(proxies)
    print('有价值数量：%d，占比：%.2f'%(len(good),len(good)/len(proxies)*100))
    file_name = 'XiaoMa_Proxy.txt'
    write_file(good, file_name)  # 把良好的代理按JSON格式写入到txt文件。