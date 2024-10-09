from enum import Enum
from typing import Optional, List, Dict
from dataclasses import dataclass
from astropy.time import Time
from astropy.coordinates import get_moon, get_sun
import datetime as dt
import pandas as pd
import calendar
import streamlit as st
from zoneinfo import ZoneInfo  # For Python 3.9+
import numpy as np

def ensure_datetime(date_obj):
    """Ensure the input is a datetime.datetime object."""
    if isinstance(date_obj, dt.datetime):
        return date_obj
    elif isinstance(date_obj, dt.date):
        return dt.datetime.combine(date_obj, dt.datetime.min.time())
    else:
        raise ValueError("Input must be a date or datetime object.")
@st.cache_data
def get_nth_new_moon_date(new_moon_dates: List[dt.date], n: int) -> dt.date:
    """Returns the date of the nth new moon starting from the start date."""
    if n <= len(new_moon_dates):
        return new_moon_dates[n - 1]
    else:
        raise ValueError("Not enough new moon dates calculated.")
@st.cache_data
def get_moon_phase(date_obs): 
    date_obs = ensure_datetime(date_obs)
    # Convert the date and time to a Time object
    time_obs = Time(date_obs)
    # Calculate the position of the moon and sun at the observation time
    moon = get_moon(time_obs)
    sun = get_sun(time_obs)
    # Calculate the phase angle between the moon and sun 
    phase_angle = moon.separation(sun).degree

    # Convert the phase angle to a moon phase
    if phase_angle <= 10.0:
        phase = 'New Moon'
    elif phase_angle < 60.0:
        phase = 'Waxing Crescent'
    elif phase_angle < 110.0:
        phase = 'First Quarter'
    elif phase_angle < 160.0:
        phase = 'Waxing Gibbous'
    elif phase_angle < 210.0:
        phase = 'Full Moon'
    elif phase_angle < 260.0:
        phase = 'Waning Gibbous'
    elif phase_angle < 310.0:
        phase = 'Third Quarter'
    else:
        phase = 'Waning Crescent'

    return phase, phase_angle

def add_months_and_days(lunar_year_start: dt.datetime, months: int, days: int) -> dt.datetime:
    """
    Returns a datetime that is the given number of lunar months (months) 
    and additional days away from the start date.
    """
    # Ensure the start date is a datetime object
    lunar_year_start = ensure_datetime(lunar_year_start)
    # Estimate an end date far enough to include the desired new moons
    end_date = lunar_year_start + dt.timedelta(days=months * 30 + days)
    # Generate new moon dates
    new_moon_dates = enumerate_new_moons(lunar_year_start, end_date)
    
    try:
        # Get the nth new moon date
        nth_new_moon_date = get_nth_new_moon_date(new_moon_dates, months)
        # Add the specified number of days
        target_date = nth_new_moon_date + dt.timedelta(days=days - 1)
        return dt.datetime.combine(target_date, dt.datetime.min.time())
    except ValueError:
        raise ValueError("Not enough new moon dates calculated.")

@st.cache_data
def enumerate_new_moons(start_date: dt.datetime, end_date: dt.datetime) -> List[dt.date]:
    """Find all new moons from start_date to end_date."""
    start_date = ensure_datetime(start_date)
    end_date = ensure_datetime(end_date)
    date_cursor = start_date
    result = []

    while date_cursor <= end_date:
        phase, _ = get_moon_phase(date_cursor)
        if phase == 'New Moon':
            # Found a new moon
            result.append(date_cursor.date())
            # Move forward by approximately one lunar cycle to find the next new moon
            date_cursor += dt.timedelta(days=29)
        else:
            # Increment day by day to check the next date
            date_cursor += dt.timedelta(days=1)
    return result

@st.cache_data
def enumerate_sabbaths(new_moon_dates: List[dt.date], end_date: dt.date) -> List[dt.date]:
    """Generate Sabbath dates: Every 7 days after a new moon until the next new moon."""
    sabbaths = []
    for i in range(len(new_moon_dates)):
        nm_date = new_moon_dates[i]
        # Start from 7 days after new moon
        sabbath_date = nm_date + dt.timedelta(days=7)
        # Determine end date for this cycle
        if i + 1 < len(new_moon_dates):
            next_nm_date = new_moon_dates[i + 1]
            cycle_end_date = next_nm_date
        else:
            cycle_end_date = end_date + dt.timedelta(days=1)  # Include end_date
        # Generate Sabbaths until the next new moon
        while sabbath_date < cycle_end_date:
            sabbaths.append(sabbath_date)
            sabbath_date += dt.timedelta(days=7)
    return sabbaths

@dataclass
class Position:
    latitude: float
    longitude: float
    timezone: str  # Add timezone attribute

@dataclass(frozen=True)
class FeastDay:
    lunar_month: int
    days: List[int]
    name: str
    description: Optional[str]  = None
    bible_ref: Optional[str] = None
    link: Optional[str] = None

