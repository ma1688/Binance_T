# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :Trade_Rest_Api.py
# @Time      :2024/8/11 下午6:31
# @Author    :MA-X-J
# @Software  :PyCharm

"""
api_key = "FXg92Z1e1IVC89WpVosBWT73RenGYaOsUR7PLuQ7YXv9cV6rpPbFWorT2WwaOk5H"
secret_key = "vqrfNjxlKAcmdwpyo47qkUDkINpkL4AiyRQM9ytn9Plc8DgJWkiWg1IFX43fP6XX"
"""

import hashlib
import hmac
import time
import urllib.parse

import httpx

api_key = "FXg92Z1e1IVC89WpVosBWT73RenGYaOsUR7PLuQ7YXv9cV6rpPbFWorT2WwaOk5H"
secret_key = "vqrfNjxlKAcmdwpyo47qkUDkINpkL4AiyRQM9ytn9Plc8DgJWkiWg1IFX43fP6XX"


class TradeRestApi:
    def __init__(self, api_key, secret_key):
        self.url = "https://fapi.binance.com"
        self.api_key = api_key
        self.secret_key = secret_key
        self.timestamp = int(time.time() * 1000)

    def get_signature(self, params):
        params['timestamp'] = self.timestamp
        query_string = urllib.parse.urlencode(params)
        signature = hmac.new(self.secret_key.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
        params['signature'] = signature
        return params



import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# Provided data
data = {
    'e': 'continuous_kline',
    'E': 1723441396148,
    'ps': 'BTCUSDT',
    'ct': 'PERPETUAL',
    'k': {
        't': 1723441380000,
        'T': 1723441439999,
        'i': '1m',
        'f': 5141607623778,
        'L': 5141608694769,
        'o': '58476.00',
        'c': '58488.50',
        'h': '58488.50',
        'l': '58475.90',
        'v': '20.936',
        'n': 445,
        'x': False,
        'q': '1224398.29390',
        'V': '14.412',
        'Q': '842851.12440',
        'B': '0'
    }
}

# Extracting the Kline data
kline = data['k']
open_time = datetime.fromtimestamp(kline['t'] / 1000)
close_time = datetime.fromtimestamp(kline['T'] / 1000)
open_price = float(kline['o'])
close_price = float(kline['c'])
high_price = float(kline['h'])
low_price = float(kline['l'])

# Plotting the candlestick
fig, ax = plt.subplots()
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=1))

# Candlestick representation
ax.plot([open_time, close_time], [open_price, close_price], color='black')
ax.vlines(open_time, low_price, high_price, color='black')
ax.vlines(close_time, low_price, high_price, color='black')

# Adding labels and title
plt.xlabel('Time')
plt.ylabel('Price')
plt.title(f"Continuous Kline Data for {data['ps']} ({data['ct']})")

# Display the plot
plt.grid(True)
plt.show()