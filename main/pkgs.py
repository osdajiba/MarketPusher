#!/usr/bin/python3
# -*- coding:utf-8 -*-

from optparse import OptionParser
import socket
from multiprocessing import shared_memory
import zmq
from jqdatasdk import *
import json


def createLists():
    List00, List01, List02 = [], [], []
    preDatetime00, preDatetime01, preDatetime02 = [], [], []
    PreClosePrice00, PreClosePrice01, PreClosePrice02 = [], [], []
    OpenPrice00, OpenPrice01, OpenPrice02 = [], [], []
    baseLists = [List00, List01, List02, preDatetime00, preDatetime01, preDatetime02,
                 PreClosePrice00, PreClosePrice01, PreClosePrice02, OpenPrice00, OpenPrice01, OpenPrice02]
    return baseLists


def bind():
    # 读取config.json文件
    with open("config.json", "r") as json_file:
        config = json.load(json_file)
    ip_address = config["ip_address"]
    # Socket to talk to server
    context = zmq.Context()
    cur_socket = context.socket(zmq.PAIR)
    cur_socket.bind(f"tcp://{ip_address}:{8000}")
    return cur_socket


def authentication():
    # 读取config.json文件
    with open("config.json", "r") as json_file:
        config = json.load(json_file)
    password = config["password"]
    username = config["username"]
    auth(username, password)


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
