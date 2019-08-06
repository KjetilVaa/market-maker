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
- Tell strategy manager of the current position
- Store number of total trades
- Store amount sold and amount bought for length of program
- Store current open orders
- Execute buy/sell orders based on information given by position manager
  and strategy manager
"""


class TradeManager():

    def __init__(self, position_manager, strategy_manager):
        self.logger = logging.getLogger("root")
        self.ready = False
        #Total ask orders filled
        self.amount_sold = 0.0
        #Total bid orders filled
        self.amount_bought = 0.0
        #Total ask orders fille - Total bid orders filles
        self.position = 0.0
        #Total orders filled
        self.total_trades = 0
        #Current open ask orders
        self.current_open_asks = []
        #Current open bid orders
        self.current_open_bids = []
        #Total open orders
        self.nb_open_orders = []

        #If one side gets taken, but not the other, we wait one cycle
        self.is_trailing_order = False

        # Managers
        self.position_manager = position_manager
        self.strategy_manager = strategy_manager

    def run(self):
        if not (self.position_manager.ready and self.strategy_manager.ready):
            self.logger.error("Position manager status: {self.position_manager.ready} - Strategy manager status: {self.strategy_manager.ready}")
            self.ready = False
            raise Exception("Managers not ready to execute trades")
        #Get current trades
        current_orders = self._get_current_trades()
        self.nb_open_orders = len(current_orders)

        #If there are 0 or 2 open orders, we open one limit ask and one limit bid
        if self.nb_open_orders == 0 or self.nb_open_orders == 2:
            self.ready = True
            #for ask
            size = self.position_manager.current_active_ask[0]
            price = self.strategy_manager.strategy.active_asks[0]
            self._place_limit_order(side="sell", price=price, size=size)
            #for bid
            size = self.position_manager.current_active_bid[0]
            price = self.strategy_manager.strategy.active_bids[0]
            self._place_limit_order(side="buy", price=price, size=size)
        #If there are one open order, we wait five seconds before cancelling it
        elif self.nb_open_orders == 1:
            self.ready = True
            # Then we have already waited one cycle and can cancel order
            if self.is_trailing_order:
                self._cancel_open_order(current_orders[0]["id"])
                self.is_trailing_order = False
        else:
            self.logger.info("Failed to read number of open orders. Existing...")
            self.ready = False
            raise Exception("Trade manager failed to get orders")




    def broadcast_position(self):
        self.position_manager._calculate_current_position(self.amount_sold, self.amount_bought)

    # place limit order
    def _place_limit_order(self, side, price, size):
        return self.position_manager.auth.place_limit_order(product_id=strategy_settings["STRATEGY"]["SYMBOL"], side=side, price=price, size=size)
    # get all open orders
    def _get_current_trades(self):
        return self.position_manager.auth.get_orders(product_id=strategy_settings["STRATEGY"]["SYMBOL"], status="open")
    # get all filled orders
    def _get_all_fills(self):
        return self.position_manager.auth.get_fills(product_id=strategy_settings["STRATEGY"]["SYMBOL"])
    # cancel a specific order
    def _cancel_open_order(self, order_id):
        return self.position_manager.auth.cancel_order(order_id)
    # cancel all open orders
    def _cancel_all_open_orders(self):
        return self.position_manager.auth.cancel_all(product_id=strategy_settings["STRATEGY"]["SYMBOL"])
