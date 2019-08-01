import time
import logging
import cbpro
import sys
import datetime as dt
import logging

from market_maker.utils.colors import Colors
from market_maker.strategy_settings import strategy_settings


"""
Postion manager's job is to constantly manage the portfolio
and assets on the exchange. Therefore, it needs the following:
1. Access to funds on the exchange
2. Determine the size of positions based on funds available on the exchange
   and feedback from the strategy manager
"""

class PositionManager():


    def __init__(self, mode):
        self.logger = logging.getLogger("root")
