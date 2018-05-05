#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : config.py
# @Author: Wanglei
# @Date  : 2018/4/29
# @Desc  :
import os
from configparser import ConfigParser

MINNUM_PROXY = 100  # 当有效的代理数目小于该值 需要启动爬虫进行爬取

PAGE_PROXY = 10

FLUSH_TIME = 600   # 刷新代理的周期

'''
数据库的配置
'''
HOST = "101.200.38.103"
PORT = 6379
NAME = "proxy"
PASSWORD = "fromtrain!QAZ"

DB_CONFIG = {
    'MYSQL_DB_URL': 'mysql+mysqldb://root:root@localhost/proxy?charset=utf8',
    'REDIS_DB_URL': 'redis://:fromtrain!QAZ@101.200.38.103:6379/9',
}

MAX_DOWNLOAD_CONCURRENT = 10
PROXY_MINNUM = 500
UPDATE_TIME = 30 * 60

CHECK_TARGET = 'https://kyfw.12306.cn/otn/leftTicket/init'


parserList = [
    {
        'urls': ['http://www.mimiip.com/gngao/%s' % n for n in range(1, 10)],
        'type': 'xpath',
        'pattern': ".//table[@class='list']/tr",
        'position': {'ip': './td[1]', 'port': './td[2]', 'type': '', 'protocol': ''}

    },
    {
        'urls': ['http://www.kuaidaili.com/ops/proxylist/%s/' % n for n in range(1, 11)],
        'type': 'xpath',
        'pattern': ".//*[@id='freelist']/table/tbody/tr[position()>0]",
        'position': {'ip': './td[1]', 'port': './td[2]', 'type': './td[3]', 'protocol': './td[4]'}
    },
    {
        'urls': ['http://www.cz88.net/proxy/%s' % m for m in
                 ['index.shtml'] + ['http_%s.shtml' % n for n in range(2, 11)]],
        'type': 'xpath',
        'pattern': ".//*[@id='boxright']/div/ul/li[position()>1]",
        'position': {'ip': './div[1]', 'port': './div[2]', 'type': './div[3]', 'protocol': ''}

    },
    {
        'urls': ['http://www.xicidaili.com/%s/%s' % (m, n) for m in ['nn', 'nt', 'wn', 'wt'] for n in range(1, 8)],
        'type': 'xpath',
        'pattern': ".//*[@id='ip_list']/tr[position()>1]",
        'position': {'ip': './td[2]', 'port': './td[3]', 'type': './td[5]', 'protocol': './td[6]'}
    },
    {
        'urls': ['http://www.66ip.cn/%s.html' % n for n in ['index'] + list(range(2, 12))],
        'type': 'xpath',
        'pattern': ".//*[@id='main']/div/div[1]/table/tr[position()>1]",
        'position': {'ip': './td[1]', 'port': './td[2]', 'type': './td[4]', 'protocol': ''}
    }
]


class Config:
    def __init__(self):
        self.pwd = os.path.split(os.path.realpath(__file__))[0]
        self.config_path = os.path.join(self.pwd, 'dev.cfg')
        self.config_file = ConfigParser()
        self.config_file.read(self.config_path)


    def proxy_getter_funs(self):
        return self.config_file.options('ProxyGetter')


if __name__ == "__main__":
    config = Config()
    print(config.pwd)