# test add_months_and_days for 7 lunar months and 15th days with start date 2024-03-09 assert we have september 16 2024
from HebrewCalendar.refactored import add_months_and_days, get_moon_phase
import datetime as dt
import pytest
#https://www.youtube.com/@gmsnewmoonshighholydays5488

def test_feast_of_tabernacles():
    expected_date = dt.datetime(2024, 9, 16)
    lunar_year_start = dt.datetime(2024, 3, 9)
    result = add_months_and_days(lunar_year_start, 7, 15)
    assert expected_date == result, f"Expected {expected_date}, got {result}"
    
def test_feast_of_trumpets():
    expected_date = dt.datetime(2024, 7, 29)
    lunar_year_start = dt.datetime(2024, 3, 9)
    result = add_months_and_days(lunar_year_start, 6, 1)
    assert expected_date == result, f"Expected {expected_date}, got {result}"
    
def test_day_of_atonement():
    expected_date = dt.datetime(2024, 9, 11)
    lunar_year_start = dt.datetime(2024, 3, 9)
    result = add_months_and_days(lunar_year_start, 7, 10)
    assert expected_date == result, f"Expected {expected_date}, got {result}"
    
def test_passover():
    expected_date = dt.datetime(2024, 3, 23)
    lunar_year_start = dt.datetime(2024, 3, 9)
    result = add_months_and_days(lunar_year_start, 1, 14)
    assert expected_date == result, f"Expected {expected_date}, got {result}"

# Tests for 2025 feast days
def test_passover_2025():
    expected_date = dt.datetime(2025, 4, 12 + 14 - 1)  # 14 days after new moon
    lunar_year_start = dt.datetime(2025, 2, 12)  # First new moon of 2025
    result = add_months_and_days(lunar_year_start, 2, 14)  # 2nd month after first new moon
    assert expected_date == result, f"Expected {expected_date}, got {result}"
    
def test_feast_of_tabernacles_2025():
    expected_date = dt.datetime(2025, 9, 7 + 15 - 1)  # 15 days after new moon
    lunar_year_start = dt.datetime(2025, 2, 12)  # First new moon of 2025
    result = add_months_and_days(lunar_year_start, 8, 15)  # 8th month after first new moon
    assert expected_date == result, f"Expected {expected_date}, got {result}"

# Tests for 2026 feast days
def test_passover_2026():
    expected_date = dt.datetime(2026, 3, 3 + 14 - 1)  # 14 days after new moon
    lunar_year_start = dt.datetime(2026, 2, 1)  # First new moon of 2026
    result = add_months_and_days(lunar_year_start, 2, 14)  # 2nd month after first new moon
    assert expected_date == result, f"Expected {expected_date}, got {result}"
    
def test_feast_of_trumpets_2026():
    expected_date = dt.datetime(2026, 9, 26 + 1 - 1)  # 1 day after new moon
    lunar_year_start = dt.datetime(2026, 2, 1)  # First new moon of 2026
    result = add_months_and_days(lunar_year_start, 8, 1)  # 8th month after first new moon
    assert expected_date == result, f"Expected {expected_date}, got {result}"
    
    
def test_get_phase_for_lunar_new_year_whichis_march_9_2024():
    march_9_phase, march_9_angle = get_moon_phase(dt.datetime(2024, 3, 9).date())
    assert march_9_phase == "New Moon", f"Expected New Moon but got {march_9_phase} for {dt.datetime(2024, 3, 9).date()} angle is {march_9_angle} "
    
def test_5_june_2024_should_be_new_moon():
    june_5_phase, june_5_angle = get_moon_phase(dt.datetime(2024, 6, 5).date())
    june_6_phase, june_6_angle = get_moon_phase(dt.datetime(2024, 6, 6).date())
    assert june_5_phase == "New Moon" , f"Expected  equal to New Moon but got {june_5_phase} for {dt.datetime(2024, 6, 5).date()} angle is {june_5_angle} should  be new moon but {june_6_angle } should be not be new moon"
    assert june_6_phase != "New Moon" , f"Expected not New Moon but got {june_6_phase} for {dt.datetime(2024, 6, 6).date()} angle is {june_6_angle} should not be new moon but {june_5_angle } should be  be new moon"
    
