from datetime import date
import pandas as pd
from pynbp.common import (run_web_api_query,
                          split_dates_range_into_smaller_chunks)

__all__ = ["get_gold_prices"]


def get_gold_prices(start: date, end: date):
    chunks = split_dates_range_into_smaller_chunks(start=start, end=end)
    dfs = []
    for start_, end_ in chunks:
        dfs.append(get_gold_prices_chunk(start=start_, end=end_))
    return pd.concat(dfs, axis=0).reset_index(
        drop=True, inplace=False).copy(deep=True)


def get_gold_prices_chunk(start: date, end: date) -> pd.DataFrame:
    return pd.DataFrame(
        data=run_web_api_query(
            url=get_gold_prices_url(start=start, end=end))
    ).rename(columns={"data": "date", "cena": "price_of_1g_of_gold_in_pln"},
             inplace=False).copy(deep=True)


def get_gold_prices_url(start: date, end: date) -> str:
    return (f"http://api.nbp.pl/api/cenyzlota/"
            f"{start.isoformat()}/{end.isoformat()}/")
