#!/usr/bin/python3
# -*- coding:utf-8 -*-

from optparse import OptionParser
import socket
from multiprocessing import shared_memory
import zmq
from jqdatasdk import *


# 命令行参数 「-u -p 聚宽账户密码」 「-n 可订阅最大股票数目」 「code 订阅的股票代码」  代码格式：code.market e.g. "000001.XSHE"
def option_parse():
    parser = OptionParser()
    parser.add_option("-u", "--username", dest="username")
    parser.add_option("-p", "--password", dest="password")
    return parser.parse_args()[0]


def createLists():
    List00, List01, List02 = [], [], []
    preDatetime00, preDatetime01, preDatetime02 = [], [], []
    PreClosePrice00, PreClosePrice01, PreClosePrice02 = [], [], []
    OpenPrice00, OpenPrice01, OpenPrice02 = [], [], []
    baseLists = [List00, List01, List02, preDatetime00, preDatetime01, preDatetime02,
                 PreClosePrice00, PreClosePrice01, PreClosePrice02, OpenPrice00, OpenPrice01, OpenPrice02]
    return baseLists


def bind():
    try:
        # Get IP address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        IP = s.getsockname()[0]
        s.close()
        # Socket to talk to server
        context = zmq.Context()
        cur_socket = context.socket(zmq.PAIR)
        cur_socket.bind(f"tcp://{IP}:8080")
        return cur_socket
    except:
        print("Failed to get address IP")
        return False


def authentication():
    auth("18140562236", "Sinoalgo123")


def create_shm_arr(shm_name, string_length=8, total_strings=100, utf32_bytes_per_char=4):
    """
    Create shared memory array
        args initialize:
        length of each string:  string_length,
        total_strings:    string's amount,
        utf32_bytes_per_char:   UTF-32每个字符占4个字节
    """
    shm_size = string_length * total_strings * utf32_bytes_per_char
    shm_arr = shared_memory.SharedMemory(
        create=True, size=shm_size, name=shm_name)
    return shm_arr


def if_i(i, shm00_name, shm01_name, shm02_name, baseLists):
    if i == 0:
        return baseLists[0], baseLists[3], baseLists[6], baseLists[9], shm00_name
    elif i == 1:
        return baseLists[1], baseLists[4], baseLists[7], baseLists[10], shm01_name
    elif i == 2:
        return baseLists[2], baseLists[5], baseLists[8], baseLists[11], shm02_name
    else:
        pass


def if_sendi(i, baseLists):
    if i == 0:
        return baseLists[0], baseLists[3], baseLists[6], baseLists[9]
    elif i == 1:
        return baseLists[1], baseLists[4], baseLists[7], baseLists[10]
    elif i == 2:
        return baseLists[2], baseLists[5], baseLists[8], baseLists[11]
    else:
        pass
