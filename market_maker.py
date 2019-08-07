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
    exchange="coinbase_pro"
    logger = logging.getLogger("root")

    # Data receiver
    market_data_receiver = MarketDataReceiver(exchange=exchange, mode=mode)

    # Start the live orderbook for market receiver
    market_data_receiver.start_orderbook()

    # Wait for orderbook to load completely
    time.sleep(2)

    #Initialize the strategy manager
    strategy_manager = StrategyManager(market_data_receiver.orderbook)

    #Initialize position manager
    position_manager = PositionManager(market_data_receiver.auth)

    #Initialize trade executor
    trade_manager = TradeManager(position_manager, strategy_manager)

    ##########################################
    #               MAIN LOOP                #
    ##########################################

    try:
        i = 0
        while True:
            logger.info(f"Starting iteration - {i}")
            if market_data_receiver.orderbook.stop == True:
                logger.error(f"Orderbook status: {market_data_receiver.orderbook.stop}")
                raise Exception("Orderbook error.")
            #broadcast current position
            trade_manager.broadcast_position()
            #Run the position manager
            position_manager.run()
            #Run the strategy manager
            if position_manager.ready:
                strategy_manager.run()
            #Run the trade executor
            if strategy_manager.ready:
                trade_manager.run()
            #Next iteration
            i += 1
            time.sleep(strategy_manager.orderbook_freq) #defaults to 5 seconds
    except Exception as e:
        logger.error(f"Critical error ocurred: {e}")
        market_data_receiver.close_orderbook()
        traceback.print_exc()
        sys.exit(1)



if __name__ == "__main__":
    #Logger setup
    logger = log.setup_custom_logger('root')

    #Run main program
    main()
