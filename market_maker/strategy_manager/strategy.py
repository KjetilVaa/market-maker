import logging
import time
import datetime as dt



class Strategy():
    
    def __init__(self, limit_ask, limit_bid, change_treshold):
        self.logger = logging.getLogger("root")
        self.limit_ask = limit_ask
        self.limit_bid = limit_bid
        self.change_treshold = change_treshold
