#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : ProxyPool.py
# @Author: Wanglei
# @Date  : 2018/5/1
# @Desc  :

import requests

from logger import logger
from config import parserList
from util.HtmlRequest import HtmlRequest
from util.HtmlParser import HtmlParser

class ProxyPool:
    def __init__(self):
        self.logger = logger
        self.html_request = HtmlRequest()
        self.html_parser = HtmlParser()

    def refresh(self):
        """
        刷新代理池
        :return:
        """
        pass


    def crawl(self):
        for parser in parserList:
            for url in parser['urls']:
                response = self.html_request.get(url)
                if response:
                    proxy_list = self.html_parser.parse(response, parser)
                    if proxy_list:
                        self.logger.info("get %d proxy from %s", len(proxy_list), url)
                        for proxy in proxy_list:
                            if self.vaild(proxy):
                                # save proxy
                                self.logger.info("get a vaild proxy: %s", proxy)





    def vaild(self, proxy):
        proxies = {"http": "http://{proxy}".format(proxy=proxy)}
        try:
            # 超过20秒的代理就不要了
            r = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=10, verify=False)
            if r.status_code == 200:
                # logger.info('%s is ok' % proxy)
                return True
        except Exception as e:
            # logger.error(str(e))
            return False


if __name__ == "__main__":
    pool = ProxyPool()
    pool.crawl()


