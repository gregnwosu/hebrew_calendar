import pytest
import datetime as dt
from HebrewCalendar.moon import get_moon_phase, calculate_sunset, Location, enumerate_sabbaths, enumerate_new_moons, add_months_and_days

# @pytest.mark.skip(reason="not implemented")
@pytest.mark.parametrize("date_obs, expected_moon_phase",[
                        (dt.datetime(2025, 2, 24, 21, 0,0), 'New Moon'), #Yom Kippur
                        (dt.datetime(2023, 8, 15, 21, 0,0), 'New Moon'),
                        (dt.datetime(2023, 7, 17, 21, 0,0), 'New Moon'),
                        (dt.datetime(2023, 5, 18, 21, 0,0), 'New Moon'),
                    #(dt.datetime(2023, 5, 3, 21, 0,0),  'New Moon'),   #passover aha passover is not on a new moon
                        (dt.datetime(2022, 11, 23, 21, 0,0),'New Moon'), 
                    #(dt.datetime(2022, 9, 4, 21, 0,0),  'New Moon'),   #atonement
                        (dt.datetime(2022, 8, 26, 21, 0,0), 'New Moon'),  #blowing of trumpets
                        (dt.datetime(2020, 8, 18, 21, 0,0), 'New Moon'),  #blowing of trumpets
                        (dt.datetime(2022, 7, 28, 21, 0,0), 'New Moon'),  
                        (dt.datetime(2019, 1, 5, 21, 0,0),  'New Moon'),  
                        (dt.datetime(2023, 2, 19, 21, 0,0), 'New Moon'),  
                        (dt.datetime(2021, 12, 3, 21, 0,0), 'New Moon'),  
                        (dt.datetime(2022, 6, 28, 21, 0,0), 'New Moon')])

def test_new_moon(date_obs, expected_moon_phase):
    """Test the get_moon_phase function."""
    #date_obs_at_sunset = calculate_sunset(date_obs, location=Location.NEW_YORK)
    actual_moon_phase, phase_angle = get_moon_phase(date_obs)
    assert actual_moon_phase == expected_moon_phase, f"Expected {expected_moon_phase} but got {actual_moon_phase} for {date_obs} angle is {phase_angle} "
    actual_moon_phase, phase_angle = get_moon_phase(date_obs + dt.timedelta(days=1)) 
    # assert actual_moon_phase != expected_moon_phase , f"Expected not equal to {expected_moon_phase} but got {actual_moon_phase} for {date_obs + dt.timedelta(days=1)} angle is {phase_angle} "
    # actual_moon_phase, phase_angle = get_moon_phase(date_obs - dt.timedelta(days=1)) 
    # assert actual_moon_phase != expected_moon_phase , f"Expected not equal to {expected_moon_phase} but got {actual_moon_phase} for {date_obs - dt.timedelta(days=1)} angle is {phase_angle} "

def test_enumerate_new_moons():
    start_date =dt.datetime(2023, 5, 15, 21, 21,0)
    end_date = dt.datetime(2023, 8, 15, 21, 21,0)
    new_moons = enumerate_new_moons(start_date, end_date)
    print(f"new moons are {new_moons}")
    assert len(new_moons) == 4, f"Expected 4 new moons but got {len(new_moons)}"
    
def test_enumerate_sabbats():
    start_date =dt.datetime(2023, 5, 15, 21, 21,0)
    end_date =  dt.datetime(2023, 6, 17, 21, 21)
    sabbaths = enumerate_sabbaths(start_date, end_date)
    print(f"sabbaths are {sabbaths}")
    assert len(sabbaths) == 12, f"Expected 12 sabbaths but got {len(sabbaths)}"