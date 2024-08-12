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

    async def aggTrade(self, symbol):
        """
        归集交易
        数据流描述 同一价格、同一方向、同一时间(100ms计算)的trade会被聚合为一条.
        更新速度  100ms

        :param symbol:
        :return:
        """
        stream_name = f"{symbol}@aggTrade"
        await self.subscribe(stream_name)

    async def latestMarkPrice(self, symbol, update_speed="1000ms"):
        """
        最新标记价格
        数据流描述 最新标记价格
        更新速度  3000ms 或 1000ms

        :param symbol: 交易对
        :param update_speed: 更新速度 ("3000ms" 或 "1000ms")
        :return:
        """
        if update_speed == "1000ms":
            stream_name = f"{symbol}@markPrice@1s"
        else:
            stream_name = f"{symbol}@markPrice"
        await self.subscribe(stream_name)

    async def latestMarkPriceAll(self, update_speed="1000ms"):
        """
        全市场最新标记价格
        数据流描述 全市场最新标记价格
        更新速度  3000ms 或 1000ms

        :param update_speed: 更新速度 ("3000ms" 或 "1000ms")
        :return:
        """
        if update_speed == "1000ms":
            stream_name = "!markPrice@arr@1s"
        else:
            stream_name = "!markPrice@arr"
        await self.subscribe(stream_name)

    async def kline(self, symbol, interval):
        """
        K线
        数据流描述 K线stream逐秒推送所请求的K线种类(最新一根K线)的更新。推送间隔250毫秒(如有刷新)

        :param symbol: 交易对
        :param interval: 时间间隔 ("1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1M")
        :return:
        """
        stream_name = f"{symbol}@kline_{interval}"
        await self.subscribe(stream_name)

    async def continuousKline(self, pair, contract_type, interval):
        """
        连续合约K线
        数据流描述 K线stream逐秒推送所请求的K线种类(最新一根K线)的更新。

        :param pair: 交易对
        :param contract_type: 合约类型 ("perpetual", "current_quarter", "next_quarter")
        :param interval: 时间间隔 ("1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1M")
        :return:
        """
        stream_name = f"{pair}_{contract_type}@continuousKline_{interval}"
        await self.subscribe(stream_name)

    async def miniTicker(self, symbol):
        """
        按交易对的精简Ticker
        数据流描述 按Symbol刷新的24小时精简ticker信息.

        :param symbol: 交易对
        :return:
        """
        stream_name = f"{symbol}@miniTicker"
        await self.subscribe(stream_name)

    async def fullTickerAll(self):
        """
        全市场的完整Ticker
        数据流描述 所有symbol 24小时完整ticker信息.需要注意的是，只有发生变化的ticker更新才会被推送。

        :return:
        """
        stream_name = "!ticker@arr"
        await self.subscribe(stream_name)

    async def fullTicker(self, symbol):
        """
        按Symbol的完整Ticker
        数据流描述 按Symbol刷新的24小时完整ticker信息

        :param symbol: 交易对
        :return:
        """
        stream_name = f"{symbol}@ticker"
        await self.subscribe(stream_name)

    async def miniTickerAll(self):
        """
        全市场的精简Ticker
        数据流描述 所有symbol24小时精简ticker信息.需要注意的是，只有发生变化的ticker更新才会被推送。

        :return:
        """
        stream_name = "!miniTicker@arr"
        await self.subscribe(stream_name)

    async def bookTicker(self, symbol):
        """
        按Symbol的最优挂单信息
        数据流描述 实时推送指定交易对最优挂单信息

        :param symbol: 交易对
        :return:
        """
        stream_name = f"{symbol}@bookTicker"
        await self.subscribe(stream_name)

    async def bookTickerAll(self):
        """
        全市场最优挂单信息
        数据流描述 所有交易对交易对最优挂单信息

        :return:
        """
        stream_name = "!bookTicker"
        await self.subscribe(stream_name)

    async def forceOrder(self, symbol):
        """
        强平订单
        数据流描述 推送特定symbol的强平订单快照信息。 1000ms内至多仅推送一条最近的强平订单作为快照

        :param symbol: 交易对
        :return:
        """
        stream_name = f"{symbol}@forceOrder"
        await self.subscribe(stream_name)

    async def forceOrderAll(self):
        """
        全市场强平订单
        数据流描述 推送全市场强平订单快照信息 每个symbol，1000ms内至多仅推送一条最近的强平订单作为快照

        :return:
        """
        stream_name = "!forceOrder@arr"
        await self.subscribe(stream_name)

    async def depth(self, symbol, levels, update_speed="250ms"):
        """
        有限档深度信息
        数据流描述 推送有限档深度信息。levels表示几档买卖单信息, 可选 5/10/20档

        :param symbol: 交易对
        :param levels: 档数 (5, 10, 20)
        :param update_speed: 更新速度 ("250ms", "500ms", "100ms")
        :return:
        """
        if update_speed == "250ms":
            stream_name = f"{symbol}@depth{levels}"
        else:
            stream_name = f"{symbol}@depth{levels}@{update_speed}"
        await self.subscribe(stream_name)

    async def incrementalDepth(self, symbol, update_speed="250ms"):
        """
        增量深度信息
        数据流描述 orderbook 的变化部分，推送间隔 250 毫秒,500 毫秒，100 毫秒(如有刷新)

        :param symbol: 交易对
        :param update_speed: 更新速度 ("250ms", "500ms", "100ms")
        :return:
        """
        if update_speed == "250ms":
            stream_name = f"{symbol}@depth"
        else:
            stream_name = f"{symbol}@depth@{update_speed}"
        await self.subscribe(stream_name)

    async def compositeIndex(self, symbol):
        """
        综合指数交易对信息流
        数据流描述 获取交易对为综合指数的基础成分信息。 推送间隔1000毫秒(如有刷新)

        :param symbol: 交易对
        :return:
        """
        stream_name = f"{symbol}@compositeIndex"
        await self.subscribe(stream_name)

    async def assetIndex(self, asset_symbol=None):
        """
        多资产模式资产汇率指数
        数据流描述 多资产模式资产价格指数

        :param asset_symbol: 资产对 (可选)
        :return:
        """
        if asset_symbol:
            stream_name = f"{asset_symbol}@assetIndex"
        else:
            stream_name = "!assetIndex@arr"
        await self.subscribe(stream_name)

    async def contractInfo(self):
        """
        交易对信息信息流
        数据流描述 Symbol状态更改时推送（上架/下架/bracket调整）; bks仅在bracket调整时推出。

        :return:
        """
        stream_name = "!contractInfo"
        await self.subscribe(stream_name)


if __name__ == "__main__":
    api_key = "FXg92Z1e1IVC89WpVosBWT73RenGYaOsUR7PLuQ7YXv9cV6rpPbFWorT2WwaOk5H"
    secret_key = "vqrfNjxlKAcmdwpyo47qkUDkINpkL4AiyRQM9ytn9Plc8DgJWkiWg1IFX43fP6XX"
    webs = MarketWebSocket(api_key, secret_key)
    asyncio.run(webs.latestMarkPrice("btcusdt"))
