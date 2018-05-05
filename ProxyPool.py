#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : ProxyPool.py
# @Author: Wanglei
# @Date  : 2018/5/1
# @Desc  :
from gevent import monkey
monkey.patch_all()

import gevent
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import time
from lxml import etree
from logger import logger
import config
from util.HtmlRequest import HtmlRequest
from util.HtmlParser import HtmlParser
from db.RedisClient import RedisClient

import logging

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class ProxyPool:
    def __init__(self):
        self.logger = logger
        self.db = RedisClient(config.NAME, config.HOST, config.PORT, config.PASSWORD)
        self.html_request = HtmlRequest()
        self.html_parser = HtmlParser()

    def update(self):
        """
        更新代理池
        :return:
        """
        while True:
            if self.db.nums() < config.PROXY_MINNUM:
                self.logger.info("db exists ip:%d, less the minnum, start crawling proxy..." % self.db.nums())
                spawns = []
                gevent.spawn(self.crawl_gatherproxy)
                # for parser in config.parserList:
                #     spawns.append(gevent.spawn(self.crawl, parser))
                #     if len(spawns) >= config.MAX_DOWNLOAD_CONCURRENT:
                #         gevent.joinall(spawns)
                #         spawns = []
                gevent.joinall(spawns)
            else:
                self.logger.info("db exists ip:%d, enough to use, wait next update..." % self.db.nums())
            time.sleep(config.UPDATE_TIME)

    def crawl(self, parser):
        for url in parser['urls']:
            response = self.html_request.get(url)
            if response:
                proxy_list = self.html_parser.parse(response.text, parser)
                if proxy_list:
                    self.logger.info("get %d proxy from %s", len(proxy_list), url)
                    for proxy in proxy_list:
                        if self.vaild(proxy):
                            # save proxy
                            self.logger.info("get a vaild proxy: %s", proxy)
                            self.db.put(proxy)


    def crawl_gatherproxy(self):
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
        url = 'http://www.gatherproxy.com/proxylist/country/?c=China'
        data = {
            "Country": "china",
            "PageIdx": 1,
            "Filter": '',
            "Uptime": 0
        }
        for page in range(1, 40):
            data['PageIdx'] = page
            response = self.html_request.post(url, data, headers)
            proxy_list = []
            root = etree.HTML(response.text)
            proxys = root.xpath(".//table[@id='tblproxy']/tr[position()>2]")
            for proxy in proxys:
                try:
                    ip_text = proxy.xpath(".//td[2]/script")[0].text
                    ip = ip_text.split("'")[1]
                    port_text = proxy.xpath(".//td[3]/script")[0].text
                    port = str(int(port_text.split("'")[1], 16))
                except Exception as e:
                    self.logger.error("parse proxy error: ", e)
                    continue
                proxy = ":".join([ip, port])
                proxy_list.append(proxy)
            if proxy_list:
                self.logger.info("get %d proxy from %s", len(proxy_list), url)
                for proxy in proxy_list:
                    if self.vaild(proxy):
                        # save proxy
                        self.logger.info("get a vaild proxy: %s", proxy)
                        self.db.changeTable("gatherproxy")
                        self.db.put(proxy)


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
    start = time.time()
    pool = ProxyPool()
    pool.update()
    end = time.time()
    print("use time ", end-start)
    # print("ip proxy number ", pool.db.nums())
    # print("get a proxy ", pool.db.get())



