import time
import logging
import cbpro
import sys
import datetime as dt
import logging

from market_maker.utils.colors import Colors
from .coinbase_pro_settings import coinbase_pro_settings as settings
from market_maker.strategy_settings import strategy_settings

#This is the master class for all interactions with CoinbasePro
class CoinbaseProOrderbook(cbpro.WebsocketClient):

    # Don't grow a table larger than this amount. Helps cap memory usage.
    # Default = 200

    def __init__(self, mode, message_type="subscribe", mongo_collection=None, should_print=True, auth=False, channels=None):
        self.mode = mode
        self.logger = logging.getLogger("root")
        self.url = settings[mode]["WS_URL"]
        self.products = [settings["SYMBOL"]]
        self.channels = ["level2"]
        self.type = message_type
        self.ws = None
        self.thread = None
        self.auth = auth
        self.api_key = settings[mode]["API_KEY"]
        self.api_secret = settings[mode]["API_SECRET"]
        self.api_passphrase = settings[mode]["API_PASSPHRASE"]
        self.should_print = should_print
        self.mongo_collection = mongo_collection
        self.rate_limit = settings["RATE_LIMIT"]
        self.ready = False
        # orderbook length parameters
        self.max_orderbook_length = settings["MAX_TABLE_LENGTH"]
        self.min_orderbook_length = settings["MIN_TABLE_LENGTH"]
        # all bids and asks
        self.bids = {}
        self.asks = {}
        # number of bids and asks
        self.bids_length = 0
        self.asks_length = 0
        # best bid and ask
        self.best_bid = 0
        self.best_ask = 0
        # accumilated bids
        self.bids_depth = 0.0
        self.asks_depth = 0.0
        #spread
        self.spread = 0.0
        #spread precentage = best_ask/spread
        self.spread_precentage = 0.0


    def on_open(self):
        self.logger.info(f"Starting CoinbaseProOrderbook in {self.mode} mode for product {self.products[0]}")

    def on_message(self, msg):

        # If some type of API error, abort.
        if msg["type"] == "error":
            self.logger.error("Error: " + msg["message"] + " - Reason: " + msg["reason"])
            self.ready = False
            raise Exception("Exiting...")

        # First snapshot of orderbook
        if msg['type'] == 'snapshot':
            # key=price and value = quantity
            self.bids = {float(k): float(v) for (k, v) in msg['bids']}
            self.asks = {float(k): float(v) for (k, v) in msg['asks']}
            self._calculate_metrics()
            self.print_metrics(with_orderbook=False)
            self.ready = True

        # Every update of orderbook
        if msg['type'] == 'l2update':
            self.ready = True
            for change in msg['changes']:
                action = change[0]
                price = float(change[1])
                quantity = float(change[2])
                if action == 'buy':
                    # if the qty becomes 0, we need to get rid of this item in the order book
                    if quantity == '0':
                        self.bids.pop(price)
                    else:
                        self.bids[price] = quantity

                else:
                    # if the qty becomes 0, we need to get rid of this item in the order book
                    if quantity == '0':
                        self.asks.pop(price)
                    else:
                        self.asks[price] = quantity

            # Calculate new metrics based on the updates
            self._calculate_metrics()
            # Print new metrics
            # self.print_metrics(with_orderbook=False)

    def on_close(self):
        self.logger.info(f"Closing CoinbaseProOrderbook in {self.mode} mode for product {self.products[0]}")
        self.ready = False


    def _calculate_metrics(self):
        # sorted defaults to index 0 in dict element, aka the key which is the price
        self.bids = {float(k):float(v) for (k, v) in sorted(self.bids.items(), reverse=True)[:self.max_orderbook_length]}
        self.asks = {float(k):float(v) for (k, v) in sorted(self.asks.items())[:self.max_orderbook_length]}
        self.bids_length = len(self.bids)
        self.asks_length = len(self.asks)
        self.bids_depth = sum(self.bids.values())
        self.asks_depth = sum(self.asks.values())
        self.best_bid = next(iter(self.bids))
        self.best_ask = next(iter(self.asks))
        self.spread = self.best_ask - self.best_bid
        self.spread_precentage = self.spread/self.best_ask

    #Retrive metrics as a dict
    def get_metrics(self):
        res = {}
        res["bids"] = self.bids
        res["asks"] = self.asks
        res["best_bid"] = self.best_bid
        res["best_ask"] = self.best_ask
        res["bids_length"] = self.bids_length
        res["asks_length"] = self.asks_length
        res["bids_depth"] = self.bids_depth
        res["asks_depth"] = self.asks_depth
        res["spread"] = self.spread
        res["spread_precentage"] = self.spread_precentage
        return res

    def is_ready(self):
        return self.ready


    def print_metrics(self, with_orderbook):
        if with_orderbook:
            print(self.get_metrics())
        res = self.get_metrics()
        print("Best Ask: ", res["best_ask"])
        print("Best Bid: ", res["best_bid"])
        print("Bids length: ", res["bids_length"])
        print("Asks length: ", res["asks_length"])
        print("Bids depth: ",res["bids_depth"])
        print("Asks depth: ", res["asks_depth"])
        print("Spread: ", res["spread"])
        print("Spread precentage: ", res["spread_precentage"])
