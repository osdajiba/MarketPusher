#!/usr/bin/python3
# -*- coding:utf-8 -*-

import socket
import zmq
import threading
import openpyxl as opxl
import json


def sendSubscribeRequirement(socket):
    with open("config.json", "r") as json_file:
        config = json.load(json_file)
    codeList = config["code"]
    print("需要订阅的股票代码：", codeList)
    for code in codeList:
        split_result = code.split(".")
        requireStr = "{\"api\":\"SubscribeMarketData\","
        requireStr += "\"symbol\":" + "\"" + split_result[0] + "\"" + ","
        requireStr += "\"market\":" + "\"" + split_result[1] + "\"" + "}"
        socket.send_string(requireStr)


def connect():
    # 读取config.json文件
    with open("config.json", "r") as json_file:
        config = json.load(json_file)
    ip_address = config["ip_address"]
    # Socket to talk to server
    context = zmq.Context()
    cur_socket = context.socket(zmq.PAIR)
    cur_socket.connect(f"tcp://{ip_address}:{8000}")
    return cur_socket


class receiver(threading.Thread):
    def __init__(self, socket_, stop_event):
        threading.Thread.__init__(self)
        self.socket = socket_
        self.stop_event = stop_event

    def run(self):
        # wb, ws = build_excel("stockData")
        while not self.stop_event.is_set():
            try:
                message = self.socket.recv_string()
                print(message)
            except zmq.error.ZMQError:
                pass
