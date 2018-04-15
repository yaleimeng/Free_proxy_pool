# Free_proxy_pool
对免费代理IP网站进行爬取，收集汇总为自己的代理池。其中关键是验证代理的有效性、匿名性、去重复。</br>

本代理池的定位是初学者能看懂，能使用的单机库。所以不打算使用高大上的Redis或者MongoDB等数据库。抓到的代理仅与磁盘文件交互。</br>
本项目**无需安装，下载后查看example**即可学会使用。简洁易用的get_a_proxy()，便于在请求网页的参数中直接使用。</br>

本项目运行所依赖的第三方库：requests、bs4、lxml、chardet。

如果感觉对您有帮助，欢迎给我加一个星星，或者fork。</br>
为了避免大家浪费精力，经验证无实用价值的免费代理网站列举如下，是为“黑名单”：</br>
- http://www.ip181.com/
- https://list.proxylistplus.com/
- http://www.xicidaili.com/nn    百度排名靠前，可用率仅1%左右。
- http://www.kuaidaili.com/free/inha     较新的只有前5页，但可用仅1--2个。
- 更新日期：2018-2-20</br>

>纪念一下曾经有用，现已无法访问的代理网站：
>+ http://www.3366ip.net/
>+ http://www.proxy360.cn/Proxy
>+ http://bugng.com/gngn
>+ http://ip.seofangfa.com/
>+ http://www.kxdaili.com/daili.html
