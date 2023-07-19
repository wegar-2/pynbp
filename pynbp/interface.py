from datetime import date

import pandas as pd

from pynbp.fx_extractor import FxExtractor
from pynbp.interest_rates_extractor import InterestRatesExtractor
from pynbp.gold_price_extractor import GoldPriceExtractor


def get_fx_rates_for_currency(iso_code: str, start: date, end: date) -> pd.DataFrame:
    return FxExtractor().get_fx_rates_for_currency(iso_code=iso_code, start=start, end=end)


def get_gold_prices(start: date, end: date) -> pd.DataFrame:
    return GoldPriceExtractor().get_gold_prices(start=start, end=end)


def get_interest_rates_table() -> pd.DataFrame:
    return InterestRatesExtractor().get_interest_rates_table()
