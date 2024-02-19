from datetime import date
import pandas as pd
from pynbp.common import (split_dates_range_into_smaller_chunks,
                          run_web_api_query)
from pynbp.constants import allowed_foreign_currencies_iso_codes


def parse_fx_json(json_) -> pd.DataFrame:
    return pd.DataFrame(data=json_["rates"]).rename(
        columns={"effectiveDate": "date", "mid": "rate"}).drop(columns=["no"], inplace=False)


def get_fx_api_query(iso_code: str, start: date, end: date) -> str:
    return f"http://api.nbp.pl/api/exchangerates" \
           f"/rates/a/{iso_code}/{start.isoformat()}/{end.isoformat()}/"


def get_fx_rates_for_currency(
        iso_code: str, start: date, end: date) -> pd.DataFrame:
    if iso_code.lower() not in allowed_foreign_currencies_iso_codes:
        raise ValueError(f"Invalid parameter {iso_code=} passed to function "
                         f"get_fx_rates_for_currency")
    chunks = split_dates_range_into_smaller_chunks(start=start, end=end)
    list_dfs = []
    for start_, end_ in chunks:
        list_dfs.append(parse_fx_json(
            json_=run_web_api_query(
                url=get_fx_api_query(
                    iso_code=iso_code, start=start_, end=end_))
        ))
    return pd.concat(list_dfs, axis=0).rename(
        columns={"rate": f"{iso_code}pln_rate"}, inplace=False).reset_index(
        inplace=False, drop=True
    ).copy(deep=True)

