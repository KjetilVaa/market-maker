import time
import logging
import cbpro
import sys
import datetime as dt
import logging

from market_maker.strategy_settings import strategy_settings
"""
The strategy manager should, based on data the orderbook data, determine
the following:
1. At what price to place limit orders on both sides (this can be asymmetric)
2. How many orders to place on each side and the interval between each
3. When to remove limit orders on one side but not the other
4. Determine the frequence of checking the orderbook. Default every 2 seconds
"""


class StrategyManager():

    def __init__(self, orderbook, orderbook_freq=5):
        self.logger = logging.getLogger("root")
        self.orderbook = orderbook
        self.orderbook_freq = orderbook_freq
        self.metrics = None
        self.ready = False
        self.strategy = None

    def start(self):
        self.metrics = self.get_orderbook()

    def get_orderbook(self):
        if self.orderbook.is_ready():
            self.logger.info("Fetching orderbook data and determining strategy")
            res = self.orderbook.get_metrics()
            self.ready = True
            return res
        else:
            self.logger.info("Orderbook not ready. Trying again...")
            self.ready = False
            return None

    
