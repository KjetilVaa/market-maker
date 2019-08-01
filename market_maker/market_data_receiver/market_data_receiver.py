from os import listdir
import logging
import time
import sys

# Each supported exchange needs a class for auth and orderbook

#### COINBASE PRO ####
# Websocket Orderbook
from market_maker.exchanges.coinbase_pro.coinbase_pro_orderbook import CoinbaseProOrderbook
# Auth class
from market_maker.exchanges.coinbase_pro.coinbase_pro_auth import CoinbaseProAuth
####################

class MarketDataReceiver():


    def __init__(self, exchange, mode):
        self.logger = logging.getLogger("root")
        #Mode is either sandbox or real trading
        self.mode = mode
        #Check if provided exchange is supported
        self.orderbook, self.auth = self._initialize_exchange(exchange)
        self.rate_limit = self.orderbook.rate_limit

    def authenticate(self):
        self.auth.authenticate(verbose=True)

    def start_orderbook(self):
        self.orderbook.start()

    def close_orderbook(self):
        self.orderbook.close()

    def _initialize_exchange(self, exchange):
        if exchange == "coinbase_pro":
            return CoinbaseProOrderbook(mode=self.mode), CoinbaseProAuth(mode=self.mode)
        raise Exception("Exchange not supported")
