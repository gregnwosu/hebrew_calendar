from enum import Enum
from typing import Optional, List, Dict
from dataclasses import dataclass
from astropy.time import Time
from astropy.coordinates import get_body
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

# Hebrew year numbers in the 19-year Metonic cycle that are leap years
# Years 3, 6, 8, 11, 14, 17, 19 of each cycle have 13 months
LEAP_YEARS_IN_CYCLE = {3, 6, 8, 11, 14, 17, 19}

def is_hebrew_leap_year(hebrew_year: int) -> bool:
    """Determine if a Hebrew year is a leap year using the 19-year Metonic cycle.

    Leap years have 13 months. In the GMS observational calendar, the leap month
    is added after month 6 (Elul), before Tishrei, to keep Passover in early spring
    while adjusting the fall feasts.
    """
    year_in_cycle = ((hebrew_year - 1) % 19) + 1
    return year_in_cycle in LEAP_YEARS_IN_CYCLE

def needs_leap_month(nisan_1_date: dt.date) -> bool:
    """Determine if a leap month is needed based on the astronomical new moons.

    In the GMS observational system, a leap year is detected when the 7th new moon
    from Nisan falls in late August (Aug 20-31). In this case, the 8th new moon
    (in September) becomes Tishrei, and the 7th moon is a leap month.

    If the 7th moon is in early/mid August (before Aug 20) or in September,
    it becomes Tishrei directly, and there's no leap month.

    This heuristic matches GMS data for 2023-2025.
    """
    start = ensure_datetime(nisan_1_date)
    # Calculate enough time to cover 8 lunar months (~237 days)
    end = start + dt.timedelta(days=250)
    new_moons = enumerate_new_moons(start, end)

    if len(new_moons) < 7:
        return False

    # Check the 7th new moon (index 6)
    nm_7 = new_moons[6]

    # It's a leap year if the 7th moon falls in late August (Aug 20-31)
    # In this case, the 8th moon becomes Tishrei instead
    return nm_7.month == 8 and nm_7.day >= 20

def gregorian_to_hebrew_year(gregorian_date: dt.date) -> int:
    """Approximate the Hebrew year from a Gregorian date.

    Hebrew year 5784 began around Sept 2023 and year 5785 around Sept 2024.
    This is approximate - the Hebrew new year (Rosh Hashanah) falls in Sept/Oct.
    For Nisan-based calculations, we add 1 if before Tishrei.
    """
    # Hebrew year is approximately Gregorian year + 3760
    # But the Hebrew year changes in the fall (Tishrei), not January
    hebrew_year = gregorian_date.year + 3760
    # If we're in the first ~9 months of the Gregorian year,
    # we're still in the Hebrew year that started the previous fall
    if gregorian_date.month < 9:
        pass  # Already correct for spring months
    else:
        hebrew_year += 1
    return hebrew_year
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
    moon = get_body("moon", time_obs)
    sun = get_body("sun", time_obs)
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


def is_new_moon_day(date_obs) -> bool:
    """Determine if this is the new moon day (start of the biblical month).

    The biblical month begins on the evening when the moon enters conjunction
    with the sun (becomes invisible). This is detected when the moon-sun
    separation angle drops below approximately 12 degrees during the waning
    phase (angle decreasing from the previous day).

    This aligns with the observational practice where the new month begins
    when the old crescent can no longer be seen.
    """
    date_obs = ensure_datetime(date_obs)
    # Check at evening time (6pm) when observations would be made
    evening = dt.datetime.combine(date_obs.date(), dt.time(18, 0))
    _, current_angle = get_moon_phase(evening)
    _, prev_angle = get_moon_phase(evening - dt.timedelta(days=1))

    # New moon day is when:
    # 1. The angle is small (near conjunction) - less than ~12°
    # 2. The angle was larger yesterday (we're in waning phase approaching conjunction)
    is_near_conjunction = current_angle <= 12.0
    is_waning = current_angle < prev_angle

    return is_near_conjunction and is_waning

def get_month_lengths_from_new_moons(lunar_year_start: dt.datetime, num_months: int = 13) -> List[int]:
    """Calculate actual month lengths by finding astronomical new moons.

    Returns a list of month lengths (in days) based on the actual
    astronomical new moon dates starting from lunar_year_start.
    """
    lunar_year_start = ensure_datetime(lunar_year_start)
    # Calculate enough time to cover the requested months (max ~390 days for 13 months)
    end_date = lunar_year_start + dt.timedelta(days=num_months * 31)
    new_moons = enumerate_new_moons(lunar_year_start, end_date)

    month_lengths = []
    for i in range(len(new_moons) - 1):
        length = (new_moons[i + 1] - new_moons[i]).days
        month_lengths.append(length)

    return month_lengths

