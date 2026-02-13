from typing import Literal, Union

from datetime import date
import pandas as pd

from pynbpapi.common import (
    split_dates_range_into_smaller_chunks, run_web_api_query)
from pynbpapi.ccy import Ccy
from pynbpapi.exceptions import (
    InvalidStartEndDatesException, InvalidCurrencyException)

__all__ = ["get_fx_rate", "get_fx_rates"]


def _validate_fx_table_code(code: str):
    if code not in ["A", "B", "C"]:
        raise ValueError("")


def _validate_start_end_dates(start: date, end: date) -> None:
    if start > end:
        raise InvalidStartEndDatesException(start, end)


def _validate_ccys(ccys: list) -> None:
    for i in range(len(ccys)):
        ccy = ccys[i]
        if not isinstance(ccy, str) or not isinstance(ccy, Ccy):
            raise TypeError(
                f"Encountered ccy of invalid type: {type(ccy)=}"
            )
        try:
            if isinstance(ccy, str):
                ccy = Ccy(ccy)
        except ValueError:
            raise InvalidCurrencyException(ccy=ccy)
        ccys[i] = ccy


def _parse_fx_json(json_) -> pd.DataFrame:
    return pd.DataFrame(data=json_["rates"]).rename(
        columns={"effectiveDate": "date", "mid": "rate"}
    ).drop(columns=["no"], inplace=False)


def _get_fx_api_query(ccy: Ccy, start: date, end: date) -> str:
    return (f"https://api.nbp.pl/api/exchangerates"
            f"/rates/a/{ccy.name.lower()}/{start.isoformat()}/"
            f"{end.isoformat()}/")


def get_fx_rate(
        ccy: Ccy | str,
        start: date,
        end: date
) -> pd.DataFrame:
    chunks = split_dates_range_into_smaller_chunks(start=start, end=end)
    list_dfs = []
    for start_, end_ in chunks:
        list_dfs.append(
            _parse_fx_json(
                json_=run_web_api_query(
                    url=_get_fx_api_query(ccy=ccy, start=start_, end=end_)
                )
            )
        )
    return pd.concat(
        list_dfs,
        axis=0
    ).rename(columns={
        "rate": f"{ccy.name.lower()}pln_rate"
    }, inplace=False).reset_index(
        inplace=False,
        drop=True
    ).copy(deep=True)


def get_fx_rates(
        ccys: Union[str, Ccy, list[Union[str, Ccy]]],
        start: date,
        end: date,
        fmt: Literal["long", "wide"]
) -> pd.DataFrame:
    _validate_start_end_dates(start, end)
    if isinstance(ccys, str) or isinstance(ccys, Ccy):
        ccys = [ccys]
    _validate_ccys(ccys)

    datas: list[pd.DataFrame] = []
    for ccy in ccys:
        datas.append(
            get_fx_rate(ccy, start, end)
        )

    if fmt == "long":
        return pd.concat(datas, axis=0)

    return pd.DataFrame()


def get_nbp_fx_table(
        table: Literal["A", "B", "C"],
        date_: date
) -> pd.DataFrame:
    _validate_fx_table_code(code=table)

    return pd.DataFrame()
