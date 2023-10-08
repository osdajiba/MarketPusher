#!/usr/bin/python3
# -*- coding:utf-8 -*-
import datetime
import threading
import time
from multiprocessing import shared_memory
import json
import pandas as pd
from jqdatasdk import *
from chinese_calendar import is_workday
import exchange_calendars as trade_date
import pkgs

XSHG = trade_date.get_calendar("XSHG")


def receive(stop_event, socket, shm00_name, shm01_name, shm02_name, stopQueue, baseLists):
    subscribeList = []
    if is_workday(datetime.date.today()):
        while not stop_event.is_set():
            start = time.time()
            message = socket.recv_string()
            print(message)
            if message == "stop":
                stop_event.set()
                stopQueue.put(True)
                continue
            msgJson = json.loads(message)
            code = msgJson["symbol"] + "." + msgJson["market"]
            try:
                if code not in subscribeList:
                    subscribeList.append(code)
                    List, preDatetime, PreClosePrice, OpenPrice, shm_name = classify(code, shm00_name, shm01_name,
                                                                                     shm02_name, baseLists)
                    write_to_shm(List, shm_name)
            except:
                print("handle msg error \t time:")
            finally:
                end = time.time()
                print("接收订阅列表，线程运行耗时:", end - start)
    else:
        while not stop_event.is_set():
            not_tradeDate(socket, subscribeList, stop_event, stopQueue)
            socket.close()


def not_tradeDate(socket, subscribeList, stop_event, stopQueue):
    PreClosePrice, OpenPrice = [], []
    pkgs.authentication()
    print("Today is NOT trade date!")
    while not stop_event.is_set():
        message = socket.recv_string()
        print(message)
        try:
            msgJson = json.loads(message)
            code = msgJson["symbol"] + "." + msgJson["market"]
            if message == "Stop the program !":
                stop_event.set()
            if code not in subscribeList:
                subscribeList.append(code)
                PreClosePrice.append(format(
                    get_price(code, start_date=XSHG.previous_close(datetime.date.today()),
                              end_date=XSHG.previous_close(datetime.date.today()), fields=['close']).close[0]))
                OpenPrice.append(format(
                    get_price(code, XSHG.previous_close(datetime.date.today()),
                              end_date=XSHG.previous_close(datetime.date.today()),
                              fields=['open']).open[0]))
            if len(subscribeList) > 0:
                for i in range(len(subscribeList)):
                    quoteStr = ""
                    quoteStr += "\"symbol\":" + "\"" + subscribeList[i].split('.')[0] + "\"" + ","
                    quoteStr += "\"market\":" + "\"" + subscribeList[i].split('.')[1] + "\"" + ","
                    quoteStr += "\"PreClosePrice\":" + PreClosePrice[i] + ","
                    quoteStr += "\"OpenPrice\":" + OpenPrice[i] + ","
                    print(quoteStr)
                    socket.recv_string(quoteStr)
        except:
            print("handle msg error \t time:", datetime.date.today())


def classify(code, shm00_name, shm01_name, shm02_name, baseLists):
    pkgs.authentication()
    data = get_current_tick(code)
    timeData = pd.to_datetime(data['datetime'])
    second = timeData.iloc[0].second
    List, preDatetime, PreClosePrice, OpenPrice, shm_name = pkgs.if_i(int(second) % 3, shm00_name, shm01_name,
                                                                      shm02_name, baseLists)
    List.append(code)
    preDatetime.append(timeData.iloc[0])
    PreClosePrice.append(format(
        get_price(code, start_date=XSHG.previous_close(datetime.date.today()),
                  end_date=XSHG.previous_close(datetime.date.today()), fields=['close']).close.iloc[0]))
    OpenPrice.append(format(
        get_price(code, start_date=datetime.date.today(), end_date=datetime.date.today(),
                  fields=['open']).open.iloc[0]))
    return List, preDatetime, PreClosePrice, OpenPrice, shm_name


def write_to_shm(codeList, shm_name="wnsm_a994d2ea"):
    existing_shm = shared_memory.SharedMemory(shm_name)
    try:
        # 获取共享内存数组的长度
        arr_length = existing_shm.size

        # 将 codeList 中的每个字符串编码为 UTF-32 格式的字节序列，并将结果存储在 encoded_data 列表中
        encoded_data = [code.encode('utf-32') for code in codeList]
        # 确保编码后的数据总长度不超过共享内存数组的长度
        total_data_length = sum(len(data) for data in encoded_data)
        if total_data_length <= arr_length:
            offset = 0
            for data in encoded_data:
                data_len = len(data)
                if offset + data_len <= arr_length:
                    existing_shm.buf[offset:offset + data_len] = data
                    offset += data_len
                else:
                    raise ValueError("共享内存空间不足以容纳所有数据")
        else:
            raise ValueError("编码后的数据总长度超出了共享内存数组的长度")
        existing_shm.close()
    except Exception as e:
        # 在发生异常时进行错误处理
        print(f"写入共享内存时发生异常：{str(e)}")
