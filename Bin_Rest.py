# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :Bin_Rest.py
# @Time      :2024/8/10 下午5:44
# @Author    :MA-X-J
# @Software  :PyCharm

import httpx


class BinRest:

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
        :param limit: 档数
        :return:  {}
        """
        return self.client.get(url=self.rest_base_url + "/fapi/v1/depth",
                               params={"symbol": symbol, "limit": limit}).json()

    async def get_recent_trades(self, symbol, limit=5):
        """
        获取最新成交
        :param symbol: 交易对
        :param limit: 档数
        :return:  {}
        """
        return self.client.get(url=self.rest_base_url + "/fapi/v1/trades",
                               params={"symbol": symbol, "limit": limit}).json()

    async def get_historical_trades(self, symbol, limit=5):
        """
        获取历史成交
        :param symbol: 交易对
        :param limit: 档数
        :return:  {}
        """
        return self.client.get(url=self.rest_base_url + "/fapi/v1/historicalTrades",
                               params={"symbol": symbol, "limit": limit}).json()

    async def get_aggregate_trades_list(self, symbol, limit=5):
        """
        获取聚合成交
        :param symbol: 交易对
        :param limit: 档数
        :return:  {}
        """
        return self.client.get(url=self.rest_base_url + "/fapi/v1/aggTrades",
                               params={"symbol": symbol, "limit": limit}).json()

    async def get_candlestick_data(self, symbol, interval, limit=5):
        """
        获取K线数据
        :param symbol: 交易对
        :param interval: 时间间隔
        :param limit: 档数
        :return:  {}
        """
        return self.client.get(url=self.rest_base_url + "/fapi/v1/klines",
                               params={"symbol": symbol, "interval": interval, "limit": limit}).json()

    async def get_continuous_Klines(self, pair, contractType, interval, startTime=None, endTime=None, limit=500):
        """
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
            "startTime": startTime,
            "endTime": endTime
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
            "startTime": startTime,
            "endTime": endTime
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
            "startTime": startTime,
            "endTime": endTime
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
        params = {"symbol": symbol} if symbol else {}
        return self.client.get(url=self.rest_base_url + "/fapi/v1/assetIndex", params=params).json()
