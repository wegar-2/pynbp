from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from pynbpapi.common import (get_default_dates_range,
                             split_dates_range_into_smaller_chunks)


def test_get_default_dates_range():
    start, end = get_default_dates_range()
    assert end == date.today() - timedelta(days=1)
    assert start == end + relativedelta(years=-1) + timedelta(days=1)


def test_split_dates_range_into_smaller_chunks():
    list_ = split_dates_range_into_smaller_chunks(
        start=date(2019, 1, 1), end=date(2022, 9, 30))
    assert isinstance(list_, list)
    assert len(list_) == 4
    assert list_[0][0] == date(2019, 1, 1)
    assert list_[2][1] == date(2021, 12, 31)