def test_2_oct_2024_should_be_new_moon():
    oct_1_phase, oct_1_angle = get_moon_phase(dt.datetime(2024, 10, 1).date())
    oct_2_phase, oct_2_angle = get_moon_phase(dt.datetime(2024, 10, 2).date())
    assert oct_1_phase != "New Moon" , f"Expected not equal to New Moon but got {oct_1_phase} for {dt.datetime(2024, 10, 1).date()} angle is {oct_1_angle} shouuld not be new moon but {oct_2_angle } should be new moon"
    assert oct_2_phase == "New Moon" , f"Expected New Moon but got {oct_2_phase} for {dt.datetime(2024, 10, 2).date()} angle is {oct_2_angle} "
    
def test_7_may_should_be_new_moon():
    may_6_phase, may_6_angle = get_moon_phase(dt.datetime(2024, 5, 6).date())
    may_7_phase, may_7_angle = get_moon_phase(dt.datetime(2024, 5, 7).date())
    assert may_6_phase != "New Moon" , f"Expected not equal to New Moon but got {may_6_phase} for {dt.datetime(2024, 5, 6).date()} angle is {may_6_angle} shouuld not be new moon but {may_7_angle } should be new moon"
    assert may_7_phase == "New Moon" , f"Expected New Moon but got {may_7_phase} for {dt.datetime(2024, 5, 7).date()} angle is {may_7_angle} should be new moon but {may_6_angle } should not be new moon"
    
# Tests for 2025 new moons
def test_12_feb_2025_should_be_new_moon():
    feb_11_phase, feb_11_angle = get_moon_phase(dt.datetime(2025, 2, 11).date())
    feb_12_phase, feb_12_angle = get_moon_phase(dt.datetime(2025, 2, 12).date())
    assert feb_11_phase != "New Moon", f"Expected not New Moon but got {feb_11_phase} for 2025-02-11"
    assert feb_12_phase == "New Moon", f"Expected New Moon but got {feb_12_phase} for 2025-02-12"

def test_12_apr_2025_should_be_new_moon():
    apr_11_phase, apr_11_angle = get_moon_phase(dt.datetime(2025, 4, 11).date())
    apr_12_phase, apr_12_angle = get_moon_phase(dt.datetime(2025, 4, 12).date())
    assert apr_11_phase != "New Moon", f"Expected not New Moon but got {apr_11_phase} for 2025-04-11"
    assert apr_12_phase == "New Moon", f"Expected New Moon but got {apr_12_phase} for 2025-04-12"

def test_12_may_2025_should_be_new_moon():
    may_11_phase, may_11_angle = get_moon_phase(dt.datetime(2025, 5, 11).date())
    may_12_phase, may_12_angle = get_moon_phase(dt.datetime(2025, 5, 12).date())
    assert may_11_phase != "New Moon", f"Expected not New Moon but got {may_11_phase} for 2025-05-11"
    assert may_12_phase == "New Moon", f"Expected New Moon but got {may_12_phase} for 2025-05-12"

# Tests for 2026 new moons
def test_1_feb_2026_should_be_new_moon():
    jan_31_phase, jan_31_angle = get_moon_phase(dt.datetime(2026, 1, 31).date())
    feb_1_phase, feb_1_angle = get_moon_phase(dt.datetime(2026, 2, 1).date())
    assert jan_31_phase != "New Moon", f"Expected not New Moon but got {jan_31_phase} for 2026-01-31"
    assert feb_1_phase == "New Moon", f"Expected New Moon but got {feb_1_phase} for 2026-02-01"

def test_3_mar_2026_should_be_new_moon():
    mar_2_phase, mar_2_angle = get_moon_phase(dt.datetime(2026, 3, 2).date())
    mar_3_phase, mar_3_angle = get_moon_phase(dt.datetime(2026, 3, 3).date())
    assert mar_2_phase != "New Moon", f"Expected not New Moon but got {mar_2_phase} for 2026-03-02"
    assert mar_3_phase == "New Moon", f"Expected New Moon but got {mar_3_phase} for 2026-03-03"