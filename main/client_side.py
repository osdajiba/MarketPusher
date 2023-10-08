#!/usr/bin/python3
# -*- coding:utf-8 -*-

import sys
from optparse import OptionParser
import zmq
import threading
import keyboard
import client
import json


def main():
    socket = client.connect()
    # Create an event to signal the receiver thread to stop
    stop_event = threading.Event()
    recvThread = client.receiver(socket, stop_event)
    recvThread.start()
    client.sendSubscribeRequirement(socket)

    # Function to stop the program when Enter is pressed
    def stop_program(e):
        if e.event_type == keyboard.KEY_DOWN and e.name == "enter":
            print("Enter key pressed. Stopping the program.")
            stop_event.set()  # Set the event to signal the receiver thread to stop
            socket.send_string("stop")
            recvThread.join()  # Wait for the receiver thread to finish
            exit(0)

    keyboard.on_press_key("q", stop_program)

    try:
        while not stop_event.is_set():
            pass
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
