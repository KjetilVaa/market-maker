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

    # Data receiver
    market_data_receiver = MarketDataReceiver(exchange=exchange, mode=mode)

    # Authenticate market reciever
    #market_data_receiver.authenticate()
    #time.sleep(2)

    # Start the live orderbook for market receiver
    market_data_receiver.start_orderbook()

    #Initialize the strategy manager
    strategy_manager = StrategyManager(market_data_receiver.orderbook)

    # Wait for orderbook to fully load
    time.sleep(5)

    # Start the strategy manager
    strategy_manager.start()

    # Position manager




if __name__ == "__main__":
    #Logger setup
    logger = log.setup_custom_logger('root')

    #Run main program
    main()
