from os.path import join
import logging


strategy_settings = {

    "STRATEGY" : {
        # Instrument to market make on. NB: Must be in the format -> BASE-QUOTE
        "SYMBOL": "BTC-DAI",

        #######################################################################
        # Order Size & Spreads
        ########################################################################

        # How many pairs of buy/sell orders to keep up by default
        "ORDER_PAIRS" : 1,

        # ORDER_START_SIZE will be the trade size measured in percentage of total account
        # Number of contracts from level 1 to ORDER_PAIRS - 1 will follow the function
        # [ORDER_START_SIZE + ORDER_STEP_SIZE (Level -1)] (measured in percentrage, e.g 0.005 = 0.5%)
        "ORDER_START_SIZE": 0.01,
        "ORDER_STEP_SIZE": 0.01,


        # Distance between successive orders, as a percentage (example: 0.005 for 0.5%)
        "INTERVAL": 0.005,

        # Minimum spread to maintain, in percent, between asks & bids
        "MIN_SPREAD": 0.01,

        # If True, market-maker will place orders just inside the existing spread and work the interval % outwards,
        # rather than starting in the middle and killing potentially profitable spreads.
        "MAINTAIN_SPREADS": True,

        # This number defines far much the price of an existing order can be from a desired order before it is amended.
        # This is useful for avoiding unnecessary calls and maintaining your ratelimits.
        #
        # Further information:
        # Each order is designed to be (INTERVAL*n)% away from the spread.
        # If the spread changes and the order has moved outside its bound defined as
        # abs((desired_order['price'] / order['price']) - 1) > settings.RELIST_INTERVAL)
        # it will be resubmitted.
        #
        # 0.01 == 1%
        "RELIST_INTERVAL": 0.01,

        ########################################################################################################################
        # Trading Behavior
        ########################################################################################################################

        # Position limits - set to True to activate. Values are in contracts.
        # If you exceed a position limit, the bot will log and stop quoting that side.
        "CHECK_POSITION_LIMITS": False,
        "MIN_POSITION": -10000,
        "MAX_POSITION": 10000,

        # If True, will only send orders that rest in the book (ExecInst: ParticipateDoNotInitiate).
        # Use to guarantee a maker rebate.
        # However -- orders that would have matched immediately will instead cancel, and you may end up with
        # unexpected delta. Be careful.
        "POST_ONLY": False,


        ########################################################################################################################
        # Misc Behavior, Technicals
        ########################################################################################################################

        # If true, don't set up any orders, just say what we would do
        # DRY_RUN = True
        "DRY_RUN": False,

        # How often to re-check and replace orders.
        # Generally, it's safe to make this short because we're fetching from websockets. But if too many
        # order amend/replaces are done, you may hit a ratelimit. If so, email BitMEX if you feel you need a higher limit.
        "LOOP_INTERVAL": 5,


        # Wait times between orders / errors
        "API_REST_INTERVAL": 1,
        "API_ERROR_INTERVAL": 10,
        "TIMEOUT": 7,

        # If we're doing a dry run, use these numbers for BTC balances
        "DRY_BTC": 50,


        # To uniquely identify orders placed by this bot, the bot sends a ClOrdID (Client order ID) that is attached
        # to each order so its source can be identified. This keeps the market maker from cancelling orders that are
        # manually placed, or orders placed by another bot.
        #
        # If you are running multiple bots on the same symbol, give them unique ORDERID_PREFIXes - otherwise they will
        # cancel each others' orders.
        # Max length is 13 characters.
        "ORDERID_PREFIX": "mm_bitmex_",

        # If any of these files (and this file) changes, reload the bot.
        #"WATCHED_FILES" = [join('market_maker', 'market_maker.py'), join('market_maker', 'bitmex.py'), 'settings.py']

        ########################################################################################################################
        # Logging
        ########################################################################################################################

        # Available levels: logging.(DEBUG|INFO|WARN|ERROR)
        "LOG_LEVEL": logging.INFO

    }

}
