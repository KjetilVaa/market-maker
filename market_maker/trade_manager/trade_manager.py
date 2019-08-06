import time
import logging
import cbpro
import sys
import datetime as dt
import logging
import numpy as np

from market_maker.utils.colors import Colors
from market_maker.strategy_settings import strategy_settings


"""
The trade executor will handle all trade-related tasks with the exchange. This includes:
1. Keeping track our position
2. handle all API buy/sell limit orders
"""


class TradeManager():

    def __init__(self, position_manager, strategy_manager):
        self.logger = logging.getLogger("root")
        self.amount_sold = 0.0
        self.amount_bought = 0.0
        self.position = 0.0
        self.ready = False
        # Managers
        self.position_manager = position_manager
        self.strategy_manager = strategy_manager

    def run(self):
        if not (self.position_manager.ready and self.strategy_manager.ready):
            self.logger.error("Position manager status: {self.position_manager.ready} - Strategy manager status: {self.strategy_manager.ready}")
            raise Exception("Managers not ready to execute trades")
        #continue
        """
        Here wee need

        """
