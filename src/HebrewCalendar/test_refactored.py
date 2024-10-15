# test add_months_and_days for 7 lunar months and 15th days with start date 2024-03-09 assert we have september 16 2024
from HebrewCalendar.refactored import add_months_and_days, get_moon_phase
import datetime as dt
import pytest
#https://www.youtube.com/@gmsnewmoonshighholydays5488

# def test_feast_of_tabernacles():
#     assert dt.datetime(2024, 9, 16) == add_months_and_days(dt.datetime(2024, 3, 9), 7, 15)
#     # this fails as it returns  dt.datetime(2024, 11, 17, 0, 0)
    
# def test_feast_of_trumpets():
#     assert dt.datetime(2024, 7, 29) == add_months_and_days(dt.datetime(2024, 3, 9), 6, 1)
#     # this fails as it returns  dt.datetime(2024, 10, 26, 0, 0)
    
# def test_day_of_atonement():
#     assert dt.datetime(2024, 9, 11) == add_months_and_days(dt.datetime(2024, 3, 9), 7, 1)
#     # this fails as it returns  dt.datetime(2024, 11, 6, 0, 0)
    
def test_passover():
    assert dt.datetime(2024, 3, 23) == add_months_and_days(dt.datetime(2024, 3, 9), 1, 14)
    # this fails as it returns  dt.datetime(2024, 11, 1, 0, 0)
    
    
def test_get_phase_for_lunar_new_year_whichis_march_9_2024():
    march_9_phase, march_9_angle = get_moon_phase(dt.datetime(2024, 3, 9).date())
    assert march_9_phase == "New Moon", f"Expected New Moon but got {march_9_phase} for {dt.datetime(2024, 3, 9).date()} angle is {march_9_angle} "
    
# def test_5_june_2024_should_be_new_moon():
#     june_5_phase, june_5_angle = get_moon_phase(dt.datetime(2024, 6, 5).date())
#     june_6_phase, june_6_angle = get_moon_phase(dt.datetime(2024, 6, 6).date())
#     assert june_5_phase == "New Moon" , f"Expected  equal to New Moon but got {june_5_phase} for {dt.datetime(2024, 6, 5).date()} angle is {june_5_angle} should  be new moon but {june_6_angle } should be not be new moon"
#     assert june_6_phase != "New Moon" , f"Expected not New Moon but got {june_6_phase} for {dt.datetime(2024, 6, 6).date()} angle is {june_6_angle} should not be new moon but {june_5_angle } should be  be new moon"
    
    
# def test_2_oct_2024_should_be_new_moon():
#     oct_1_phase, oct_1_angle = get_moon_phase(dt.datetime(2024, 10, 1).date())
#     oct_2_phase, oct_2_angle = get_moon_phase(dt.datetime(2024, 10, 2).date())
#     assert oct_1_phase != "New Moon" , f"Expected not equal to New Moon but got {oct_1_phase} for {dt.datetime(2024, 10, 1).date()} angle is {oct_1_angle} shouuld not be new moon but {oct_2_angle } should be new moon"
#     assert oct_2_phase == "New Moon" , f"Expected New Moon but got {oct_2_phase} for {dt.datetime(2024, 10, 2).date()} angle is {oct_2_angle} "
    
# def test_7_may_should_be_new_moon():
#     may_6_phase, may_6_angle = get_moon_phase(dt.datetime(2024, 5, 6).date())
#     may_7_phase, may_7_angle = get_moon_phase(dt.datetime(2024, 5, 7).date())
#     assert may_6_phase != "New Moon" , f"Expected not equal to New Moon but got {may_6_phase} for {dt.datetime(2024, 5, 6).date()} angle is {may_6_angle} shouuld not be new moon but {may_7_angle } should be new moon"
#     assert may_7_phase == "New Moon" , f"Expected New Moon but got {may_7_phase} for {dt.datetime(2024, 5, 7).date()} angle is {may_7_angle} should be new moon but {may_6_angle } should not be new moon"