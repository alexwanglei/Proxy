#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : ProxyValidor.py
# @Author: Wanglei
# @Date  : 2018/5/2
# @Desc  :

import ssl
import time
from threading import Thread
from queue import Queue
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import config
from logger import logger
from db.RedisClient import RedisClient
from util.HtmlRequest import HtmlRequest

import logging

logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
context = ssl._create_unverified_context()

class ProxyValidator:
    def __init__(self):
        self.proxy_queue = Queue()
        self.logger = logger
        self.html_request = HtmlRequest()
        self.db = RedisClient(config.NAME, config.HOST, config.PORT, config.PASSWORD)

    def start_valid(self, thread_num=10):
        thread_list = []
        for i in range(thread_num):
            thread_list.append(Thread(target=self.vaild, name="check_proxy_thread-%d" % i))
        for thread in thread_list:
            thread.daemon = True
            thread.start()

        for thread in thread_list:
           thread.join()


    def vaild(self):
        while not self.proxy_queue.empty():
            proxy = self.proxy_queue.get()
            if not self.check(proxy):
                self.logger.info("invalid proxy %s", proxy)
                self.db.delete(proxy)

            self.proxy_queue.task_done()


    def run(self):
        self.init_queue()
        while True:
            if not self.proxy_queue.empty():
                self.logger.info("start valid proxy...")
                self.start_valid()
            else:
                self.logger.info("valid complete! wait next valid")
                time.sleep(60 * 10)
                self.init_queue()


    def init_queue(self):
        for item in self.db.get_all():
            self.proxy_queue.put(item)


    def check(self, proxy):
        proxies = {"http": "http://{proxy}".format(proxy=proxy)}
        try:
            # 超过20秒的代理就不要了
            headers = {
                'Host': 'kyfw.12306.cn',
                'Referer': 'https://kyfw.12306.cn/otn/leftTicket/init',
            }
            r = self.html_request.get(config.CHECK_TARGET, header=headers, proxies=proxies)
            # r = requests.get(url=config.CHECK_TARGET, headers=headers, proxies=proxies, timeout=10, verify=False)
            if r.status_code == 200:
                logger.info('%s is ok' % proxy)
                return True
        except Exception as e:
            logger.error(str(e))
            return False



if __name__ == "__main__":
    validator = ProxyValidator()
    validator.run()