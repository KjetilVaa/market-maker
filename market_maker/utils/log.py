from os.path import join
import logging
from market_maker.strategy_settings import strategy_settings


def setup_custom_logger(name, log_level=strategy_settings["STRATEGY"]["LOG_LEVEL"]):
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    logger.addHandler(handler)
    return logger