def add_months_and_days(lunar_year_start: dt.datetime, months: int, days: int,
                        is_leap_year: Optional[bool] = None) -> dt.datetime:
    """Return the date ``months`` lunar months and ``days`` days after ``lunar_year_start``.

    This implementation uses astronomical calculations to find actual new moon dates,
    providing accurate month lengths rather than a fixed pattern.

    In the GMS observational system, leap years have 13 months with the extra month
    inserted after month 6 (Elul), before Tishrei. This keeps Passover in early spring
    while pushing the fall feasts later.

    Month mapping in leap years:
    - Months 1-6: Nisan through Elul (same as regular year)
    - Month 7: Leap month (Elul II)
    - Months 8-13: Tishrei through Adar (shifted by 1 from regular year numbering)

    For feast calculations, we use biblical month numbers:
    - Month 7 in biblical terms = Tishrei = new moon #7 (regular) or #8 (leap)
    """
    lunar_year_start = ensure_datetime(lunar_year_start)

    # Determine if this is a leap year based on astronomical observation
    if is_leap_year is None:
        is_leap_year = needs_leap_month(lunar_year_start.date())

    # Get astronomical month lengths
    num_months_needed = 13 if is_leap_year else 12
    months_to_calculate = max(num_months_needed, months) + 2
    month_lengths = get_month_lengths_from_new_moons(lunar_year_start, months_to_calculate)

    # In GMS system, the leap month is after month 6 (before Tishrei)
    # So for months 7+ in a leap year, we need to add 1 to the new moon index
    if is_leap_year and months > 6:
        # Biblical month 7 (Tishrei) = new moon #8 in leap year
        actual_new_moon_index = months  # months is 1-indexed, so month 7 -> index 7 -> 8th new moon
    else:
        actual_new_moon_index = months - 1  # Convert to 0-indexed

    # Calculate days until the target month
    days_until_month = 0
    for i in range(actual_new_moon_index):
        if i < len(month_lengths):
            days_until_month += month_lengths[i]
        else:
            # Fallback to average lunar month if we run out of calculated months
            days_until_month += 29

    nth_new_moon = lunar_year_start + dt.timedelta(days=days_until_month)

    # Days are counted from the new moon day (day 0), so simply add ``days``
    target_date = nth_new_moon + dt.timedelta(days=days)
    return dt.datetime.combine(target_date, dt.datetime.min.time())

@st.cache_data
def enumerate_new_moons(start_date: dt.datetime, end_date: dt.datetime) -> List[dt.date]:
    """Find all new moon days from start_date to end_date.

    Uses the biblical/observational method: the new month begins on the evening
    when the moon enters conjunction (becomes invisible). Days run from evening
    to evening.
    """
    start_date = ensure_datetime(start_date)
    end_date = ensure_datetime(end_date)
    date_cursor = start_date
    result = []

    while date_cursor <= end_date:
        if is_new_moon_day(date_cursor):
            # Found new moon - this is the start of the new month
            result.append(date_cursor.date())
            # Move forward by approximately one lunar cycle to find the next new moon
            date_cursor += dt.timedelta(days=28)
        else:
            # Increment day by day to check the next date
            date_cursor += dt.timedelta(days=1)
    return result