class FeastDays(Enum):
    PASSOVER = FeastDay(
        name='Passover (Pesach)',
        description="Commemorates the Israelites' deliverance from slavery in Egypt.",
        lunar_month=1,
        days=[14],
        bible_ref='Leviticus 23:5'
    )
    UNLEAVENED_BREAD = FeastDay(
        name='Feast of Unleavened Bread',
        description='A festival lasting seven days during which unleavened bread is eaten.',
        lunar_month=1,
        days=[15,16,17,18,19,20,21],
        bible_ref='Leviticus 23:6-8'
    )
    FEAST_OF_WEEKS = FeastDay(
        name='Feast of Weeks (Shavuot)',
        description='Celebrated fifty days after the Firstfruits. Also known as Pentecost.',
        lunar_month=1,
        days=[50],
        bible_ref='Leviticus 23:15-21'
    )
    FEAST_OF_TRUMPETS = FeastDay(
        name='Feast of Trumpets (Rosh Hashanah)',
        description="New Year's festival marked by the blowing of trumpets.",
        lunar_month=7,
        days=[1],
        bible_ref='Leviticus 23:23-25'
    )
    DAY_OF_ATONEMENT = FeastDay(
        name='Day of Atonement (Yom Kippur)',
        description='A day of fasting and repentance.',
        lunar_month=7,
        days=[10],
        bible_ref='Leviticus 23:26-32'
    )
    FEAST_OF_TABERNACLES = FeastDay(
        name='Feast of Tabernacles (Sukkot)',
        description="A seven-day festival commemorating the Israelites' forty years of wandering in the desert.",
        lunar_month=7,
        days=[15,16,17,18,19,20,21],
        bible_ref='Leviticus 23:33-36, 39-43'
    )
    PURIM = FeastDay(
        name='Purim',
        description="Commemorates the deliverance of the Jewish people from Haman's plot.",
        lunar_month=12,
        days=[14,15],
        bible_ref='Esther 9:20-32'
    )
    FEAST_OF_DEDICATION = FeastDay(
        name='Hanukkah (Feast of Dedication)',
        description='Commemorates the Maccabean revolt and rededication of the Second Temple.',
        lunar_month=8,
        days=[25,26,27,28,29,30,31,32],
        bible_ref='John 10:22'
    )

    @staticmethod
    @st.cache_data
    def find_feast_days(year_start: dt.datetime, year_end: dt.datetime) -> Dict[dt.date, FeastDay]:
        result = {}
        for fd in FeastDays:
            for day in fd.value.days:
                feast_date = add_months_and_days(year_start, fd.value.lunar_month, day)
                if feast_date.date() <= year_end.date():
                    result[feast_date.date()] = fd.value
        return result

def create_calendar(year, month, feast_dates, sabbath_dates, new_moon_dates, clicked_date_key):
    # Create a list to store buttons
    cal = calendar.monthcalendar(year, month)
    days_of_week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    st.write(f"### {calendar.month_name[month]} {year}")
    # Display the days of the week
    cols = st.columns(7)
    for i, day_name in enumerate(days_of_week):
        cols[i].write(f"**{day_name}**")
    # Iterate over each week
    for week in cal:
        cols = st.columns(7)
        for i, day in enumerate(week):
            if day == 0:
                cols[i].write("")
            else:
                current_date = dt.date(year, month, day)
                cell_text = str(day)
                # Indicate feast days, Sabbaths, and New Moons
                emojis = ''
                if current_date in feast_dates:
                    emojis += " 🎉"
                if current_date in sabbath_dates:
                    emojis += " ✨"
                if current_date in new_moon_dates:
                    emojis += " 🌑"
                cell_text += emojis
                # Create a unique key for each button
                button_key = f"{current_date}-{i}"
                if cols[i].button(cell_text, key=button_key):
                    st.session_state[clicked_date_key] = current_date

def main():
    st.title("Hebrew Year Calendar with Feast Days, Sabbaths, and New Moons")

    # Example start date for the Hebrew year
    start_of_lunar_year = st.date_input("Select Start of Hebrew Year", dt.date(2024, 9, 23))
    start_of_lunar_year = ensure_datetime(start_of_lunar_year)

    # Calculate end date (approximately one lunar year later)
    end_of_lunar_year = start_of_lunar_year + dt.timedelta(days=354)  # Lunar year is approximately 354 days

    # Generate data for the calendar (cached)
    feast_dates = FeastDays.find_feast_days(start_of_lunar_year, end_of_lunar_year)
    new_moon_dates = enumerate_new_moons(start_of_lunar_year, end_of_lunar_year)
    sabbath_dates = enumerate_sabbaths(new_moon_dates, end_of_lunar_year.date())

    # Create a date range for the entire Hebrew year
    date_range = pd.date_range(start=start_of_lunar_year, end=end_of_lunar_year)

    # Group dates by month and year
    dates_by_month_year = {}
    for single_date in date_range:
        year_month = (single_date.year, single_date.month)
        if year_month not in dates_by_month_year:
            dates_by_month_year[year_month] = []
        dates_by_month_year[year_month].append(single_date)

    # Key to track clicked date in session state
    clicked_date_key = 'clicked_date'
    if clicked_date_key not in st.session_state:
        st.session_state[clicked_date_key] = None

    # Display the calendar for each month in the Hebrew year
    for (year, month), dates in dates_by_month_year.items():
        create_calendar(year, month, feast_dates, sabbath_dates, new_moon_dates, clicked_date_key)

    # Display information for the clicked date
    if st.session_state[clicked_date_key]:
        clicked_date = st.session_state[clicked_date_key]
        st.subheader(f"Information for {clicked_date.strftime('%B %d, %Y')}")
        if clicked_date in feast_dates:
            feast = feast_dates[clicked_date]
            st.write(f"**Feast Day:** {feast.name} ({feast.bible_ref})")
            st.write(f"{feast.description}")
        if clicked_date in sabbath_dates:
            st.write("**Sabbath Day**")
        if clicked_date in new_moon_dates:
            st.write("**New Moon Day**")
        if clicked_date not in feast_dates and clicked_date not in sabbath_dates and clicked_date not in new_moon_dates:
            st.write("This is a regular day.")
        # Display moon phase
        phase, angle = get_moon_phase(clicked_date)
        st.write(f"**Moon Phase:** {phase} (Phase angle: {angle:.2f}°)")
        # Reset clicked date after displaying information
        st.session_state[clicked_date_key] = None

if __name__ == '__main__':
    main()



    