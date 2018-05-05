#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : main.py
# @Author: Wanglei
# @Date  : 2018/4/29
# @Desc  :

from multiprocessing import Process
from ProxyValidator import ProxyValidator
from ProxyPool import ProxyPool

import time

def run():
    pool = ProxyPool()
    vaildator = ProxyValidator()
    p_list = []
    p1 = Process(target=pool.update, name="PoxyUpdate")
    p_list.append(p1)
    p2 = Process(target=vaildator.run, name="ProxyVaild")
    p_list.append(p2)

    for p in p_list:
        p.deamon = True
        p.start()

    for p in p_list:
        p.join()



if __name__ == "__main__":
    run()
