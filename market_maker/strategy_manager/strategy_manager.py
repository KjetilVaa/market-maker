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

    def __init__(self, orderbook):
        self.logger = logging.getLogger("root")
        if len(orderbook["asks"]) <= 1 or len(orderbook["bids"]) <= 1:
            self.orderbook = None
            self.ready = False
        self.orderbook = orderbook
        self.ready = True

        # these will have an immediate effect on position size
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
        # beating the competition
        self.inside_spread = strategy_settings["STRATEGY"]["INSIDE_SPREAD"]
        # initialize strategy
        self.strategy = BasicStrategy(order_pairs=self.order_pairs, inside_spread = self.inside_spread, interval=self.interval, min_spread=self.min_spread)

    def run(self):
        # calculate strategy
        self.strategy.calculate(self.orderbook, self.ready)
