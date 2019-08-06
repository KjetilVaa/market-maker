import time
import logging
import cbpro
import sys
import datetime as dt
import logging

from market_maker.strategy_settings import strategy_settings
from .basic_strategy import BasicStrategy
"""
For every iteration:
- Store limit ask and limit bid price based on data from the orderbook
TODO:
- Determine multiple limit ask and bid prices
- Determine asymmetric limit orders
- Use orderbook flow to mitiage risk and increase spread
"""


class StrategyManager():

    def __init__(self, orderbook, orderbook_freq=5):
        self.logger = logging.getLogger("root")
        self.orderbook = orderbook
        self.orderbook_freq = orderbook_freq
        self.metrics = None
        self.ready = False
        # these will have an immediate effect on position size
        self.i = 0
        """
        below are some important strategy parameters from the settings file
        """
        # number of buy/sell order pairs to keep up
        self.order_pairs = strategy_settings["STRATEGY"]["ORDER_PAIRS"]
        # distance in precentage between successive order pairs.
        # each order is designed to be (INTERVAL*n)% away from the spread.
        self.interval = strategy_settings["STRATEGY"]["INTERVAL"]
        # minimum spread to begin trading
        self.min_spread = strategy_settings["STRATEGY"]["MIN_SPREAD"]
        # initialize strategy
        self.strategy = BasicStrategy(order_pairs=self.order_pairs, interval=self.interval, min_spread=self.min_spread)

    def run(self):
        # fetch orderbook metrics
        self.metrics = self._get_orderbook()
        # calculate strategy
        self.strategy.calculate(self.metrics, self.ready)




    def _get_orderbook(self):
        if self.orderbook.is_ready():
            self.logger.info("Fetching orderbook data and determining strategy")
            res = self.orderbook.get_metrics()
            self.ready = True
            return res
        else:
            self.logger.info("Orderbook not ready. Trying again...")
            self.ready = False
            return None
