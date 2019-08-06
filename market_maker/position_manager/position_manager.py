import time
import logging
import cbpro
import sys
import datetime as dt
import logging

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
        self.base_quote_ratio = 0.0
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
        self._calculate_positions()


    def _calculate_positions(self):
        #trade size =  wallet_amount * percentage_each_trade
        if self.base_quote_ratio >= 1.25 or self.base_quote_ratio <= 0.75:
            self.logger.info(f"A base_quote balance ratio of {self.base_quote_ratio} is not within the threshold. Exiting...")
            raise Exception("Balance ratio out of comfort zone.")
        active_ask = self.order_start_size * base_currency["available"]
        active_bid = self.order_start_size * quote_currency["available"]
        self.active_asks = active_ask
        self.active_bids = active_bid


    def _get_accounts(self):
        base_found = False
        quote_found = False
        res = self.auth.accounts
        if len(res) <= 1:
            self.ready = False
            self.logger.error("Found too few accounts - Exiting...")
            raise Exception("Too few accounts from auth")
        for o in self.accounts:
            if o["currency"] == self.symbol.split("-")[0]:
                base_found = True
                self.base_currency = o
            if o["currency"] == self.symbol.split("-")[1]:
                quote_found = True
                self.quote_currency = o
        # check if both accounts where found
        if base_found and quote_found:
            self.ready = True
            self.pair_currency_ratio = self.base_currency["currency"]/self.quote_currency["currency"]
        else:
            self.ready = False

    def update_accounts(self):
        self.auth.authenticate(verbose=False)
        time.sleep(0.5)
        self._get_accounts()





    def start(self, ask_limit, bid_limit):
