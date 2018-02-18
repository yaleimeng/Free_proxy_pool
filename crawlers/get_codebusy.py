# -*- coding: utf-8 -*-
'''
@author: Yalei Meng    E-mail: yaleimeng@sina.com
@license: (C) Copyright 2017, HUST Corporation Limited.
@desc:抓取码农很忙的免费代理。10页500条。
@DateTime: Created on 2017/10/12，at 12:55            '''
from proxy import requestPage,write_file,verify_Proxies

def get_All66():
      urls = ['proxy.coderbusy.com/'.format(str(i)) for i in range(1,12)]
      output = set()
      for url in urls:
          soup = requestPage(url, wait=3)
          if soup is None:
              return output
          infos = soup.select('table tbody tr')
          for info in infos:
              item = info.select('td')
              address = item[0].text.strip() + ':' + item[1].text[16:-3]
              if address not in output:
                  output.add(address)
      print(output, '找到IP数量：', len(output))
      return output

if __name__ == '__main__':
    proxies = get_All66()
    good = verify_Proxies(proxies)
    print('有价值数量：%d，占比：%.2f'%(len(good),len(good)/len(proxies)*100))
    file_name = 'CodeBusy_Proxy.txt'
    write_file(good, file_name)  # 把良好的代理按JSON格式写入到txt文件。
