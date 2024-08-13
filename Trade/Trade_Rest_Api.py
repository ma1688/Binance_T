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
import asyncio
import hashlib
import hmac
import time
import urllib.parse

import httpx


class TradeRestApi:
    def __init__(self, api_key, secret_key):
        # self.url = "https://fapi.binance.com"
        self.url = "https://testnet.binancefuture.com"
        self.api_key = api_key
        self.secret_key = secret_key
        self.timestamp = int(time.time() * 1000)
        self.headers = {
            "Content-Type": "application/json;charset=utf-8",
            'X-MBX-APIKEY': self.api_key
        }
        self.client = httpx.AsyncClient(headers=self.headers)

    async def get_signature(self, params):
        """
        :param params:
        :return:
        """
        params['timestamp'] = self.timestamp
        query_string = urllib.parse.urlencode(params)
        signature = hmac.new(self.secret_key.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
        params['signature'] = signature
        return params

    async def place_order(self, symbol, side, types, positionSide="BOTH", reduceOnly=False, quantity=None, price=None,
                          newClientOrderId=None, stopPrice=None, closePosition=None, activationPrice=None,
                          callbackRate=None, timeInForce=None, workingType=None, priceProtect=None,
                          newOrderRespType=None, priceMatch=None, selfTradePreventionMode=None, goodTillDate=None,
                          recvWindow=None):
        """
        下单
        """
        params = {
            'symbol': symbol,
            'side': side,
            'type': types,
            'timestamp': self.timestamp
        }
        if positionSide:
            params['positionSide'] = positionSide
        if reduceOnly:
            params['reduceOnly'] = reduceOnly
        if quantity:
            params['quantity'] = quantity
        if price:
            params['price'] = price
        if newClientOrderId:
            params['newClientOrderId'] = newClientOrderId
        if stopPrice:
            params['stopPrice'] = stopPrice
        if closePosition:
            params['closePosition'] = closePosition
        if activationPrice:
            params['activationPrice'] = activationPrice
        if callbackRate:
            params['callbackRate'] = callbackRate
        if timeInForce:
            params['timeInForce'] = timeInForce
        if workingType:
            params['workingType'] = workingType
        if priceProtect:
            params['priceProtect'] = priceProtect
        if newOrderRespType:
            params['newOrderRespType'] = newOrderRespType
        if priceMatch:
            params['priceMatch'] = priceMatch
        if selfTradePreventionMode:
            params['selfTradePreventionMode'] = selfTradePreventionMode
        if goodTillDate:
            params['goodTillDate'] = goodTillDate
        if recvWindow:
            params['recvWindow'] = recvWindow

        params = await self.get_signature(params)
        print(f"params: {params}")
        url = f"{self.url}/fapi/v1/order"
        response = await self.client.post(url, params=params)
        print(f"{response.url}")
        return response.json()

    async def place_batch_order(self, batchOrders, recvWindow=1688):
        """
        批量下单
        """
        params = {
            'batchOrders': batchOrders,
            'timestamp': self.timestamp
        }
        if recvWindow:
            params['recvWindow'] = recvWindow

        params = await self.get_signature(params)
        url = f"{self.url}/fapi/v1/batchOrders"
        response = await self.client.post(url, params=params)
        return response.json()

    async def modify_order(self, symbol, side, quantity, price, orderId=None, origClientOrderId=None, priceMatch=None,
                           recvWindow=None):
        """
        修改订单
        修改订单功能，当前只支持限价（LIMIT）订单修改，修改后会在撮合队列里重新排序

        请求权重   10s order rate limit(X-MBX-ORDER-COUNT-10S)为1;
                 1min order rate limit(X-MBX-ORDER-COUNT-1M)为1;
                 IP rate limit(x-mbx-used-weight-1m)为1
        """
        params = {
            'symbol': symbol,
            'side': side,
            'quantity': quantity,
            'price': price,
            'timestamp': self.timestamp
        }
        if orderId:
            params['orderId'] = orderId
        if origClientOrderId:
            params['origClientOrderId'] = origClientOrderId
        if priceMatch:
            params['priceMatch'] = priceMatch
        if recvWindow:
            params['recvWindow'] = recvWindow

        params = await self.get_signature(params)
        url = f"{self.url}/fapi/v1/order"
        response = await self.client.put(url, params=params)
        return response.json()

    async def modify_batch_order(self, batchOrders, recvWindow=None):
        """
        批量修改订单
        """
        params = {
            'batchOrders': batchOrders,
            'timestamp': self.timestamp
        }
        if recvWindow:
            params['recvWindow'] = recvWindow

        params = await self.get_signature(params)
        url = f"{self.url}/fapi/v1/batchOrders"
        response = await self.client.put(url, params=params)
        return response.json()

    async def get_order_amendment_history(self, symbol, orderId=None, origClientOrderId=None, startTime=None,
                                          endTime=None, limit=50, recvWindow=None):
        """
        查询订单修改历史
        """
        params = {
            'symbol': symbol,
            'timestamp': self.timestamp
        }
        if orderId:
            params['orderId'] = orderId
        if origClientOrderId:
            params['origClientOrderId'] = origClientOrderId
        if startTime:
            params['startTime'] = startTime
        if endTime:
            params['endTime'] = endTime
        if limit:
            params['limit'] = limit
        if recvWindow:
            params['recvWindow'] = recvWindow

        params = await self.get_signature(params)
        url = f"{self.url}/fapi/v1/orderAmendment"
        response = await self.client.get(url, params=params)
        return response.json()

    async def cancel_order(self, symbol, orderId=None, origClientOrderId=None, recvWindow=None):
        """
        撤销订单
        """
        params = {
            'symbol': symbol,
            'timestamp': self.timestamp
        }
        if orderId:
            params['orderId'] = orderId
        if origClientOrderId:
            params['origClientOrderId'] = origClientOrderId
        if recvWindow:
            params['recvWindow'] = recvWindow

        params = await self.get_signature(params)
        url = f"{self.url}/fapi/v1/order"
        response = await self.client.delete(url, params=params)
        return response.json()

    async def cancel_batch_order(self, symbol, orderIdList=None, origClientOrderIdList=None, recvWindow=None):
        """
        批量撤销订单
        """
        params = {
            'symbol': symbol,
            'timestamp': self.timestamp
        }
        if orderIdList:
            params['orderIdList'] = orderIdList
        if origClientOrderIdList:
            params['origClientOrderIdList'] = origClientOrderIdList
        if recvWindow:
            params['recvWindow'] = recvWindow

        params = await self.get_signature(params)
        url = f"{self.url}/fapi/v1/batchOrders"
        response = await self.client.delete(url, params=params)
        return response.json()

    async def cancel_all_orders(self, symbol, recvWindow=None):
        """
        撤销全部订单
        """
        params = {
            'symbol': symbol,
            'timestamp': self.timestamp
        }
        if recvWindow:
            params['recvWindow'] = recvWindow

        params = await self.get_signature(params)
        url = f"{self.url}/fapi/v1/allOpenOrders"
        response = await self.client.delete(url, params=params)
        return response.json()

    async def countdown_cancel_all_orders(self, symbol, countdownTime, recvWindow=None):
        """
        倒计时撤销所有订单
        """
        params = {
            'symbol': symbol,
            'countdownTime': countdownTime,
            'timestamp': self.timestamp
        }
        if recvWindow:
            params['recvWindow'] = recvWindow

        params = await self.get_signature(params)
        url = f"{self.url}/fapi/v1/countdownCancelAll"
        response = await self.client.post(url, params=params)
        return response.json()

    async def get_order_status(self, symbol, orderId=None, origClientOrderId=None, recvWindow=None):
        """
        查询订单状态
        """
        params = {
            'symbol': symbol,
            'timestamp': self.timestamp
        }
        if orderId:
            params['orderId'] = orderId
        if origClientOrderId:
            params['origClientOrderId'] = origClientOrderId
        if recvWindow:
            params['recvWindow'] = recvWindow

        params = await self.get_signature(params)
        url = f"{self.url}/fapi/v1/order"
        response = await self.client.get(url, params=params)
        return response.json()

    async def get_all_orders(self, symbol, orderId=None, startTime=None, endTime=None, limit=500, recvWindow=None):
        """
        查询所有订单(包括历史订单)
        """
        params = {
            'symbol': symbol,
            'timestamp': self.timestamp
        }
        if orderId:
            params['orderId'] = orderId
        if startTime:
            params['startTime'] = startTime
        if endTime:
            params['endTime'] = endTime
        if limit:
            params['limit'] = limit
        if recvWindow:
            params['recvWindow'] = recvWindow

        params = await self.get_signature(params)
        url = f"{self.url}/fapi/v1/allOrders"
        response = await self.client.get(url, params=params)
        return response.json()

    async def get_open_orders(self, symbol=None, recvWindow=None):
        """
        查看当前全部挂单
        """
        params = {
            'timestamp': self.timestamp
        }
        if symbol:
            params['symbol'] = symbol
        if recvWindow:
            params['recvWindow'] = recvWindow

        params = await self.get_signature(params)
        url = f"{self.url}/fapi/v1/openOrders"
        response = await self.client.get(url, params=params)
        return response.json()

    async def get_open_order(self, symbol, orderId=None, origClientOrderId=None, recvWindow=None):
        """
        查询当前挂单
        """
        params = {
            'symbol': symbol,
            'timestamp': self.timestamp
        }
        if orderId:
            params['orderId'] = orderId
        if origClientOrderId:
            params['origClientOrderId'] = origClientOrderId
        if recvWindow:
            params['recvWindow'] = recvWindow

        params = await self.get_signature(params)
        url = f"{self.url}/fapi/v1/openOrder"
        response = await self.client.get(url, params=params)
        return response.json()

    async def get_force_orders(self, symbol=None, autoCloseType=None, startTime=None, endTime=None, limit=50,
                               recvWindow=None):
        """
        查询用户强平单历史
        """
        params = {
            'timestamp': self.timestamp
        }
        if symbol:
            params['symbol'] = symbol
        if autoCloseType:
            params['autoCloseType'] = autoCloseType
        if startTime:
            params['startTime'] = startTime
        if endTime:
            params['endTime'] = endTime
        if limit:
            params['limit'] = limit
        if recvWindow:
            params['recvWindow'] = recvWindow

        params = await self.get_signature(params)
        url = f"{self.url}/fapi/v1/forceOrders"
        response = await self.client.get(url, params=params)
        return response.json()

    async def get_user_trades(self, symbol, orderId=None, startTime=None, endTime=None, fromId=None, limit=500,
                              recvWindow=None):
        """
        获取某交易对的成交历史
        """
        params = {
            'symbol': symbol,
            'timestamp': self.timestamp
        }
        if orderId:
            params['orderId'] = orderId
        if startTime:
            params['startTime'] = startTime
        if endTime:
            params['endTime'] = endTime
        if fromId:
            params['fromId'] = fromId
        if limit:
            params['limit'] = limit
        if recvWindow:
            params['recvWindow'] = recvWindow

        print(f"params: {params}")
        params = await self.get_signature(params)
        url = f"{self.url}/fapi/v1/userTrades"
        response = await self.client.get(url, params=params)
        return response.json()

    async def change_margin_type(self, symbol, marginType, recvWindow=None):
        """
        变换用户在指定symbol合约上的保证金模式：逐仓或全仓
        """
        params = {
            'symbol': symbol,
            'marginType': marginType,
            'timestamp': self.timestamp
        }
        if recvWindow:
            params['recvWindow'] = recvWindow

        params = await self.get_signature(params)
        url = f"{self.url}/fapi/v1/marginType"
        response = await self.client.post(url, params=params)
        return response.json()

    async def change_position_mode(self, dualSidePosition, recvWindow=None):
        """
        变换用户在所有symbol合约上的持仓模式：双向持仓或单向持仓
        """
        params = {
            'dualSidePosition': dualSidePosition,
            'timestamp': self.timestamp
        }
        if recvWindow:
            params['recvWindow'] = recvWindow

        params = await self.get_signature(params)
        url = f"{self.url}/fapi/v1/positionSide/dual"
        response = await self.client.post(url, params=params)
        return response.json()

    async def change_leverage(self, symbol, leverage, recvWindow=None):
        """
        调整用户在指定symbol合约的开仓杠杆
        """
        params = {
            'symbol': symbol,
            'leverage': leverage,
            'timestamp': self.timestamp
        }
        if recvWindow:
            params['recvWindow'] = recvWindow

        params = await self.get_signature(params)
        url = f"{self.url}/fapi/v1/leverage"
        response = await self.client.post(url, params=params)
        return response.json()

    async def change_multi_assets_margin(self, multiAssetsMargin, recvWindow=None):
        """
        变换用户在所有symbol合约上的联合保证金模式：开启或关闭联合保证金模式
        """
        params = {
            'multiAssetsMargin': multiAssetsMargin,
            'timestamp': self.timestamp
        }
        if recvWindow:
            params['recvWindow'] = recvWindow

        params = await self.get_signature(params)
        url = f"{self.url}/fapi/v1/multiAssetsMargin"
        response = await self.client.post(url, params=params)
        return response.json()

    async def adjust_isolated_margin(self, symbol, amount, type, positionSide=None, recvWindow=None):
        """
        针对逐仓模式下的仓位，调整其逐仓保证金资金
        """
        params = {
            'symbol': symbol,
            'amount': amount,
            'type': type,
            'timestamp': self.timestamp
        }
        if positionSide:
            params['positionSide'] = positionSide
        if recvWindow:
            params['recvWindow'] = recvWindow

        params = await self.get_signature(params)
        url = f"{self.url}/fapi/v1/positionMargin"
        response = await self.client.post(url, params=params)
        return response.json()

    async def get_position_risk_v2(self, symbol=None, recvWindow=None):
        """
        查询持仓风险
        """
        params = {
            'timestamp': self.timestamp
        }
        if symbol:
            params['symbol'] = symbol
        if recvWindow:
            params['recvWindow'] = recvWindow

        params = await self.get_signature(params)
        url = f"{self.url}/fapi/v2/positionRisk"
        response = await self.client.get(url, params=params)
        return response.json()

    async def get_position_risk_v3(self, symbol=None, recvWindow=None):
        """
        查询持仓风险，仅返回有持仓或挂单的交易对
        """
        params = {
            'timestamp': self.timestamp
        }
        if symbol:
            params['symbol'] = symbol
        if recvWindow:
            params['recvWindow'] = recvWindow

        params = await self.get_signature(params)
        url = f"{self.url}/fapi/v3/positionRisk"
        response = await self.client.get(url, params=params)
        return response.json()

    async def get_adl_quantile(self, symbol=None, recvWindow=None):
        """
        持仓ADL队列估算
        """
        params = {
            'timestamp': self.timestamp
        }
        if symbol:
            params['symbol'] = symbol
        if recvWindow:
            params['recvWindow'] = recvWindow

        params = await self.get_signature(params)
        url = f"{self.url}/fapi/v1/adlQuantile"
        response = await self.client.get(url, params=params)
        return response.json()

    async def get_isolated_margin_history(self, symbol, types=None, startTime=None, endTime=None, limit=500,
                                          recvWindow=None):
        """
        查询逐仓保证金变动历史
        """
        params = {
            'symbol': symbol,
            'timestamp': self.timestamp
        }
        if types:
            params['type'] = types
        if startTime:
            params['startTime'] = startTime
        if endTime:
            params['endTime'] = endTime
        if limit:
            params['limit'] = limit
        if recvWindow:
            params['recvWindow'] = recvWindow

        params = await self.get_signature(params)
        url = f"{self.url}/fapi/v1/positionMargin/history"
        response = await self.client.get(url, params=params)
        return response.json()


if __name__ == "__main__":
    api_key = "ab7e987dff902922908f4521b5046a9018d46a993dbfce334e5dfa84a21e1c38"
    secret_key = "a01c3e6c0d49afdd52f59a902e2739aa8f57e999802e36a59303619d7ed7d69e"
    # api_key = "4UITYCS7rLuEuyKnST3IRwz8FPNKfxuCkjnCcT0UylKmo40s2pVM0r8cQnKb8fXy"
    # secret_key = "slQxspM6XYEAnGnhApekv2snw61XAMeXnmL9QQdQiGTVcjMoeOzyaazqCDdaMQNa"

    # 测试网下单
    trade = TradeRestApi(api_key, secret_key)
    # 下单
    print(asyncio.run(trade.place_order("ethusdt", "SELL", "LIMIT",
                                        "BOTH", True, 0.01, 2600)))
