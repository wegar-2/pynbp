from datetime import date
import pandas as pd
from pynbp.common import (split_dates_range_into_smaller_chunks,
                          run_web_api_query)
from pynbp.currency import Currency

__all__ = ["get_fx_rates_for_currency"]


def parse_fx_json(json_) -> pd.DataFrame:
    return pd.DataFrame(data=json_["rates"]).rename(
        columns={"effectiveDate": "date", "mid": "rate"}
    ).drop(columns=["no"], inplace=False)


def get_fx_api_query(ccy: Currency, start: date, end: date) -> str:
    return (f"http://api.nbp.pl/api/exchangerates"
            f"/rates/a/{ccy.name.lower()}/{start.isoformat()}/"
            f"{end.isoformat()}/")


def get_fx_rates_for_currency(
        ccy: Currency,
        start: date,
        end: date
) -> pd.DataFrame:
    chunks = split_dates_range_into_smaller_chunks(start=start, end=end)
    list_dfs = []
    for start_, end_ in chunks:
        list_dfs.append(parse_fx_json(
            json_=run_web_api_query(
                url=get_fx_api_query(ccy=ccy, start=start_, end=end_))))
    return pd.concat(list_dfs, axis=0).rename(
        columns={"rate": f"{ccy.name.lower()}pln_rate"}, inplace=False
    ).reset_index(inplace=False, drop=True).copy(deep=True)
