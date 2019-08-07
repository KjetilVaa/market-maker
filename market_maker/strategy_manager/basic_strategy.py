import logging
import time
import datetime as dt


"""
This strategy will simply post an limit buy and sell with an spread,
and depending on which maker order gets taken, it will do the opposite to
make the spread profit.
It should get all higher level parameters from the strategy manager
"""



class BasicStrategy():

    def __init__(self, order_pairs, interval, min_spread):
        self.logger = logging.getLogger("root")
        self.metrics = None
        self.order_pairs = order_pairs
        self.ready = False

        # distance in precentage between successive order pairs.
        # each order is designed to be (INTERVAL*n)% away from the spread.
        self.interval = interval
        # minimum spread to begin trading
        self.min_spread = min_spread
        self.current_active_asks = [0.0]
        self.current_active_bids = [0.0]


    def calculate(self, metrics, ready):
        # only if spread is good
        self.metrics = metrics
        self.ready = ready

        if ready == False:
            self.logger.info("Strategy Manager not ready. Trying again")
            return
        elif metrics["spread_precentage"] >= self.min_spread:
            limit_ask, limit_bid = self._determine_limit_order(metrics["best_ask"], metrics["best_bid"])
            if limit_ask != self.current_active_asks and limit_bid != self.current_active_bids:
                self.current_active_asks = limit_ask
                self.current_active_bids = limit_bid
                self.logger.info(f"NEW ASK: {limit_ask} - NEW BID: {limit_bid} - SPREAD: {metrics['spread_precentage']}")
            else:
                self.logger.info(f"SAME ASK: {limit_ask} - SAME BID: {limit_bid} - SPREAD: {metrics['spread_precentage']}")
        else:
            self.logger.info(f"SPREAD TOO LOW - MIN_SPREAD: {self.min_spread} - SPREAD: {metrics['spread_precentage']}")
            #Cancel all orders
            return


    def _determine_limit_order(self, best_ask, best_bid):
        # only supports one order pair currently
        if self.order_pairs == 1:
            # New limit = old_best_limit - (old_best_limit * precentage_interval)
            limit_ask = best_ask - (best_ask*self.interval)
            limit_bid = best_bid - (best_bid*self.interval)
            return [limit_ask], [limit_bid]
        else:
            self.logger.error(f"Strategy does not support {self.order_pairs} - Exiting...")
            raise Exception("Strategy settings is not supported")
