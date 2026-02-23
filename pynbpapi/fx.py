from datetime import date, datetime
from functools import reduce
from typing import Literal, Union

import pandas as pd

from pynbpapi.common import (
    split_dates_range_into_smaller_chunks, run_web_api_query)
from pynbpapi.ccy import Ccy
from pynbpapi.exceptions import (
    InvalidStartEndDatesException, InvalidCurrencyException)

__all__ = ["get_fx_rate", "get_fx_rates", "get_nbp_fx_tables"]


def _validate_fx_table_code(code: str) -> None:
    if code not in ["A", "B", "C"]:
        raise ValueError(f"Invalid NBP code value {code}")


def _validate_start_end_dates(start: date, end: date) -> None:
    if start > end:
        raise InvalidStartEndDatesException(start, end)


def _validate_ccys(ccys: list) -> None:
    for i in range(len(ccys)):
        ccy = ccys[i]
        if not (isinstance(ccy, str) or isinstance(ccy, Ccy)):
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
        "rate": f"{ccy.name.lower()}pln"
    }, inplace=False).reset_index(
        inplace=False,
        drop=True
    ).copy(deep=True)[["date", f"{ccy.name.lower()}pln"]]


def get_fx_rates(
        ccys: Union[str, Ccy, list[Union[str, Ccy]]],
        start: date,
        end: date,
        fmt: Literal["long", "wide"] = "long",
        fill_nas: bool = True
) -> pd.DataFrame:
    _validate_start_end_dates(start, end)
    if isinstance(ccys, str) or isinstance(ccys, Ccy):
        ccys = [ccys]
    _validate_ccys(ccys)

    datas: list[pd.DataFrame] = []
    for ccy in ccys:
        data = get_fx_rate(ccy, start, end)
        if fmt == "long":
            pair_name: str = f"{ccy.name.lower()}pln"
            data["pair"] = pair_name
            data = data.rename(columns={pair_name: "rate"})
        datas.append(data)

    if fmt == "long":
        return pd.concat(datas, axis=0)

    data = reduce(lambda x, y: pd.merge(x, y, on="date", how="outer"), datas)
    if fill_nas:
        data = data.ffill(axis=0)
        data = data.bfill(axis=0)
    return data.sort_values(by="date", ascending=True)


def get_nbp_fx_tables(
        table: Literal["A", "B", "C"],
        start: date,
        end: date
) -> pd.DataFrame:
    _validate_fx_table_code(code=table)
    _validate_start_end_dates(start, end)
    tables = run_web_api_query(
        url=f"https://api.nbp.pl/api/exchangerates/tables/"
            f"{table}/{start.isoformat()}/{end.isoformat()}/"
    )
    parsed_tables: list[pd.DataFrame] = []
    for table_ in tables:
        rates_data = pd.DataFrame(table_["rates"])
        rates_data["table"] = table_["table"]
        rates_data["no"] = table_["no"]
        rates_data["date"] = datetime.strptime(
            table_["effectiveDate"], "%Y-%m-%d").date()
        parsed_tables.append(rates_data)

    return pd.concat(
        parsed_tables, axis=0
    ).reset_index(drop=True).sort_values(
        by=["date", "currency"], ascending=[True, True]
    )
