from datetime import date

__all__ = [
    "InvalidStartEndDatesException",
    "InvalidCurrencyException"
]


class InvalidStartEndDatesException(ValueError):
    def __init__(self, start: date, end: date):
        self.message: str = (f"Inconsistent start={start.isoformat()} and "
                             f"end={end.isoformat()} dates! ")


class InvalidCurrencyException(ValueError):
    def __init__(self, ccy):
        self.message = f""
