import time
import logging
import cbpro
import sys
import datetime as dt
import logging

import ccxt
from .coinbasepro_settings import coinbasepro_settings as settings


"""
This is the class for the coinbasepro exchange. It should:
- Be able to fetch the orderbook
- Calculate different metrics based on the orderbook
- Be able to authenticate with the exchange
- Perform authenticated actions with the exchange (create limit orders etc..)
"""

class CoinbasePro():


    def __init__(self, mode):
        self.logger = logging.getLogger("root")
        self.ready = True
        # settings stuff
        self.url = settings[mode]["API_URL"]
        self.symbol = settings["SYMBOL"]
        self.api_key = settings[mode]["API_KEY"]
        self.api_secret = settings[mode]["API_SECRET"]
        self.api_passphrase = settings[mode]["API_PASSPHRASE"]
        self.rate_limit = int(settings["RATE_LIMIT"])
        self.orderbook_limit = int(settings["ORDERBOOK_LIMIT"])
        # market data
        self.orderbook = {
            "asks": [],
            "bids": [],
            "bids_length": 0,
            "asks_length": 0,
            # best bid and ask
            "best_bid": 0,
            "best_ask": 0,
            # accumilated bids
            "bids_depth": 0.0,
            "asks_depth": 0.0,
            #spread
            "spread": 0.0,
            #spread precentage = best_ask/spread
            "spread_precentage": 0.0
        }

        self.auth = {
            # {free, on_hold, total=free+on_hold}
            "base_balance": {},
            "quote_balance": {}
        }

        # Initialize exchange
        self.exchange = self.initialize_exchange()


    def initialize_exchange(self):
        exchange = ccxt.coinbasepro({
        "rateLimit": self.rate_limit,
        "apiKey": self.api_key,
        "secret": self.api_secret,
        "password": self.api_passphrase
        })
        return exchange

    def get_balance(self):
        if not self.ready:
            raise Exception("Exchange is not ready.")
        self.logger.info("Fetching balances for coinbasepro")
        res = self.exchange.fetch_balance()
        if len(res["info"]) <= 1:
            raise Exception("Could not get balances for current exchange")
        base_symbol = self.symbol.split("/")[0]
        quote_symbol = self.symbol.split("/")[1]
        # parse result to our base and quote balances
        self.auth["base_balance"] = res[base_symbol]
        self.auth["quote_balance"] = res[quote_symbol]

    def get_orderbook(self):
        if not self.ready:
            raise Exception("Exchange is not ready.")
        self.logger.info(f"Fetching {self.symbol} orderbook")
        res = self.exchange.fetch_l2_order_book(self.symbol, self.orderbook_limit)
        if len(res["asks"]) <= 0 or len(res["bids"]) <= 0:
            self.ready = False
            raise Exception("Exchange is not ready")
        self.ready = True
        self.orderbook["asks"] = res["asks"]
        self.orderbook["bids"] = res["bids"]
        #calculate metrics --> res['bids'] = [[price, amount]...]
        self.orderbook["best_ask"] = res["asks"][0][0]
        self.orderbook["best_bid"] = res["bids"][0][0]
        self.orderbook["asks_length"] = len(res["asks"])
        self.orderbook["bids_length"] = len(res["bids"])
        self.orderbook["spread"] = res["asks"][0][0] - res["bids"][0][0]
        self.orderbook["spread_precentage"] = res["asks"][0][0]/res["bids"][0][0]
        self.orderbook["ask_depth"] = sum(item[1] for item in res["asks"])
        self.orderbook["bid_depth"] = sum(item[1] for item in res["bids"])

    def print_orderbook_metrics(self):
        print("Best Ask: ", self.orderbook["best_ask"])
        print("Best Bid: ", self.orderbook["best_bid"])
        print("Asks length: ", self.orderbook["asks_length"])
        print("Bids length: ", self.orderbook["bids_length"])
        print("Asks depth: ", self.orderbook["ask_depth"])
        print("Bids depth: ", self.orderbook["bid_depth"])
        print("Spread: ", self.orderbook["spread"])
        print("Spread precentage: ", self.orderbook["spread_precentage"])

    def print_auth_metrics(self):
        print("Base balance ", self.auth["base_balance"])
        print("Quote balance ", self.auth["quote_balance"])
