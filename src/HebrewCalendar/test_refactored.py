# test add_months_and_days for 7 lunar months and 15th days with start date 2024-03-09 assert we have september 16 2024
from HebrewCalendar.refactored import add_months_and_days, enumerate_sabbaths
import datetime as dt


def test_feast_of_tabernacles():
    assert dt.datetime(2024, 9, 16) == add_months_and_days(dt.datetime(2024, 3, 9), 7, 15)


def test_day_of_atonement():
    assert dt.datetime(2024, 9, 11) == add_months_and_days(dt.datetime(2024, 3, 9), 7, 10)


def test_passover():
    assert dt.datetime(2024, 3, 23) == add_months_and_days(dt.datetime(2024, 3, 9), 1, 14)


def test_new_moon_is_sabbath():
    start = dt.datetime(2024, 3, 9)
    end = start + dt.timedelta(days=60)
    new_moons = [add_months_and_days(start, m, 0).date() for m in range(1, 3)]
    sabbaths = enumerate_sabbaths(new_moons, end.date())
    assert new_moons[0] in sabbaths


def test_two_day_sabbath_when_month_29_days():
    start = dt.datetime(2024, 3, 9)
    end = start + dt.timedelta(days=60)
    new_moons = [add_months_and_days(start, m, 0).date() for m in range(1, 3)]
    sabbaths = enumerate_sabbaths(new_moons, end.date())
    second_nm = new_moons[1]
    last_before_second = max(d for d in sabbaths if d < second_nm)
    assert (second_nm - last_before_second).days == 1

