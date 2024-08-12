# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :Market_Rest_WebSocket.py
# @Time      :2024/8/10 下午5:44
# @Author    :MA-X-J
# @Software  :PyCharm
import asyncio
import json

import httpx
import websockets

api_key = "FXg92Z1e1IVC89WpVosBWT73RenGYaOsUR7PLuQ7YXv9cV6rpPbFWorT2WwaOk5H"
secret_key = "vqrfNjxlKAcmdwpyo47qkUDkINpkL4AiyRQM9ytn9Plc8DgJWkiWg1IFX43fP6XX"


class MarketRestApi:

    def __init__(self, proxy=None):
        self.rest_base_url = "https://fapi.binance.com"
        self.proxy = proxy
        self.client = httpx.Client(proxies=proxy)

    async def test_ping(self):
        """
        测试服务器是否正常
        :return:  {}
        """
        return self.client.get(url=self.rest_base_url + "/fapi/v1/ping").json()

    async def get_server_time(self):
        """
        获取服务器时间
        :return:  {'serverTime': 1723285908488}
        """
        return self.client.get(url=self.rest_base_url + "/fapi/v1/time").json()

    async def get_exchange_info(self):
        """
        获取交易对信息

        :return:  {}
        """
        return self.client.get(url=self.rest_base_url + "/fapi/v1/exchangeInfo").json()

    async def get_order_book(self, symbol, limit=5):
        """
        获取深度信息
        :param symbol: 交易对
        :param limit: 档数  默认 500; 可选值:[5, 10, 20, 50, 100, 500, 1000]
        :return:
        """
        return self.client.get(url=self.rest_base_url + "/fapi/v1/depth",
                               params={"symbol": symbol, "limit": limit}).json()

    async def get_recent_trades(self, symbol, limit=500):
        """
        获取最新成交
        :param symbol: 交易对
        :param limit: 档数 默认:500，最大1000
        :return:  {}
        """
        return self.client.get(url=self.rest_base_url + "/fapi/v1/trades",
                               params={"symbol": symbol, "limit": limit}).json()

    async def get_historical_trades(self, symbol, limit=500, fromId=None):
        """
        获取历史成交  需要API-key
        :param symbol: 交易对
        :param limit: 档数 默认值:500 最大值:1000.
        :param fromId:  从哪一条成交id开始返回. 缺省返回最近的成交记录
        :return:  {}
        """
        return self.client.get(url=self.rest_base_url + "/fapi/v1/historicalTrades",
                               params={"symbol": symbol, "limit": limit, "fromId": fromId}).json()

    async def get_aggregate_trades_list(self, symbol, fromId=None, startTime=None, endTime=None, limit=500):
        """
        获取聚合成交
        :param symbol: 交易对
        :param fromId: 从包含fromID的成交开始返回结果
        :param startTime:  从该时刻之后的成交记录开始返回结果
        :param endTime: 返回该时刻为止的成交记录
        :param limit: 档数  默认 500; 最大 1000.
        :return:  {}

        如果同时发送startTime和endTime，间隔必须小于一小时
        如果没有发送任何筛选参数(fromId, startTime, endTime)，默认返回最近的成交记录
        保险基金和自动减仓(ADL)成交不属于订单簿成交，故不会被归并聚合
        同时发送startTime/endTime和fromId可能导致请求超时，建议仅发送fromId或仅发送startTime和endTime
        """
        return self.client.get(url=self.rest_base_url + "/fapi/v1/aggTrades",
                               params={"symbol": symbol, "fromId": fromId, "startTime": startTime, "endTime": endTime,
                                       "limit": limit}).json()

    async def get_candlestick_data(self, symbol, interval, startTime=None, endTime=None, limit=500):
        """
        获取K线数据
        :param symbol: 交易对
        :param interval: 时间间隔
        :param fromId: 从包含fromID的成交开始返回结果
        :param startTime:  从该时刻之后的成交记录开始返回结果
        :param endTime: 返回该时刻为止的成交记录
        :param limit: 档数  默认 500; 最大 1000.
        :return:  {}

        LIMIT参数	权重
            [1,100)	1
            [100, 500)	2
            [500, 1000]	5
            > 1000	10
        """
        return self.client.get(url=self.rest_base_url + "/fapi/v1/klines",
                               params={"symbol": symbol, "interval": interval, "startTime": startTime,
                                       "endTime": endTime, "limit": limit}).json()

    async def get_continuous_Klines(self, pair, contractType, interval, startTime=None, endTime=None, limit=500):
        """
        *****************************************
        合约类型:
        PERPETUAL 永续合约
        CURRENT_QUARTER 当季交割合约
        NEXT_QUARTER 次季交割合约
        ******************************************
        获取合约K线数据
        :param pair: 交易对  NY必须参数
        :param contractType: 合约类型  NY必须参数
        :param interval: 时间间隔   NY必须参数
        :param startTime: 起始时间  NN
        :param endTime: 结束时间  NN
        :param limit: 档数  默认值:500 最大值:1500  NN
        :return:  {}
        """
        return self.client.get(url=self.rest_base_url + "/fapi/v1/continuousKlines",
                               params={"pair": pair, "contractType": contractType, "interval": interval,
                                       "startTime": startTime, "endTime": endTime, "limit": limit}).json()

    async def get_index_price_klines(self, pair, interval, startTime=None, endTime=None, limit=500):
        """
        获取价格指数K线数据
        :param pair: 标的交易对
        :param interval: 时间间隔
        :param startTime: 起始时间
        :param endTime: 结束时间
        :param limit: 档数 默认值:500 最大值:1500
        :return:  {}
        """
        return self.client.get(url=self.rest_base_url + "/fapi/v1/indexPriceKlines",
                               params={"pair": pair, "interval": interval, "startTime": startTime, "endTime": endTime,
                                       "limit": limit}).json()

    async def get_mark_price_klines(self, symbol, interval, startTime=None, endTime=None, limit=500):
        """
        获取标记价格K线数据
        :param symbol: 交易对
        :param interval: 时间间隔
        :param startTime: 起始时间
        :param endTime: 结束时间
        :param limit: 档数 默认值:500 最大值:1500
        :return:  {}
        """
        return self.client.get(url=self.rest_base_url + "/fapi/v1/markPriceKlines",
                               params={"symbol": symbol, "interval": interval, "startTime": startTime,
                                       "endTime": endTime, "limit": limit}).json()

    async def get_premium_index_klines(self, symbol, interval, startTime=None, endTime=None, limit=500):
        """
        获取溢价指数K线数据
        :param symbol: 交易对
        :param interval: 时间间隔
        :param startTime: 起始时间
        :param endTime: 结束时间
        :param limit: 档数 默认值:500 最大值:1500
        :return:  {}
        """
        return self.client.get(url=self.rest_base_url + "/fapi/v1/premiumIndexKlines",
                               params={"symbol": symbol, "interval": interval, "startTime": startTime,
                                       "endTime": endTime, "limit": limit}).json()

    async def get_premium_index(self, symbol=None):
        """
        获取最新标记价格和资金费率
        :param symbol: 交易对
        :return:  {}
        """
        return self.client.get(url=self.rest_base_url + "/fapi/v1/premiumIndex", params={"symbol": symbol}).json()

    async def get_funding_rate_history(self, symbol=None, startTime=None, endTime=None, limit=100):
        """
        查询资金费率历史
        :param symbol: 交易对
        :param startTime: 起始时间
        :param endTime: 结束时间
        :param limit: 默认值:100 最大值:1000
        :return: {}
        """
        params = {
            "symbol": symbol,
            "startTime": startTime,
            "endTime": endTime,
            "limit": limit
        }
        return self.client.get(url=self.rest_base_url + "/fapi/v1/fundingRate", params=params).json()

    async def get_funding_info(self, symbol=None):
        """

        查询资金费率信息
        :param symbol: 交易对
        :return: {}
        """
        return self.client.get(url=self.rest_base_url + "/fapi/v1/fundingInfo", params={'symbol': symbol}).json()

    async def get_24hr_ticker(self, symbol=None):
        """
        获取24小时价格变动情况
        :param symbol: 交易对
        :return: {}
        """
        params = {"symbol": symbol} if symbol else {}
        return self.client.get(url=self.rest_base_url + "/fapi/v1/ticker/24hr", params=params).json()

    async def get_latest_price(self, symbol=None):
        """
        获取最新价格
        :param symbol: 交易对
        :return: {}
        """
        params = {"symbol": symbol} if symbol else {}
        return self.client.get(url=self.rest_base_url + "/fapi/v1/ticker/price", params=params).json()

    async def get_latest_price_V2(self, symbol=None):
        """
        获取最新价格V2
        :param symbol: 交易对
        :return: {}
        """
        params = {"symbol": symbol} if symbol else {}
        return self.client.get(url=self.rest_base_url + "/fapi/v2/ticker/price", params=params).json()

    async def get_best_order(self, symbol=None):
        """
        返回当前最优的挂单(最高买单，最低卖单)
        :param symbol: 交易对
        :return: {}
        """
        params = {"symbol": symbol} if symbol else {}
        return self.client.get(url=self.rest_base_url + "/fapi/v1/ticker/bookTicker", params=params).json()

    async def get_quarterly_contract_settlement_price(self, pair):
        """
        返回季度合约历史结算价
        :param pair: 交易对
        :return: {}
        """
        return self.client.get(url=self.rest_base_url + "/futures/data/delivery-price",
                               params={"pair": pair}).json()

    async def get_open_interest(self, symbol):
        """
        获取未平仓合约数
        :param symbol: 交易对
        :return: {}
        """
        return self.client.get(url=self.rest_base_url + "/fapi/v1/openInterest",
                               params={"symbol": symbol}).json()

    async def get_open_interest_hist(self, symbol, period, limit=30, startTime=None, endTime=None):
        """
        查询合约持仓量历史
        :param symbol: 交易对
        :param period: 时间间隔 ("5m","15m","30m","1h","2h","4h","6h","12h","1d")
        :param limit: 返回数据的条数 (默认值: 30, 最大值: 500)
        :param startTime: 起始时间
        :param endTime: 结束时间
        :return: {}
        """
        params = {
            "symbol": symbol,
            "period": period,
            "limit": limit,
            # "startTime": startTime,
            # "endTime": endTime
        }
        return self.client.get(url=self.rest_base_url + "/futures/data/openInterestHist", params=params).json()

    async def get_top_long_short_position_ratio(self, symbol, period, limit=30, startTime=None, endTime=None):
        """
        获取大户持仓量多空比
        :param symbol: 交易对
        :param period: 时间间隔 ("5m","15m","30m","1h","2h","4h","6h","12h","1d")
        :param limit: 返回数据的条数 (默认值: 30, 最大值: 500)
        :param startTime: 起始时间
        :param endTime: 结束时间
        :return: {}
        """
        params = {
            "symbol": symbol,
            "period": period,
            "limit": limit,
            # "startTime": startTime,
            # "endTime": endTime
        }
        return self.client.get(url=self.rest_base_url + "/futures/data/topLongShortPositionRatio", params=params).json()

    async def get_top_long_short_account_ratio(self, symbol, period, limit=30, startTime=None, endTime=None):
        """
        获取大户账户数多空比
        :param symbol: 交易对
        :param period: 时间间隔 ("5m","15m","30m","1h","2h","4h","6h","12h","1d")
        :param limit: 返回数据的条数 (默认值: 30, 最大值: 500)
        :param startTime: 起始时间
        :param endTime: 结束时间
        :return: {}
        """
        params = {
            "symbol": symbol,
            "period": period,
            "limit": limit,
            # "startTime": startTime,
            # "endTime": endTime
        }
        return self.client.get(url=self.rest_base_url + "/futures/data/topLongShortAccountRatio", params=params).json()

    async def get_global_long_short_account_ratio(self, symbol, period, limit=30, startTime=None, endTime=None):
        """
        获取多空持仓人数比
        :param symbol: 交易对
        :param period: 时间间隔 ("5m","15m","30m","1h","2h","4h","6h","12h","1d")
        :param limit: 返回数据的条数 (默认值: 30, 最大值: 500)
        :param startTime: 起始时间
        :param endTime: 结束时间
        :return: {}
        """
        params = {
            "symbol": symbol,
            "period": period,
            "limit": limit,
            "startTime": startTime,
            "endTime": endTime
        }
        return self.client.get(url=self.rest_base_url + "/futures/data/globalLongShortAccountRatio",
                               params=params).json()

    async def get_taker_long_short_ratio(self, symbol, period, limit=30, startTime=None, endTime=None):
        """
        获取合约主动买卖量
        :param symbol: 交易对
        :param period: 时间间隔 ("5m","15m","30m","1h","2h","4h","6h","12h","1d")
        :param limit: 返回数据的条数 (默认值: 30, 最大值: 500)
        :param startTime: 起始时间
        :param endTime: 结束时间
        :return: {}
        """
        params = {
            "symbol": symbol,
            "period": period,
            "limit": limit,
            "startTime": startTime,
            "endTime": endTime
        }
        return self.client.get(url=self.rest_base_url + "/futures/data/takerlongshortRatio", params=params).json()

    async def get_lvt_klines(self, symbol, interval, startTime=None, endTime=None, limit=500):
        """
        获取杠杆代币历史净值K线
        :param symbol: token name, e.g. "BTCDOWN", "BTCUP"
        :param interval: 时间间隔
        :param startTime: 起始时间
        :param endTime: 结束时间
        :param limit: 默认 500, 最大 1000
        :return: {}
        """
        params = {
            "symbol": symbol,
            "interval": interval,
            "startTime": startTime,
            "endTime": endTime,
            "limit": limit
        }
        return self.client.get(url=self.rest_base_url + "/fapi/v1/lvtKlines", params=params).json()

    async def get_index_info(self, symbol=None):
        """
        获取交易对为综合指数的基础成分信息
        :param symbol: 交易对
        :return: {}
        """
        params = {"symbol": symbol} if symbol else {}
        return self.client.get(url=self.rest_base_url + "/fapi/v1/indexInfo", params=params).json()

    async def get_asset_index(self, symbol=None):
        """
        获取多资产模式资产汇率指数
        :param symbol: 资产对
        :return: {}
        """
        params = {"symbol": symbol}
        return self.client.get(url=self.rest_base_url + "/fapi/v1/assetIndex", params=params).json()


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
    # rest = MarketRestApi()
    # # 测试
    # print(asyncio.run(rest.test_ping()))
    # # # 获取服务器时间
    # print(asyncio.run(rest.get_server_time()))
    # # # 获取交易对信息
    # # print(asyncio.run(rest.get_exchange_info()))
    # # # 获取深度信息
    # print(asyncio.run(rest.get_order_book("BTCUSDT")))
    # # # 获取最新成交
    # # print(asyncio.run(rest.get_recent_trades("BTCUSDT")))
    # # 获取历史成交
    # # print(asyncio.run(rest.get_historical_trades("BTCUSDT")))
    # # 获取聚合成交
    # # print(asyncio.run(rest.get_aggregate_trades_list("BTCUSDT")))
    # # 获取K线数据
    # # print(asyncio.run(rest.get_candlestick_data("BTCUSDT", "1m")))
    # # # 获取合约K线数据
    # # print(asyncio.run(rest.get_continuous_Klines("BTCUSDT", "PERPETUAL", "1m")))
    # # 获取价格指数K线数据
    # # print(asyncio.run(rest.get_index_price_klines("BTCUSDT", "1m")))
    # # 获取标记价格K线数据
    # # print(asyncio.run(rest.get_mark_price_klines("BTCUSDT", "1m")))
    # # 获取溢价指数K线数据
    # # print(asyncio.run(rest.get_premium_index_klines("BTCUSDT", "1m")))
    # # 获取最新标记价格和资金费率
    # # print(asyncio.run(rest.get_premium_index("BTCUSDT")))
    # # 查询资金费率历史
    # # print(asyncio.run(rest.get_funding_rate_history("BTCUSDT")))
    # # 查询资金费率信息
    # # print(asyncio.run(rest.get_funding_info("BTCUSDT")))
    # # 获取24小时价格变动情况
    # # print(asyncio.run(rest.get_24hr_ticker("BTCUSDT")))
    # # 获取最新价格
    # # print(asyncio.run(rest.get_latest_price("BTCUSDT")))
    # # 获取最新价格V2
    # # print(asyncio.run(rest.get_latest_price_V2("BTCUSDT")))
    # # 返回当前最优的挂单(最高买单，最低卖单)
    # # print(asyncio.run(rest.get_best_order("BTCUSDT")))
    # # 返回季度合约历史结算价
    # # print(asyncio.run(rest.get_quarterly_contract_settlement_price("BTCUSD_240725")))
    # # 获取未平仓合约数
    # # print(asyncio.run(rest.get_open_interest("BTCUSDT")))
    # # # 查询合约持仓量历史
    # # print(asyncio.run(rest.get_open_interest_hist("BTCUSDT", "15m")))
    # # 获取大户持仓量多空比
    # # print(asyncio.run(rest.get_top_long_short_position_ratio("BTCUSDT", "1d")))
    # # 获取大户账户数多空比
    # # print(asyncio.run(rest.get_top_long_short_account_ratio("BTCUSDT", "1d")))
    # # # 获取多空持仓人数比
    # # print(asyncio.run(rest.get_global_long_short_account_ratio("BTCUSDT", "1d")))
    # # # 获取合约主动买卖量
    # # print(asyncio.run(rest.get_taker_long_short_ratio("BTCUSDT", "1d")))
    # # # 获取杠杆代币历史净值K线
    # # print(asyncio.run(rest.get_lvt_klines("BTCDOWN", "1m")))
    # # # 获取交易对为综合指数的基础成分信息
    # # print(asyncio.run(rest.get_index_info("BTCUSDT")))
    # # # 获取多资产模式资产汇率指数
    # # print(asyncio.run(rest.get_asset_index("BTCUSDT")))
    # #
    # #