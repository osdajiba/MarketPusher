#!/usr/bin/python3
# -*- coding:utf-8 -*-

import re
import threading
import time
import datetime
from multiprocessing import shared_memory
from jqdatasdk import *
import pkgs
import pandas as pd


def getTick(stop_event, dataQueue, shm_name, stopQueue):
    shm_code = shared_memory.SharedMemory(name=shm_name)
    pkgs.authentication()
    while not stop_event.is_set():
        start = time.time()
        if stopQueue.empty():
            List = read_shm_code(shm_code)
            if len(List) > 0:
                allData = pd.DataFrame(get_current_tick(List))
                dataQueue.put(allData)
            end = time.time()
            time.sleep(3 - end + start)
        else:
            stop_event.set()
    shm_code.close()


def read_shm_code(shm_code, pattern=re.compile(r'(\w{6}\.(XSHE|XSHG))')):
    # 使用 decode_binary_list 函数解码共享内存中的数据，并将其添加到列表 codeList 中
    codeList = []
    binary_list = shm_code.buf.tobytes()
    try:
        decoded_data = binary_list.decode('utf-32')
        # 使用正则表达式匹配代码
        matches = pattern.findall(decoded_data)
        # 提取匹配到的代码并添加到列表中
        for match in matches:
            codeList.append(match[0])
    except:
        print("共享内存解码失败")
    finally:
        return codeList
