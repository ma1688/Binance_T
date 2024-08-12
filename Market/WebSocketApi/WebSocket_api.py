# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :WebSocket_api.py
# @Time      :2024/8/12 下午5:01
# @Author    :MA-X-J
# @Software  :PyCharm
import asyncio
import json

import websockets


class MarketWebSocket:
    def __init__(self, api_keys, secret_keys):
        # 初始化方法，设置基础URL、API密钥和WebSocket对象
        self.base_url = "wss://fstream.binance.com"
        self.api_key = api_keys
        self.secret_key = secret_keys
        self.ws = None

    async def connect(self, stream_name):
        # 连接到单个WebSocket流
        url = f"{self.base_url}/ws/{stream_name}"
        self.ws = await websockets.connect(url)
        await self.handle_connection()

    async def connect_multiple(self, stream_names):
        # 连接到多个WebSocket流
        streams = "/".join(stream_names)
        url = f"{self.base_url}/stream?streams={streams}"
        self.ws = await websockets.connect(url)
        await self.handle_connection()

    async def handle_connection(self):
        # 处理WebSocket连接，接收消息并打印
        try:
            while True:
                message = await self.ws.recv()
                data = json.loads(message)
                print(f"{data}")
        except websockets.ConnectionClosed:
            # 连接关闭时重新连接
            print("Connection closed, reconnecting...")
            await self.reconnect()

    async def reconnect(self):
        # 重新连接WebSocket
        await asyncio.sleep(5)
        await self.connect(self.stream_name)

    async def send_ping(self):
        # 定期发送ping消息以保持连接
        while True:
            await asyncio.sleep(180)
            await self.ws.ping()

    async def subscribe(self, stream_name):
        # 订阅单个WebSocket流并发送ping消息
        await self.connect(stream_name)
        await asyncio.create_task(self.send_ping())

    async def subscribe_multiple(self, stream_names):
        # 订阅多个WebSocket流并发送ping消息
        await self.connect_multiple(stream_names)
        await asyncio.create_task(self.send_ping())

    async def close(self):
        # 关闭WebSocket连接
        await self.ws.close()


if __name__ == "__main__":
    api_key = "FXg92Z1e1IVC89WpVosBWT73RenGYaOsUR7PLuQ7YXv9cV6rpPbFWorT2WwaOk5H"
    secret_key = "vqrfNjxlKAcmdwpyo47qkUDkINpkL4AiyRQM9ytn9Plc8DgJWkiWg1IFX43fP6XX"
    webs = MarketWebSocket(api_key, secret_key)
    asyncio.run(webs.subscribe("btcusdt_perpetual@continuousKline_1m"))
