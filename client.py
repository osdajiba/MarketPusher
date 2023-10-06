#!/usr/bin/python3
# -*- coding:utf-8 -*-

import socket
import zmq
import threading
import openpyxl as opxl


def connect():
    try:
        # Get IP address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        IP = s.getsockname()[0]
        s.close()
        # Socket to talk to server
        context = zmq.Context()
        cur_socket = context.socket(zmq.PAIR)
        cur_socket.connect(f"tcp://{IP}:{8080}")
        return cur_socket
    except:
        print("Failed to get address IP")
        return False


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




