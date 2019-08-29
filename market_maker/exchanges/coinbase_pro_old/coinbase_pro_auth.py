import time
import logging
import cbpro
import sys
import datetime as dt
import logging

from market_maker.utils.colors import Colors
from .coinbase_pro_settings import coinbase_pro_settings as settings
from market_maker.strategy_settings import strategy_settings


class CoinbaseProAuth(cbpro.AuthenticatedClient):

    def __init__(self, mode):
        self.logger = logging.getLogger("root")
        self.mode = mode
        self.minimum_accounts = 2
        self.api_key = settings[self.mode]["API_KEY"]
        self.api_secret = settings[self.mode]["API_SECRET"]
        self.api_passphrase = settings[self.mode]["API_PASSPHRASE"]
        self.api_url = settings[self.mode]["API_URL"]
        self.accounts = []
        self.datetime_format = settings["DATETIME_FORMAT"]
        super(CoinbaseProAuth, self).__init__(self.api_key, self.api_secret, self.api_passphrase, self.api_url)

    def authenticate(self, verbose):
        self.logger.info(f"Authenticating with coinbase_pro in {self.mode} mode")
        res = self.get_accounts()
        if len(res) > self.minimum_accounts:
            self.accounts = res
            if verbose:
                self.logger.info(f"Successfully fetched following accounts from coinbase_pro")
                for o in res:
                    print(f"""Account: {o["currency"]} - Balance: {o["balance"]} - Available: {o["available"]} - Hold: {o["hold"]}""")
        else:
            self.logger.error(res)
            raise Exception(f"Unable to authenticate to coinbase_pro. Exiting...")
