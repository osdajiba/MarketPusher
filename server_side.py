#!/usr/bin/python3
# -*- coding:utf-8 -*-

import threading
from multiprocessing import Queue, Process, Event, shared_memory
from optparse import OptionParser
import pkgs
import getTicker
import sender
import receiver


def main():
    baseLists = pkgs.createLists()
    shm00 = pkgs.create_shm_arr("wnsm_second00", total_strings=100)
    shm01 = pkgs.create_shm_arr("wnsm_second01", total_strings=100)
    shm02 = pkgs.create_shm_arr("wnsm_second02", total_strings=100)
    shmArr00 = shared_memory.SharedMemory(name="wnsm_second00")
    shmArr01 = shared_memory.SharedMemory(name="wnsm_second01")
    shmArr02 = shared_memory.SharedMemory(name="wnsm_second02")
    dataQueue00 = Queue()
    dataQueue01 = Queue()
    dataQueue02 = Queue()
    stopQueue = Queue()
    stop_event = Event()
    socket = pkgs.bind()
    pkgs.authentication()

    # 创建子进程
    getList, sendList = [], []
    for i in range(3):
        if i == 0:
            shm_name = shmArr00.name
            dataQueue = dataQueue00
        elif i == 1:
            shm_name = shmArr01.name
            dataQueue = dataQueue01
        else:
            shm_name = shmArr02.name
            dataQueue = dataQueue02
        getTick_process = Process(target=getTicker.getTick, args=(stop_event, dataQueue, shm_name, stopQueue))
        sendThread = threading.Thread(target=sender.send, args=(
            stop_event, socket, dataQueue, stopQueue, i, baseLists))
        sendList.append(sendThread)
        getList.append(getTick_process)
        getTick_process.start()
        sendThread.start()

    receiveThread = threading.Thread(target=receiver.receive, args=(
        stop_event, socket, shm00.name, shm01.name, shm02.name, stopQueue, baseLists))
    receiveThread.start()

    # 清除内存数据,等待子进程完成, 结束进程
    shm00.close()
    shm01.close()
    shm02.close()
    shm00.unlink()
    shm01.unlink()
    shm02.unlink()
    for i in range(3):
        getList[i].join()
        sendList[i].join()
    receiveThread.join()


if __name__ == '__main__':
    main()
