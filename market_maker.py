import logging

from market_maker.utils import log
from market_maker.market_data_receiver.market_data_receiver import MarketDataReceiver
from market_maker.position_manager.position_manager import PositionManager


def main():

    # Should the bot run in 'SANDBOX' or 'REAL' mode?
    mode="SANDBOX"
    exchange="coinbase_pro"

    # Data receiver
    market_data_receiver = MarketDataReceiver(exchange=exchange, mode=mode)
    market_data_receiver.authenticate()
    market_data_receiver.start_orderbook()

    #Wait for orderbook and authentication to fully load
    time.sleep(3)

    # Position manager




if __name__ == "__main__":
    #Logger setup
    logger = log.setup_custom_logger('root')

    #Run main program
    main()
