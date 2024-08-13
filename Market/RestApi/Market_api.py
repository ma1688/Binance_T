# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :Market_api.py
# @Time      :2024/8/12 下午4:41
# @Author    :MA-X-J
# @Software  :PyCharm
import asyncio
import time

import httpx


# api_key = "FXg92Z1e1IVC89WpVosBWT73RenGYaOsUR7PLuQ7YXv9cV6rpPbFWorT2WwaOk5H"
# secret_key = "vqrfNjxlKAcmdwpyo47qkUDkINpkL4AiyRQM9ytn9Plc8DgJWkiWg1IFX43fP6XX"


class MarketRestApi:

    def __init__(self, api_keys, secret_keys):
        # self.rest_base_url = "https://fapi.binance.com"
        self.rest_base_url = "https://testnet.binancefuture.com"
        self.api_key = api_keys
        self.secret_key = secret_keys
        self.timestamp = int(time.time() * 1000)
        self.headers = {
            "Content-Type": "application/json;charset=utf-8",
            'X-MBX-APIKEY': self.api_key
        }
        self.client = httpx.AsyncClient(headers=self.headers)

    # 测试服务器是否正常ping
    async def test_ping(self):
        """
        测试服务器是否正常
        :return:  {}
        """
        test_ping = await self.client.get(url=self.rest_base_url + "/fapi/v1/ping")
        return test_ping.json()

    # 获取服务器时间
    async def get_server_time(self):
        """
        获取服务器时间
        :return:  {'serverTime': 1723285908488}
        """
        server_time = await self.client.get(url=self.rest_base_url + "/fapi/v1/time")
        return server_time.json()

    # 获取交易对信息
    async def get_exchange_info(self):
        """
        获取交易对信息
        :return:  {}
        """
        exchange_info = await self.client.get(url=self.rest_base_url + "/fapi/v1/exchangeInfo")
        return exchange_info.json()

    # 获取深度信息
    async def get_depth(self, symbol, limit=5):
        """
        获取深度信息
        :param symbol: 交易对
        :param limit: 档数  默认 500; 可选值:[5, 10, 20, 50, 100, 500, 1000]
        :return:
        """
        depth_data = await self.client.get(url=self.rest_base_url + "/fapi/v1/depth",
                                           params={"symbol": symbol, "limit": limit})
        return depth_data.json()

    # 获取近期订单簿成交
    async def get_recent_trades(self, symbol, limit=500):
        """
        获取近期订单簿成交
        :param symbol: 交易对
        :param limit: 档数 默认:500，最大1000
        :return:  {}
        """
        recent_trades = await self.client.get(url=self.rest_base_url + "/fapi/v1/trades",
                                              params={"symbol": symbol, "limit": limit})
        return recent_trades.json()

    # 查询订单簿历史成交
    async def get_historical_trades(self, symbol, limit=500, fromId=None):
        """
        查询订单簿历史成交
        :param symbol: 交易对
        :param limit: 档数 默认值:500 最大值:1000.
        :param fromId:  从哪一条成交id开始返回. 缺省返回最近的成交记录
        :return:  {}
        """
        get_historical_trades = await self.client.get(url=self.rest_base_url + "/fapi/v1/historicalTrades",
                                                      params={"symbol": symbol, "limit": limit, "fromId": fromId})
        return get_historical_trades.json()

    # 获取聚合成交
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
        aggregate_trades_list = await self.client.get(url=self.rest_base_url + "/fapi/v1/aggTrades",
                                                      params={"symbol": symbol, "fromId": fromId,
                                                              "startTime": startTime,
                                                              "endTime": endTime,
                                                              "limit": limit})
        return aggregate_trades_list

    # 获取K线数据
    async def get_candlestick_data(self, symbol, interval, startTime=None, endTime=None, limit=500):
        """
        获取K线数据
        :param symbol: 交易对
        :param interval: 时间间隔
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
        candlestick_data = await self.client.get(url=self.rest_base_url + "/fapi/v1/klines",
                                                 params={"symbol": symbol, "interval": interval, "startTime": startTime,
                                                         "endTime": endTime, "limit": limit})
        return candlestick_data.json()

    # 获取指数K线数据
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
        continuous_Klines = await self.client.get(url=self.rest_base_url + "/fapi/v1/continuousKlines",
                                                  params={"pair": pair, "contractType": contractType,
                                                          "interval": interval,
                                                          "startTime": startTime, "endTime": endTime, "limit": limit})
        return continuous_Klines.json()

    # 获取指数K线数据
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
        index_price_klines = await self.client.get(url=self.rest_base_url + "/fapi/v1/indexPriceKlines",
                                                   params={"pair": pair, "interval": interval, "startTime": startTime,
                                                           "endTime": endTime,
                                                           "limit": limit})
        return index_price_klines.json()

    # 获取标记价格K线数据
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
        mark_price_klines = await self.client.get(url=self.rest_base_url + "/fapi/v1/markPriceKlines",
                                                  params={"symbol": symbol, "interval": interval,
                                                          "startTime": startTime,
                                                          "endTime": endTime, "limit": limit})
        return mark_price_klines.json()

    # 获取溢价指数K线数据
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
        premium_index_klines = await self.client.get(url=self.rest_base_url + "/fapi/v1/premiumIndexKlines",
                                                     params={"symbol": symbol, "interval": interval,
                                                             "startTime": startTime,
                                                             "endTime": endTime, "limit": limit})
        return premium_index_klines.json()

    # 获取资金费率K线数据
    async def get_premium_index(self, symbol=None):
        """
        获取最新标记价格和资金费率
        :param symbol: 交易对
        :return:  {}
        """
        premium_index = await self.client.get(url=self.rest_base_url + "/fapi/v1/premiumIndex",
                                              params={"symbol": symbol})
        return premium_index.json()

    # 获取资金费率K线数据
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
        funding_rate_history = await self.client.get(url=self.rest_base_url + "/fapi/v1/fundingRate",
                                                     params=params)
        return funding_rate_history.json()

    # 获取资金费率信息
    async def get_funding_info(self, symbol=None):
        """

        查询资金费率信息
        :param symbol: 交易对
        :return: {}
        """
        funding_info = await self.client.get(url=self.rest_base_url + "/fapi/v1/fundingRate", params={"symbol": symbol})
        return funding_info.json()

    # 获取24小时价格变动情况
    async def get_24hr_ticker(self, symbol=None):
        """
        获取24小时价格变动情况
        :param symbol: 交易对
        :return: {}
        """
        params = {"symbol": symbol}
        day_ticker = await self.client.get(url=self.rest_base_url + "/fapi/v1/ticker/24hr", params=params)
        return day_ticker.json()

    # 获取最新价格
    async def get_latest_price(self, symbol=None):
        """
        获取最新价格
        :param symbol: 交易对
        :return: {}
        """
        params = {"symbol": symbol}
        latest_price = await self.client.get(url=self.rest_base_url + "/fapi/v1/ticker/price", params=params)
        return latest_price.json()

    # 获取最新价格V2
    async def get_latest_price_V2(self, symbol=None):
        """
        获取最新价格V2
        :param symbol: 交易对
        :return: {}
        """
        params = {"symbol": symbol}
        latest_price_V2 = await self.client.get(url=self.rest_base_url + "/fapi/v2/ticker/price", params=params)
        return latest_price_V2.json()

    # 获取最优挂单
    async def get_best_order(self, symbol=None):
        """
        返回当前最优的挂单(最高买单，最低卖单)
        :param symbol: 交易对
        :return: {}
        """
        params = {"symbol": symbol} if symbol else {}
        best_order = await self.client.get(url=self.rest_base_url + "/fapi/v1/ticker/bookTicker", params=params)
        return best_order.json()

    # 返回季度合约历史结算价
    async def get_quarterly_contract_settlement_price(self, pair):
        """
        返回季度合约历史结算价
        :param pair: 交易对
        :return: {}
        """
        quarterly_contract_settlement_price = await self.client.get(
            url=self.rest_base_url + "/futures/data/settle-price",
            params={"pair": pair})
        return quarterly_contract_settlement_price.json()

    # 获取未平仓合约数
    async def get_open_interest(self, symbol):
        """
        获取未平仓合约数
        :param symbol: 交易对
        :return: {}
        """
        open_interest = await self.client.get(url=self.rest_base_url + "/fapi/v1/openInterest",
                                              params={"symbol": symbol})
        return open_interest.json()

    # 查询合约持仓量历史
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
            "startTime": startTime,
            "endTime": endTime
        }
        open_interest_hist = await self.client.get(url=self.rest_base_url + "/futures/data/openInterestHist",
                                                   params=params)
        return open_interest_hist.json()

    # 获取大户持仓量多空比
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
            "startTime": startTime,
            "endTime": endTime
        }
        top_long_short_position_ratio = await self.client.get(
            url=self.rest_base_url + "/futures/data/topLongShortPositionRatio", params=params)
        return top_long_short_position_ratio.json()

    # 获取大户账户数多空比
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
            "startTime": startTime,
            "endTime": endTime
        }
        top_long_short_account_ratio = await self.client.get(
            url=self.rest_base_url + "/futures/data/topLongShortAccountRatio",
            params=params)
        return top_long_short_account_ratio.json()

    # 获取多空持仓人数比
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
        global_long_short_account_ratio = await self.client.get(
            url=self.rest_base_url + "/futures/data/globalLongShortAccountRatio",
            params=params)
        return global_long_short_account_ratio.json()

    # 获取合约主动买卖量
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
        taker_long_short_ratio = await self.client.get(url=self.rest_base_url + "/futures/data/takerlongshortRatio",
                                                       params=params)
        return taker_long_short_ratio.json()

    # 获取杠杆代币历史净值K线
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
        lvt_klines = await self.client.get(url=self.rest_base_url + "/fapi/v1/lvtKlines", params=params)
        return lvt_klines.json()

    # 获取交易对为综合指数的基础成分信息
    async def get_index_info(self, symbol=None):
        """
        获取交易对为综合指数的基础成分信息
        :param symbol: 交易对
        :return: {}
        """
        params = {"symbol": symbol} if symbol else {}
        index_info = await self.client.get(url=self.rest_base_url + "/fapi/v1/indexInfo", params=params)
        return index_info.json()

    # 获取多资产模式资产汇率指数
    async def get_asset_index(self, symbol=None):
        """
        获取多资产模式资产汇率指数
        :param symbol: 资产对
        :return: {}
        """
        params = {"symbol": symbol}
        asset_index = await self.client.get(url=self.rest_base_url + "/fapi/v1/assetIndex", params=params)
        return asset_index.json()


if __name__ == "__main__":
    api_key = "ab7e987dff902922908f4521b5046a9018d46a993dbfce334e5dfa84a21e1c38"
    secret_key = "a01c3e6c0d49afdd52f59a902e2739aa8f57e999802e36a59303619d7ed7d69e"

    market = MarketRestApi(api_key, secret_key)
    print(asyncio.run(market.get_aggregate_trades_list("BTCUSDT")))
