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
Position Manager's job is to constantly determine the size of each limit trade,
and to dynamically adjust risk based on total funds on the account.
For each iteration it will:
1. Fetch total funds for relevant account
2. Calculate a preferred buy/sell size

"""

class PositionManager():


    def __init__(self, auth):
        self.logger = logging.getLogger("root")
        self.auth = auth
        self.symbol = strategy_settings["STRATEGY"]["SYMBOL"]
        self.ready = False
        self.base_currency = None
        self.quote_currency = None
        self.pair_currency_ratio = None
        self.active_asks = [0.0]
        self.active_bids = [0.0]
        """
        below are some important strategy parameters from the settings file
        """
        self.order_start_size = strategy_settings["STRATEGY"]["ORDER_START_SIZE"]
        self.order_step_size = strategy_settings["STRATEGY"]["ORDER_STEP_SIZE"]


    def run(self):
        self.logger.info("Updating account details - Calculating trade posistions")
        self.update_accounts()
        if self.ready:
            self._calculate_positions()
            self._print_accounts()
        else:
            self.logger.error("Is not ready. Exiting")
            raise Exception("Failed to update base and quote accounts.")


    def _calculate_positions(self):
        # Dynamic order size calculation
        if self.pair_currency_ratio >= 3.00 or self.pair_currency_ratio <= 0.75:
            self.logger.info(f"A pair_currency_ratio of {self.pair_currency_ratio} is not within the threshold. Exiting...")
            raise Exception("Balance ratio supassed threshold")
        elif self.position > 0:
            #do something
        elif self.position < 0:
            #do somethign
        else:
            #do the same as launch
        active_ask = self.order_start_size * float(self.base_currency["available"])
        active_bid = self.order_start_size * float(self.quote_currency["available"])
        self.active_asks = active_ask
        self.active_bids = active_bid

    def _order_size_model(self, position, shape_parameter=-0.005):
        return 

    def _get_accounts(self):
        base_found = False
        quote_found = False
        res = self.auth.accounts
        if len(res) <= 1:
            self.ready = False
            self.logger.error("Found too few accounts - Exiting...")
            raise Exception("Too few accounts from auth")
        for o in self.auth.accounts:
            if o["currency"] == self.symbol.split("-")[0]:
                base_found = True
                self.base_currency = o
            if o["currency"] == self.symbol.split("-")[1]:
                quote_found = True
                self.quote_currency = o
        # check if both accounts where found
        if base_found and quote_found:
            if float(self.base_currency["available"]) <= 0.0 or float(self.quote_currency["available"]) <= 0.0:
                self.logger.error("The base or quote account has no available assets. Exiting...")
                raise Exception("Not enough funds")
            self.ready = True
            self.pair_currency_ratio = float(self.base_currency["available"])/float(self.quote_currency["available"])
        else:
            self.ready = False

    def update_accounts(self):
        self.auth.authenticate(verbose=False)
        self._get_accounts()


    def _print_accounts(self):
        print(f"base_currency: {self.base_currency}")
        print(f"quote_currency: {self.quote_currency}")
        print(f"pair_currency_ratio: {self.pair_currency_ratio}")
        print(f"active_asks: {self.active_asks}")
        print(f"active_bids: {self.active_bids}")
