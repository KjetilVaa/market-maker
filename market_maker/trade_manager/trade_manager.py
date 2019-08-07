import time
import logging
import cbpro
import sys
import datetime as dt
import logging
import numpy as np
from multiprocessing import Process

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
        self.started_time = dt.datetime.now()
        #Total ask orders filled
        self.amount_sold = 0.0
        #Total bid orders filled
        self.amount_bought = 0.0
        #Total ask orders filled - Total bid orders filles
        self.position = 0.0
        #Total orders filled
        self.total_trades = []
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
            price = self.strategy_manager.strategy.current_active_asks[0]
            pos1 = {"side": "sell", "price": price, "size": size}
            #for bid
            size = self.position_manager.current_active_bid[0]
            price = self.strategy_manager.strategy.current_active_bids[0]
            pos2 = {"side": "buy", "price": price, "size": size}
            #execute in parallel
            self._place_two_limit_orders(pos1, pos2)
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
        # Get all filled trades and calculate amount sold, amount bought, and position
        all_fills = self._get_all_fills()
        all_fills = list(all_fills)
        # Filter out trades that happened earlier than this bot run session
        if len(all_fills) < 1:
            self.total_trades = []
            self.logger.info("Found no filled orders for strategy_settings['STRATEGY']['SYMBOL']")
            self.position_manager._calculate_current_position(self.position)
        else:
            self.total_trades = []
            for o in all_fills:
                fill_date = dt.datetime.strptime(o["created_at"], self.position_manager.auth.datetime_format)
                # trade happened after we started the bot
                if fill_date >= self.started_time:
                    self.total_trades.append(o)
                    if o["side"] == "buy":
                        self.amount_bought += o["size"] * o["price"]
                    if o["side"] == "sell":
                        self.amount_sold += o["size"] * o["price"]

            # now pass the new position to position manager
            if len(self.total_trades) < 1:
                self.logger.info("No filled trades found.")
            self.position = self.amount_sold - self.amount_bought
            self.logger.info(f"POSITION: {self.position}")
            self.position_manager._calculate_current_position(self.position)


    # place two limit orders in parallell
    def _place_two_limit_orders(self, pos1, pos2):
        p1 = Process(target=self._place_limit_order(pos1["side"], pos1["price"], pos1["size"]))
        p1.start()
        p2 = Process(target=self._place_limit_order(pos2["side"], pos2["price"], pos2["size"]))
        p2.start()
        p1.join()
        p2.join()

    # place limit order
    def _place_limit_order(self, side, price, size):
        self.logger.info(f"{strategy_settings['STRATEGY']['SYMBOL']} - NEW {side} ORDER - PRICE: {price} - SIZE: {size}")
        return self.position_manager.auth.place_limit_order(product_id=strategy_settings["STRATEGY"]["SYMBOL"], side=side, price=price, size=size)

    # get all open orders
    def _get_current_trades(self):
        self.logger.info(f"Fething current open trades")
        return self.position_manager.auth.get_orders(product_id=strategy_settings["STRATEGY"]["SYMBOL"], status="open")

    # get all filled orders
    def _get_all_fills(self):
        self.logger.info(f"Fetching all filled orders for {strategy_settings['STRATEGY']['SYMBOL']}")
        return self.position_manager.auth.get_fills(product_id=strategy_settings["STRATEGY"]["SYMBOL"])

    # cancel a specific order
    def _cancel_open_order(self, order_id):
        self.logger.info(f"Cancelling order: {order_id}")
        return self.position_manager.auth.cancel_order(order_id)

    # cancel all open orders
    def _cancel_all_open_orders(self):
        self.logger.info(f"Cancelling all open orders")
        return self.position_manager.auth.cancel_all(product_id=strategy_settings["STRATEGY"]["SYMBOL"])

    def _trading_summary(self):
        print("trading summary not done")
        #TODO: Should return a summary of profits and other metrics for this session
