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
"""


class StrategyManager():

    def __init__(self, auth, orderbook):
        self.logger = logging.getLogger("root")
        
