#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : HtmlParser.py
# @Author: Wanglei
# @Date  : 2018/5/1
# @Desc  :
import re
from lxml import etree

class HtmlParser:

    def parse(self, response, parser):
        '''
        :param response: 响应
        :param type: 解析方式
        :return:
        '''
        if parser['type'] == 'xpath':
            return self.XpathPraser(response, parser)
        elif parser['type'] == 'regular':
            return self.RegularPraser(response, parser)
        elif parser['type'] == 'module':
            return getattr(self, parser['moduleName'], None)(response, parser)
        else:
            return None


    def XpathPraser(self, response, parser):
        '''
        针对xpath方式进行解析
        :param response:
        :param parser:
        :return:
        '''
        proxylist = []
        root = etree.HTML(response)
        proxys = root.xpath(parser['pattern'])
        for proxy in proxys:
            try:
                ip = proxy.xpath(parser['position']['ip'])[0].text
                port = proxy.xpath(parser['position']['port'])[0].text

            except Exception as e:
                continue
            proxy = ":".join([ip, port])
            proxylist.append(proxy)
        return proxylist


    def RegularPraser(self, response, parser):
        '''
        针对正则表达式进行解析
        :param response:
        :param parser:
        :return:
        '''
        proxylist = []
        pattern = re.compile(parser['pattern'])
        matchs = pattern.findall(response)
        if matchs != None:
            for match in matchs:
                try:
                    ip = match[parser['position']['ip']]
                    port = match[parser['position']['port']]

                except Exception as e:
                    continue
                proxy = ":".join([ip, port])
                proxylist.append(proxy)
            return proxylist