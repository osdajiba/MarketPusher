#!/usr/bin/python3
# -*- coding:utf-8 -*-

import time
import zmq
import pkgs
import pandas as pd


def send(stop_event, socket, dataQueue, stopQueue, num, baseLists):
    codeList, preDatetime, PreClosePrice, OpenPrice = pkgs.if_sendi(num, baseLists)
    while not stop_event.is_set():
        start = time.time()
        if stopQueue.empty():
            if dataQueue.empty():
                pass
            else:
                data = dataQueue.get(False)
                print(data)
                for i in range(len(data)):
                    quoteStr = ""
                    quoteStr += "{"
                    quoteStr += "\"api\":\"OnMarketData\","
                    quoteStr += "\"LowestPrice\":" + format(data.low.iloc[i]) + ","
                    quoteStr += "\"HighestPrice\":" + format(data.high.iloc[i]) + ","
                    if len(data) == 1:
                        split_result = codeList[0].split(".")
                        quoteStr += "\"symbol\":" + "\"" + split_result[0] + "\"" + ","
                        quoteStr += "\"market\":" + "\"" + split_result[1] + "\"" + ","
                        quoteStr += "\"PreClosePrice\":" + PreClosePrice[0] + ","
                        quoteStr += "\"OpenPrice\":" + OpenPrice[0] + ","
                    else:
                        split_result = data.index[i].split(".")
                        quoteStr += "\"symbol\":" + "\"" + split_result[0] + "\"" + ","
                        quoteStr += "\"market\":" + "\"" + split_result[1] + "\"" + ","
                        quoteStr += "\"PreClosePrice\":" + PreClosePrice[i] + ","
                        quoteStr += "\"OpenPrice\":" + OpenPrice[i] + ","
                    quoteStr += "\"LastPrice\":" + format(data.current.iloc[i]) + ","
                    quoteStr += "\"Volume\":" + format(data.volume.iloc[i]) + ","
                    quoteStr += "\"Turnover\":" + format(data.money.iloc[i]) + ","
                    quoteStr += "\"UpdateTime\":" + "\"" + format(
                        data.datetime.iloc[i].strftime('%H:%M:%S')) + "\"" + ","
                    quoteStr += "\"BidPrice1\":" + format(data.b1_p.iloc[i]) + ","
                    quoteStr += "\"BidVolume1\":" + format(data.b1_v.iloc[i]) + ","
                    quoteStr += "\"AskPrice1\":" + format(data.a1_p.iloc[i]) + ","
                    quoteStr += "\"AskVolume1\":" + format(data.a1_v.iloc[i]) + ","
                    quoteStr += "\"BidPrice2\":" + format(data.b2_p.iloc[i]) + ","
                    quoteStr += "\"BidVolume2\":" + format(data.b2_v.iloc[i]) + ","
                    quoteStr += "\"AskPrice2\":" + format(data.a2_p.iloc[i]) + ","
                    quoteStr += "\"AskVolume2\":" + format(data.a2_v.iloc[i]) + ","
                    quoteStr += "\"BidPrice3\":" + format(data.b3_p.iloc[i]) + ","
                    quoteStr += "\"BidVolume3\":" + format(data.b3_v.iloc[i]) + ","
                    quoteStr += "\"AskPrice3\":" + format(data.a3_p.iloc[i]) + ","
                    quoteStr += "\"AskVolume3\":" + format(data.a3_v.iloc[i]) + ","
                    quoteStr += "\"BidPrice4\":" + format(data.b4_p.iloc[i]) + ","
                    quoteStr += "\"BidVolume4\":" + format(data.b4_v.iloc[i]) + ","
                    quoteStr += "\"AskPrice4\":" + format(data.a4_p.iloc[i]) + ","
                    quoteStr += "\"AskVolume4\":" + format(data.a4_v.iloc[i]) + ","
                    quoteStr += "\"BidPrice5\":" + format(data.b5_p.iloc[i]) + ","
                    quoteStr += "\"BidVolume5\":" + format(data.b5_v.iloc[i]) + ","
                    quoteStr += "\"AskPrice5\":" + format(data.a5_p.iloc[i]) + ","
                    quoteStr += "\"AskVolume5\":" + format(data.a5_v.iloc[i])
                    quoteStr += "}"
                    socket.send_string(quoteStr)
            end = time.time()
            time.sleep(3 - end + start)
            print("发送订阅，线程运行时间间隔:{}秒".format(3 - end + start))
        else:
            stop_event.set()
    socket.close()
