from pynbp.base_extractor import BaseExtractor
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


def test_get_default_dates_range():
    start, end = BaseExtractor.get_default_dates_range()

    assert end == date.today() - timedelta(days=1)
    assert start == end + relativedelta(years=-1) + timedelta(days=1)


def test_split_dates_range_into_smaller_chunks():
    l = BaseExtractor.split_dates_range_into_smaller_chunks(start=date(2019, 1, 1), end=date(2022, 9, 30))

    assert isinstance(l, list)
    assert len(l) == 4
    assert l[0][0] == date(2019, 1, 1)
    assert l[2][1] == date(2021, 12, 31)
