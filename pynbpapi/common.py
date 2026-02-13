from datetime import date, timedelta
from json import loads
from dateutil.relativedelta import relativedelta
from requests import get

__all__ = [
    "get_default_dates_range",
    "run_web_api_query",
    "split_dates_range_into_smaller_chunks"
]


def get_default_dates_range() -> tuple[date, date]:
    date_end = date.today() - timedelta(days=1)
    date_start = date_end + relativedelta(years=-1) + timedelta(days=1)
    return date_start, date_end


def run_web_api_query(url: str) -> dict:
    return loads(get(url=url, timeout=180).text)


def split_dates_range_into_smaller_chunks(
        start: date,
        end: date
) -> list[tuple[date, date]]:
    if (end - start).days >= 367:
        temp = start
        out = []
        while temp < end:
            out.append(
                (temp, temp + relativedelta(years=1) - timedelta(days=1))
            )
            temp = temp + relativedelta(years=1)
        out[-1] = (out[-1][0], end)
        return out
    return [(start, end)]
