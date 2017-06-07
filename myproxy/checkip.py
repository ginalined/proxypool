# coding=utf-8
import re
import requests

class CheckIp:

    def __init__(self):

        self.local = ''
        self.http_check_url = 'http://ddns.oray.com/checkip'
        self.http_check_urls = ['http://ddns.oray.com/checkip', 'http://www.baidu.com', 'http://ip.cn/']
        self.https_check_urls = ['https://ddns.oray.com/checkip','https://www.douban.com/', 'https://www.tmall.com/']
        self._get_local()

    # 获取本地 ip
    def _get_local(self):

        req = requests.get(self.http_check_url)
        self.local = self._extract_ip(req.text)

    # 从网页中提取 ip
    def _extract_ip(self, page):

        pattern = re.compile(r'<body>Current IP Address: (\d+.\d+.\d+.\d+)</body>')
        res = re.findall(pattern=pattern, string=page)
        if len(res) >= 1:
            return res[0]

    # 从给定数据中提取 ip
    def _extract_ip_2(self,dic):

        try:
            proxy = dic.get('http')
        except:
            proxy = dic.get('https')

        ip = proxy.split('//')[1].split(':')[0]
        return ip

    # 检查 ip 是否可用
    def check(self, proxy, type, is_https=False):

        # print(proxy, type)
        # 查看是否使用 https 代理
        if is_https:
            urls = self.https_check_urls

        else:
            urls = self.http_check_urls


        suc_count = 0
        for url in urls:
            try:
                req = requests.get(url=url, proxies=proxy, timeout=2)
                assert req.status_code == 200
                suc_count += 1

            except Exception as e:
                continue

        if suc_count >= 2:
            # print(proxy,suc_count)
            return True

        else:
            return False