@st.cache_data
def enumerate_sabbaths(new_moon_dates: List[dt.date], end_date: dt.date) -> List[dt.date]:
    """Generate Sabbath dates including the new moons themselves.

    The new moon opens the month and is treated as a Sabbath.  Additional
    Sabbaths occur every seven days thereafter until (but not including)
    the next new moon.  If the next month begins the day after the final
    weekly Sabbath (i.e. a 29‑day month), this naturally results in a
    two‑day Sabbath spanning the month boundary.
    """
    sabbaths: List[dt.date] = []
    for i, nm_date in enumerate(new_moon_dates):
        sabbath_date = nm_date  # The new moon itself is a Sabbath

        if i + 1 < len(new_moon_dates):
            cycle_end_date = new_moon_dates[i + 1]
        else:
            # Include Sabbaths up to the provided end_date for the final month
            cycle_end_date = end_date + dt.timedelta(days=1)

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
    # GMS observational calendar: days run from evening to evening
    # "Day 14 eve" means the feast starts on the evening of that Gregorian date
    # So we include the day before in our day list to capture the evening start

    PASSOVER = FeastDay(
        name='Passover (Pesach)',
        description="Commemorates the Israelites' deliverance from slavery in Egypt. Includes the Feast of Unleavened Bread.",
        lunar_month=1,
        days=[14, 15, 16, 17, 18, 19, 20, 21],  # Day 14 (Passover) through day 21 (end of Unleavened Bread)
        bible_ref='Leviticus 23:5-8'
    )
    FIRSTFRUITS = FeastDay(
        name='Firstfruits (Wave Sheaf)',
        description='The day after the Sabbath during Unleavened Bread when the firstfruits of barley are offered.',
        lunar_month=1,
        days=[16],  # Day 16 of Nisan
        bible_ref='Leviticus 23:10-14'
    )
    FEAST_OF_WEEKS = FeastDay(
        name='Feast of Weeks (Shavuot)',
        description='Celebrated fifty days after Firstfruits (counting from Nisan 16). Also known as Pentecost.',
        lunar_month=3,
        days=[6],  # Day 6 of Sivan
        bible_ref='Leviticus 23:15-21'
    )
    FEAST_OF_TRUMPETS = FeastDay(
        name='Feast of Trumpets (Rosh Hashanah)',
        description="New Year's festival marked by the blowing of trumpets. Coincides with the new moon.",
        lunar_month=7,
        days=[0, 1],  # Day 0 (new moon) and day 1 - evening to evening spans both Gregorian dates
        bible_ref='Leviticus 23:23-25'
    )
    DAY_OF_ATONEMENT = FeastDay(
        name='Day of Atonement (Yom Kippur)',
        description='A day of fasting and repentance.',
        lunar_month=7,
        days=[9, 10],  # Day 9 eve to day 10 eve
        bible_ref='Leviticus 23:26-32'
    )
    FEAST_OF_TABERNACLES = FeastDay(
        name='Feast of Tabernacles (Sukkot)',
        description="An eight-day festival commemorating the Israelites' forty years of wandering in the desert. Includes Shemini Atzeret.",
        lunar_month=7,
        days=[14, 15, 16, 17, 18, 19, 20, 21, 22],  # Day 14 eve to day 22 eve (7 days + Shemini Atzeret)
        bible_ref='Leviticus 23:33-36, 39-43'
    )
    # Note: In leap years, Purim is celebrated in Adar II (month 13), not Adar I (month 12)
    # The find_feast_days method handles this adjustment
    PURIM = FeastDay(
        name='Purim',
        description="Commemorates the deliverance of the Jewish people from Haman's plot. In leap years, celebrated in Adar II.",
        lunar_month=12,  # Will be adjusted to 13 in leap years by find_feast_days
        days=[13, 14, 15],  # Day 13 eve to day 15 eve
        bible_ref='Esther 9:20-32'
    )
    FEAST_OF_DEDICATION = FeastDay(
        name='Hanukkah (Feast of Dedication)',
        description='Commemorates the Maccabean revolt and rededication of the Second Temple.',
        lunar_month=9,  # Kislev (9th month from Nisan)
        days=[24, 25, 26, 27, 28, 29, 30],  # 24 Kislev eve starts Hanukkah, through 30 Kislev, then continues into Tevet
        bible_ref='John 10:22'
    )
    # Hanukkah continues into Tevet (month 10) for the final 2 days
    FEAST_OF_DEDICATION_END = FeastDay(
        name='Hanukkah (Feast of Dedication)',
        description='Commemorates the Maccabean revolt and rededication of the Second Temple.',
        lunar_month=10,  # Tevet (10th month from Nisan)
        days=[1, 2],  # 1-2 Tevet (last 2 days of 8-day festival)
        bible_ref='John 10:22'
    )

    @staticmethod
    @st.cache_data
    def find_feast_days(year_start: dt.datetime, year_end: dt.datetime) -> Dict[dt.date, FeastDay]:
        result = {}
        year_start = ensure_datetime(year_start)
        # Use GMS observational method for leap year detection
        is_leap = needs_leap_month(year_start.date())

        for fd in FeastDays:
            lunar_month = fd.value.lunar_month

            # In leap years, Purim moves from month 12 (Adar I) to month 13 (Adar II)
            if fd == FeastDays.PURIM and is_leap:
                lunar_month = 13

            for day in fd.value.days:
                feast_date = add_months_and_days(year_start, lunar_month, day, is_leap_year=is_leap)
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

    # Start date for the Hebrew year (Nisan 1)
    # GMS Nisan 1 dates: 2023: Feb 19, 2024: Mar 9, 2025: Feb 27
    start_of_lunar_year = st.date_input("Select Start of Hebrew Year (Nisan 1)", dt.date(2025, 2, 27))
    start_of_lunar_year = ensure_datetime(start_of_lunar_year)

    # Determine if this is a leap year
    hebrew_year = gregorian_to_hebrew_year(start_of_lunar_year.date())
    is_leap = is_hebrew_leap_year(hebrew_year)

    # Calculate end date based on whether it's a leap year
    # Regular year: ~354 days (12 months), Leap year: ~384 days (13 months)
    year_length = 384 if is_leap else 354
    end_of_lunar_year = start_of_lunar_year + dt.timedelta(days=year_length)

    leap_status = "Leap Year (13 months)" if is_leap else "Regular Year (12 months)"
    st.info(f"Hebrew Year {hebrew_year} - {leap_status}")

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

    # Display information for the clicked date in sidebar for visibility
    if st.session_state[clicked_date_key]:
        clicked_date = st.session_state[clicked_date_key]
        with st.sidebar:
            st.subheader(f"Information for {clicked_date.strftime('%B %d, %Y')}")
            if clicked_date in feast_dates:
                feast = feast_dates[clicked_date]
                st.write(f"**Feast Day:** {feast.name}")
                st.write(f"**Reference:** {feast.bible_ref}")
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
            # Add clear button to reset selection
            if st.button("Clear Selection"):
                st.session_state[clicked_date_key] = None
                st.rerun()

if __name__ == '__main__':
    main()



    