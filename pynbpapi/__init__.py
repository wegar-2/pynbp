from .ccy import Ccy
from .fx import get_fx_rate
from .gold import get_gold_prices
from .interest_rates import get_interest_rates_table

__all__ = [
    "Ccy",
    "get_fx_rate",
    "get_gold_prices",
    "get_interest_rates_table"
]

import logging


def configure_logging():
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    logger = logging.getLogger()
    if logger.hasHandlers():
        logger.handlers.clear()
    logger.setLevel(logging.INFO)
    logger.addHandler(console_handler)


configure_logging()
