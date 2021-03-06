import logging
import time
import sys
import traceback

from market_maker.utils import log
from market_maker.market_data_receiver.market_data_receiver import MarketDataReceiver
from market_maker.position_manager.position_manager import PositionManager
from market_maker.strategy_manager.strategy_manager import StrategyManager
from market_maker.trade_manager.trade_manager import TradeManager


def main():

    # Should the bot run in 'SANDBOX' or 'REAL' mode?
    mode="REAL"
    exchange="coinbasepro"
    logger = logging.getLogger("root")

    # Data receiver
    market_data_receiver = MarketDataReceiver(exchange=exchange, mode=mode)


    # Start the live orderbook for market receiver
    market_data_receiver.get_orderbook()
    market_data_receiver.get_balance()

    # Wait for orderbook to load completely
    #time.sleep(0.5)

    #Initialize the strategy manager
    strategy_manager = StrategyManager(market_data_receiver.exchange.orderbook)
    strategy_manager.run()

    """
    #Initialize position manager
    position_manager = PositionManager(market_data_receiver.auth)

    #Initialize trade executor
    trade_manager = TradeManager(position_manager, strategy_manager)

    def session_summary(starting_inv, current_inv, inv_ratio):
        print("****** SESSION SUMMARY ******")
        print(f"CURRENT INVENTORY RATIO: {inv_ratio}")
        print(f"STARTING INVENTORY: {starting_inv}")
        print(f"CURRENT INVENTORY: {current_inv}")
        print(f"PROFIT: {starting_inv-current_inv}")

    ##########################################
    #               MAIN LOOP                #
    ##########################################

    try:
        i = 0
        while True:
            logger.info(f"Starting iteration - {i}")
            if market_data_receiver.orderbook.stop == True:
                logger.error(f"Orderbook stop status: {market_data_receiver.orderbook.stop}")
                raise Exception("Orderbook error.")
            #broadcast current position
            trade_manager.broadcast_position()
            #Run the position manager
            position_manager.run(strategy_manager.orderbook.best_ask)
            #Run the strategy manager
            if position_manager.ready:
                strategy_manager.run()
            #Run the trade executor
            if strategy_manager.ready:
                trade_manager.run()
            #Check the trade executor is ready
            if not trade_manager.ready:
                raise Exception("Trade manager not ready")
            #Print session summary
            session_summary(position_manager.starting_total_quote_currency, position_manager.current_total_quote_currency, position_manager.pair_currency_ratio)
            #Next iteration
            i += 1
            time.sleep(strategy_manager.orderbook_freq) #defaults to 5 seconds
    except Exception as e:
        logger.error(f"Critical error ocurred: {e}")
        market_data_receiver.close_orderbook()
        traceback.print_exc()
        sys.exit(1)

    """


if __name__ == "__main__":
    #Logger setup
    logger = log.setup_custom_logger('root')

    #Run main program
    main()
