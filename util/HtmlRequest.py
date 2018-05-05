#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : HtmlRequest.py
# @Author: Wanglei
# @Date  : 2018/5/1
# @Desc  :
import time
import random
import requests
from lxml import etree
from requests.packages.urllib3.exceptions import InsecureRequestWarning



requests.packages.urllib3.disable_warnings(InsecureRequestWarning)



class HtmlRequest:

    @property
    def user_agent(self):
        """
        return an User-Agent at random
        :return:
        """
        ua_list = [
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
            'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
        ]
        return random.choice(ua_list)


    @property
    def header(self):
        """
        basic header
        :return:
        """
        return {'User-Agent': self.user_agent,
                'Accept': '*/*',
                'Accept - Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Accept-Language': 'zh-CN,zh;q=0.9'}

    def get(self, url, header=None, retry_time=3, proxies=None, timeout=10, retry_interval=0, verify=False):
        headers = self.header
        if header and isinstance(header, dict):
            headers.update(header)
        while True:
            try:
                r = requests.get(url, headers=headers, proxies=proxies, timeout=timeout, verify=verify)
                if not r.ok:
                    raise Exception
                return r
            except Exception as e:
                print(e)
                retry_time -= 1
                if retry_time <= 0:
                    # 多次请求失败
                    return None
                time.sleep(retry_interval)


    def post(self, url, data, headers):
        try:
            r = requests.post(url, data, headers=headers)
            return r
        except Exception as e:
            print(e)

if __name__ == "__main__":
    headers = {
        'Host': 'www.gatherproxy.com',
        'Proxy-Connection': 'keep-alive',
        'Origin': 'http://www.gatherproxy.com',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'http://www.gatherproxy.com/proxylist/country/?c=China',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9'

    }
    html_request = HtmlRequest()
    url = 'http://www.gatherproxy.com/proxylist/country/?c=China'
    data = {
        "Country": "china",
        "PageIdx": 1,
        "Filter": '',
        "Uptime": 0
    }
    response = html_request.post(url, data, headers)
    proxylist = []
    root = etree.HTML(response.text)
    proxys = root.xpath(".//table[@id='tblproxy']/tr[position()>2]")
    for proxy in proxys:
        try:
            ip_text = proxy.xpath(".//td[2]/script")[0].text
            ip = ip_text.split("'")[1]
            port_text = proxy.xpath(".//td[3]/script")[0].text
            port = str(int(port_text.split("'")[1], 16))

        except Exception as e:
            print(e)
            continue
        proxy = ":".join([ip, port])
        proxylist.append(proxy)
    print(proxylist)




