# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :Account_API.py
# @Time      :2024/8/12 下午3:04
# @Author    :MA-X-J
# @Software  :PyCharm
import asyncio
import hashlib
import hmac
import time
import urllib.parse

import httpx


class Account:
    """
    账户相关API
    """

    def __init__(self, api_key, secret_key):
        """
        初始化各参数
        """
        # self.base_url = "https://fapi.binance.com"
        self.base_url = "https://testnet.binancefuture.com"
        self.api_key = api_key
        self.secret_key = secret_key
        self.timestamp = int(time.time() * 1000)
        self.headers = {
            "Content-Type": "application/json;charset=utf-8",
            "User-Agent": "binance-api",
            'X-MBX-APIKEY': self.api_key
        }
        self.client = httpx.AsyncClient(headers=self.headers)

    async def get_signature(self, params):
        """
        获取签名
        """
        params['timestamp'] = self.timestamp
        query_string = urllib.parse.urlencode(params)
        signature = hmac.new(self.secret_key.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
        params['signature'] = signature
        return params

    async def get_account_information_v2(self):
        """
        获取账户信息 V2
        """
        params = {
            'timestamp': self.timestamp,
            'recvWindow': 5000
        }
        params = await self.get_signature(params)
        url = f"{self.base_url}/fapi/v2/account"
        response = await self.client.get(url, params=params)
        return response.json()

    async def get_account_information_v3(self):
        """
        获取账户信息 V3
        """
        params = {
            'timestamp': self.timestamp,
            'recvWindow': 5000
        }
        params = await self.get_signature(params)
        url = f"{self.base_url}/fapi/v3/account"
        response = await self.client.get(url, params=params)
        return response.json()

    async def get_account_balance_v2(self):
        """
        获取账户余额 V2
        """
        params = {
            'timestamp': self.timestamp,
            'recvWindow': 5000
        }
        params = await self.get_signature(params)
        url = f"{self.base_url}/fapi/v2/balance"
        response = await self.client.get(url, params=params)
        return response.json()

    async def get_account_balance_v3(self):
        """
        获取账户余额 V3
        """
        params = {
            'timestamp': self.timestamp,
            'recvWindow': 5000
        }
        params = await self.get_signature(params)
        url = f"{self.base_url}/fapi/v3/balance"
        response = await self.client.get(url, params=params)
        return response.json()

    async def get_commission_rate(self, symbol, recvWindow=None):
        """
        查询用户手续费率
        请求权重 20
        """
        params = {
            'symbol': symbol,
            'timestamp': self.timestamp
        }
        if recvWindow:
            params['recvWindow'] = recvWindow
        params = await self.get_signature(params)
        url = f"{self.base_url}/fapi/v1/commissionRate"
        response = await self.client.get(url, params=params)
        return response.json()

    async def get_account_config(self, recvWindow=None):
        """
        查询账户配置
        请求权重 5
        """
        params = {
            'timestamp': self.timestamp
        }
        if recvWindow:
            params['recvWindow'] = recvWindow
        params = await self.get_signature(params)
        url = f"{self.base_url}/fapi/v1/accountConfig"
        response = await self.client.get(url, params=params)
        return response.json()

    async def get_symbol_config(self, symbol=None, recvWindow=None):
        """
        查询交易对上的基础配置
        请求权重 5
        """
        params = {
            'timestamp': self.timestamp
        }
        if symbol:
            params['symbol'] = symbol
        if recvWindow:
            params['recvWindow'] = recvWindow
        params = await self.get_signature(params)
        url = f"{self.base_url}/fapi/v1/symbolConfig"
        response = await self.client.get(url, params=params)
        return response.json()

    async def get_order_rate_limit(self, recvWindow=None):
        """
        查询用户下单限频
        请求权重 1
        """
        params = {
            'timestamp': self.timestamp
        }
        if recvWindow:
            params['recvWindow'] = recvWindow
        params = await self.get_signature(params)
        url = f"{self.base_url}/fapi/v1/rateLimit/order"
        response = await self.client.get(url, params=params)
        return response.json()

    async def get_leverage_bracket(self, symbol=None, recvWindow=None):
        """
        查询账户特定交易对的杠杆分层标准
        请求权重 1
        """
        params = {
            'timestamp': self.timestamp
        }
        if symbol:
            params['symbol'] = symbol
        if recvWindow:
            params['recvWindow'] = recvWindow
        params = await self.get_signature(params)
        url = f"{self.base_url}/fapi/v1/leverageBracket"
        response = await self.client.get(url, params=params)
        return response.json()

    async def get_multi_assets_margin(self, recvWindow=None):
        """
        查询用户目前在所有symbol合约上的联合保证金模式
        请求权重 30
        """
        params = {
            'timestamp': self.timestamp
        }
        if recvWindow:
            params['recvWindow'] = recvWindow
        params = await self.get_signature(params)
        url = f"{self.base_url}/fapi/v1/multiAssetsMargin"
        response = await self.client.get(url, params=params)
        return response.json()

    async def get_position_side(self, recvWindow=None):
        """
        查询用户目前在所有symbol合约上的持仓模式
        请求权重 30
        """
        params = {
            'timestamp': self.timestamp
        }
        if recvWindow:
            params['recvWindow'] = recvWindow
        params = await self.get_signature(params)
        url = f"{self.base_url}/fapi/v1/positionSide/dual"
        response = await self.client.get(url, params=params)
        return response.json()

    async def get_income(self, symbol=None, incomeType=None, startTime=None, endTime=None, page=None, limit=None,
                         recvWindow=None):
        """
        获取账户损益资金流水
        请求权重 30
        """
        params = {
            'timestamp': self.timestamp
        }
        if symbol:
            params['symbol'] = symbol
        if incomeType:
            params['incomeType'] = incomeType
        if startTime:
            params['startTime'] = startTime
        if endTime:
            params['endTime'] = endTime
        if page:
            params['page'] = page
        if limit:
            params['limit'] = limit
        if recvWindow:
            params['recvWindow'] = recvWindow
        params = await self.get_signature(params)
        url = f"{self.base_url}/fapi/v1/income"
        response = await self.client.get(url, params=params)
        return response.json()

    async def get_api_trading_status(self, symbol=None, recvWindow=None):
        """
        合约交易量化规则指标
        请求权重 带 symbol 1, 不带 10
        """
        params = {
            'timestamp': self.timestamp
        }
        if symbol:
            params['symbol'] = symbol
        if recvWindow:
            params['recvWindow'] = recvWindow
        params = await self.get_signature(params)
        url = f"{self.base_url}/fapi/v1/apiTradingStatus"
        response = await self.client.get(url, params=params)
        return response.json()

    async def get_income_download_id(self, startTime, endTime, recvWindow=None):
        """
        获取合约资金流水下载Id
        请求权重 5
        """
        params = {
            'startTime': startTime,
            'endTime': endTime,
            'timestamp': self.timestamp
        }
        if recvWindow:
            params['recvWindow'] = recvWindow
        params = await self.get_signature(params)
        url = f"{self.base_url}/fapi/v1/income/asyn"
        response = await self.client.get(url, params=params)
        return response.json()

    async def get_income_download_link(self, downloadId, recvWindow=None):
        """
        通过下载Id获取合约资金流水下载链接
        请求权重 5
        """
        params = {
            'downloadId': downloadId,
            'timestamp': self.timestamp
        }
        if recvWindow:
            params['recvWindow'] = recvWindow
        params = await self.get_signature(params)
        url = f"{self.base_url}/fapi/v1/income/asyn/id"
        response = await self.client.get(url, params=params)
        return response.json()

    async def get_order_history_download_id(self, startTime, endTime, recvWindow=None):
        """
        获取合约订单历史下载Id
        请求权重 5
        """
        params = {
            'startTime': startTime,
            'endTime': endTime,
            'timestamp': self.timestamp
        }
        if recvWindow:
            params['recvWindow'] = recvWindow
        params = await self.get_signature(params)
        url = f"{self.base_url}/fapi/v1/order/asyn"
        response = await self.client.get(url, params=params)
        return response.json()

    async def get_order_download_link(self, downloadId, recvWindow=None):
        """
        通过下载Id获取合约订单下载链接
        请求权重 5
        """
        params = {
            'downloadId': downloadId,
            'timestamp': self.timestamp
        }
        if recvWindow:
            params['recvWindow'] = recvWindow
        params = await self.get_signature(params)
        url = f"{self.base_url}/fapi/v1/order/asyn/id"
        response = await self.client.get(url, params=params)
        return response.json()

    async def get_trade_history_download_id(self, startTime, endTime, recvWindow=None):
        """
        获取合约交易历史下载Id
        请求权重 5
        """
        params = {
            'startTime': startTime,
            'endTime': endTime,
            'timestamp': self.timestamp
        }
        if recvWindow:
            params['recvWindow'] = recvWindow
        params = await self.get_signature(params)
        url = f"{self.base_url}/fapi/v1/trade/asyn"
        response = await self.client.get(url, params=params)
        return response.json()

    async def get_trade_download_link(self, downloadId, recvWindow=None):
        """
        通过下载Id获取合约交易历史下载链接
        请求权重 5
        """
        params = {
            'downloadId': downloadId,
            'timestamp': self.timestamp
        }
        if recvWindow:
            params['recvWindow'] = recvWindow
        params = await self.get_signature(params)
        url = f"{self.base_url}/fapi/v1/trade/asyn/id"
        response = await self.client.get(url, params=params)
        return response.json()

    async def set_fee_burn(self, feeBurn, recvWindow=None):
        """
        改变用户所有symbol合约交易BNB抵扣开关
        请求权重 1
        """
        params = {
            'feeBurn': feeBurn,
            'timestamp': self.timestamp
        }
        if recvWindow:
            params['recvWindow'] = recvWindow
        params = await self.get_signature(params)
        url = f"{self.base_url}/fapi/v1/feeBurn"
        response = await self.client.post(url, params=params)
        return response.json()

    async def get_fee_burn_status(self, recvWindow=None):
        """
        查询用户所有symbol合约交易BNB抵扣开关状态
        请求权重 30
        """
        params = {
            'timestamp': self.timestamp
        }
        if recvWindow:
            params['recvWindow'] = recvWindow
        params = await self.get_signature(params)
        url = f"{self.base_url}/fapi/v1/feeBurn"
        response = await self.client.get(url, params=params)
        return response.json()


if __name__ == '__main__':
    # api_keys = "FXg92Z1e1IVC89WpVosBWT73RenGYaOsUR7PLuQ7YXv9cV6rpPbFWorT2WwaOk5H"
    # secret_keys = "vqrfNjxlKAcmdwpyo47qkUDkINpkL4AiyRQM9ytn9Plc8DgJWkiWg1IFX43fP6XX"
    api_keys = "ab7e987dff902922908f4521b5046a9018d46a993dbfce334e5dfa84a21e1c38"
    secret_keys = "a01c3e6c0d49afdd52f59a902e2739aa8f57e999802e36a59303619d7ed7d69e"
    account = Account(api_keys, secret_keys)

    print(asyncio.run(account.get_account_balance_v2()))


