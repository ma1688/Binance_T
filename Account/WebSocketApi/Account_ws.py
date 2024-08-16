# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :Account_ws.py
# @Time      :2024/8/16 11:15
# @Author    :MA-X-J
# @Software  :PyCharm


import asyncio
import hashlib
import hmac
import json
import time
import uuid

import websockets


class AccountWs:
    def __init__(self, api_key, secret_key, base_url):
        self.api_key = api_key
        self.secret_key = secret_key
        self.base_url = base_url
        self.ws_url = f"{self.base_url}"

    async def _generate_signature(self, params):
        query_string = '&'.join([f"{key}={params[key]}" for key in sorted(params)])
        return hmac.new(self.secret_key.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

    async def get_account(self, ws_method, recvWindow=None):
        params = {
            "apiKey": self.api_key,
            "timestamp": int(time.time() * 1000)
        }
        if recvWindow:
            params["recvWindow"] = recvWindow
        params["signature"] = await self._generate_signature(params)

        request = {
            "id": str(uuid.uuid4()),
            "method": ws_method,
            "params": params
        }

        async with websockets.connect(self.ws_url) as websocket:
            await websocket.send(json.dumps(request))
            response = await websocket.recv()
            return json.loads(response)


# Example usage
if __name__ == '__main__':
    api_keys = "ab7e987dff902922908f4521b5046a9018d46a993dbfce334e5dfa84a21e1c38"
    secret_keys = "a01c3e6c0d49afdd52f59a902e2739aa8f57e999802e36a59303619d7ed7d69e"
    base_url = "wss://testnet.binancefuture.com/ws-fapi/v1"

    "v2/account.balance" #账户余额V2 (USER_DATA)
    "account.balance"  # 账户余额 (USER_DATA)
    "v2/account.status"  # 账户状态V2 (USER_DATA)
    "account.status"  # 账户状态 (USER_DATA)

    account_ws = AccountWs(api_keys, secret_keys, base_url)
    response = asyncio.run(account_ws.get_account("v2/account.balance"))
    print(response)

