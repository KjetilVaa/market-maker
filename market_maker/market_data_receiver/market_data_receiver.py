from os import listdir
import logging
import time
import sys

from market_maker.exchanges.coinbasepro.coinbasepro import CoinbasePro

"""
This is the master class for each exchange. It should do the following:
- Be able to start the orderbook receiver
- Be able to authenticate with the exchange
- Be able to stop the orderbook
- Be able to unauthenticate from the exchange

In addition, each supported exchange should be implemented under "exchanges" with:
- An auth class
- An orderbook class
- An settings class (request rate etc. for spesific exchange)
"""

class MarketDataReceiver():


    def __init__(self, exchange, mode):
        self.logger = logging.getLogger("root")
        #Mode is either sandbox or real trading
        self.mode = mode
        #Check if provided exchange is supported
        self.exchange = self._initialize_exchange(exchange)

    def get_balance(self):
        self.exchange.get_balance()

    def get_orderbook(self):
        self.exchange.get_orderbook()

    def close_orderbook(self):
        self.orderbook.close_orderbook()

    def _initialize_exchange(self, exchange):
        if exchange == "coinbasepro":
            return CoinbasePro(mode=self.mode)
        raise Exception("Exchange not supported")
