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
For every iteration:
- Store the amount of available base and quote asset on the chosen exchange
- Store the ratio (base/quote) to observe the inventory don't get one-sided
- Store the bid and ask order size
    a. There must always be size for both sides in case we need to
    quote new bid and ask at this iteration
    b. The order size will be dynamically chosen based on the current position
    (from the trade manager) to maintain a good inventory ratio
"""

class PositionManager():


    def __init__(self, auth):
        self.logger = logging.getLogger("root")
        self.auth = auth
        self.symbol = strategy_settings["STRATEGY"]["SYMBOL"]
        self.ready = False
        self.starting_base_available = None
        self.starting_quote_available = None
        self.base_currency = None
        self.quote_currency = None
        self.pair_currency_ratio = None
        self.active_asks_size = [0.0]
        self.active_bids_size = [0.0]
        self.is_first_iteration = True
        self.position = 0.0
        """
        below are some important strategy parameters from the settings file
        """
        self.order_start_size = strategy_settings["STRATEGY"]["ORDER_START_SIZE"]
        self.order_step_size = strategy_settings["STRATEGY"]["ORDER_STEP_SIZE"]
        self.shape_parameter = strategy_settings["STRATEGY"]["SHAPE_PARAMETER"]


    def run(self):
        self.logger.info("Updating account details - Calculating trade posistions")
        self._update_accounts()
        if self.ready:
            self._calculate_current_position()
            self._calculate_positions()
            self._print_accounts()
        else:
            self.logger.error("Is not ready. Exiting")
            raise Exception("Failed to update base and quote accounts.")


    def _calculate_positions(self):
        active_ask_size = 0.0
        active_bid_size = 0.0
        #if inventory is too unbalanced, abort.
        if self.pair_currency_ratio >= 1.25 or self.pair_currency_ratio <= 0.75:
            self.logger.info(f"A pair_currency_ratio of {self.pair_currency_ratio} is not within the threshold. Exiting...")
            raise Exception("Balance ratio supassed threshold")
        #if position is positive, make sell order size bigger
        if self.position > 0:
            active_ask_size = self.order_start_size
            active_bid_size = self._dynamic_order_size(self.position)
        #if position is negative, make buy order size bigger
        if self.position < 0:
            active_bid_size = self.order_start_size
            active_ask_size = self._dynamic_order_size(self.position)
        #if position is zero, make buy order size = sell order size
        if self.position == 0:
            active_ask_size = self.order_start_size
            active_bid_size = self.order_start_size

        self.active_asks_size = [active_ask_size]
        self.active_bids_size = [active_bids_size]


    def _dynamic_order_size(self, position):
        return self.order.order_start_size * np.exp(self.shape_parameter*position)

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
                self.ready = False
                raise Exception("Not enough funds")
            self.ready = True
            self.pair_currency_ratio = float(self.base_currency["available"])/float(self.quote_currency["available"])
            if self.is_first_iteration:
                self.starting_base_available = float(self.base_currency["available"])
                self.starting_quote_available = float(self.quote_currency["available"])
        else:
            self.ready = False

    def _update_accounts(self):
        self.auth.authenticate(verbose=False)
        self._get_accounts()

    def _print_accounts(self):
        print(f"pair_currency_ratio: {self.pair_currency_ratio}")
        print(f"position: {self.position}")
        print(f"active_asks: {self.active_asks}")
        print(f"active_bids: {self.active_bids}")

    def _calculate_current_position(self, amount_sold, amount_bought):
        self.position = amount_sold - amount_bought
