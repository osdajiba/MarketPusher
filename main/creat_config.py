#!/usr/bin/python3
# -*- coding:utf-8 -*-

import json
import socket

# Get IP address
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
IP = s.getsockname()[0]
s.close()
print("localhost ip address:", IP)

# 自动创建一个包含用户名、密码、IP地址、需要查询股票tick的代码的字典
config = {
    "username": "",
    "password": "",
    "ip_address": IP,
    "code": ["000005.XSHE", "000001.XSHE", "000025.XSHE", "000034.XSHE", "000017.XSHE", "601988.XSHG"]
}

# 将字典写入JSON文件
with open("config.json", "w") as json_file:
    json.dump(config, json_file, indent=4)

print("config.json file has been created with the configuration.")
