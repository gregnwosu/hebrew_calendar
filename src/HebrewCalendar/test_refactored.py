# test add_months_and_days for 7 lunar months and 15th days with start date 2024-03-09 assert we have september 16 2024
from HebrewCalendar.refactored import add_months_and_days
import datetime as dt
import pytest


def test_feast_of_tabernacles():
   
    assert dt.datetime(2024, 9, 16) == add_months_and_days(dt.datetime(2024, 3, 9), 7, 15)
    # this fails as it returns  dt.datetime(2024, 11, 17, 0, 0)
    
    
def test_day_of_atonement():
    assert dt.datetime(2024, 9, 11) == add_months_and_days(dt.datetime(2024, 3, 9), 7, 10)
    # this fails as it returns  dt.datetime(2024, 11, 6, 0, 0)
    
def test_passover():
    assert dt.datetime(2024, 3, 23) == add_months_and_days(dt.datetime(2024, 3, 9), 1, 14)
    # this fails as it returns  dt.datetime(2024, 11, 1, 0, 0)