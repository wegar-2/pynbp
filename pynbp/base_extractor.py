from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import typing as t
from requests import get
from json import loads


class BaseExtractor:

    def __init__(self):
        pass

    @staticmethod
    def get_default_dates_range() -> t.Tuple[date, date]:
        date_end = date.today() - timedelta(days=1)
        date_start = date_end + relativedelta(years=-1) + timedelta(days=1)
        return date_start, date_end

    @staticmethod
    def run_web_api_query(url: str) -> t.Dict:
        return loads(get(url=url).text)

    @staticmethod
    def split_dates_range_into_smaller_chunks(start: date, end: date) -> t.List[t.Tuple[date, date]]:
        if (end - start).days >= 367:
            temp = start
            out = []
            while temp < end:
                out.append((temp, temp + relativedelta(years=1) - timedelta(days=1)))
                temp = temp + relativedelta(years=1)
            out[-1] = (out[-1][0], end)
            return out
        else:
            return [(start, end)]
