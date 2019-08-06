import logging
import time

from market_maker.utils import log
from market_maker.market_data_receiver.market_data_receiver import MarketDataReceiver
from market_maker.position_manager.position_manager import PositionManager
from market_maker.strategy_manager.strategy_manager import StrategyManager

def main():

    # Should the bot run in 'SANDBOX' or 'REAL' mode?
    mode="REAL"
    exchange="coinbase_pro"
    logger = logging.getLogger("root")

    # Data receiver
    market_data_receiver = MarketDataReceiver(exchange=exchange, mode=mode)

    # Authenticate market reciever
    market_data_receiver.authenticate()
    # Wait to fully authenticate
    time.sleep(2)

    # Start the live orderbook for market receiver
    #market_data_receiver.start_orderbook()

    #Initialize the strategy manager
    #strategy_manager = StrategyManager(market_data_receiver.orderbook)

    #Initialize position manager
    position_manager = PositionManager(market_data_receiver.auth)

    # Wait for strategy and position manager to fully load
    #logger.info("Launching strategy and position manager")
    #time.sleep(3)

    # Here we start the infinite loop that listens to the orderbook
    #while True:
        # Start the strategy manager
        #strategy_manager.run()



        #time.sleep(strategy_manager.orderbook_freq)
    # Position manager





if __name__ == "__main__":
    #Logger setup
    logger = log.setup_custom_logger('root')

    #Run main program
    main()
