#Output
#To calculate the phase of the moon at a given date, we need to know the date and time of the observation. We can use the Python library `Astropy` to calculate the phase of the moon. Here is an example program that calculates the phase of the moon for a given date and time:

from enum import Enum
from typing import Optional, List, Dict
from dataclasses import dataclass
from functools import reduce
import numpy as np
from astropy.time import Time
from astropy.coordinates import get_body, get_sun, GeocentricTrueEcliptic
import datetime as dt

def get_moon_phase(date_obs):
    # Convert the date and time to an astropy Time object
    time_obs = Time(date_obs.strftime('%Y-%m-%d %H:%M:%S'))

    # Calculate the position of the moon and sun at the observation time
    moon = get_body("moon", time_obs)
    sun = get_body("sun", time_obs)
    # Calculate the phase angle between the moon and sun
    phase_angle =  moon.separation(sun).degree

    # Convert the phase angle to a moon phase
    # Using 12 degrees threshold to better match traditional calendar observations
    if phase_angle <= 12.0:
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

# This updated function should now detect the start of a new moon phase on only one day.


@dataclass
class Position:
    latitude: float
    longitude: float

@dataclass(frozen=True)
class FeastDay:
    lunar_month: int
    days: List[int]
    name: str
    description: Optional[str]  = None
    bible_refs: Optional[List[str]] = None
    link: Optional[str] = None

class FeastDays(Enum):
    # SABBATH = FeastDay(name='Sabbath', description='A day of rest observed every seventh day.', lunar_month=1, days ='Every seventh day', bible_ref='Leviticus 23:3')
    PASSOVER = FeastDay(name='Passover (Pesach)', description="Commemorates the Israelites' deliverance from slavery in Egypt.", lunar_month=1, days=[14], bible_refs=['Leviticus 23:5', 'Exodus 12:1-14'])
    UNLEAVENED_BREAD = FeastDay(name='Feast of Unleavened Bread', description='A festival lasting seven days during which unleavened bread is eaten.', lunar_month=1, days=[15,16,17,18,19,20,21], bible_refs=['Leviticus 23:6-8', 'Exodus 12:15-20'])
    #FIRST_FRUITS = FeastDay(name='Firstfruits', description='An offering of the first fruits of the harvest.', lunar_month=1, days='Day after the Sabbath during the Feast of Unleavened Bread', bible_refs=['Leviticus 23:9-14'])
    FEAST_OF_WEEKS = FeastDay(name='Feast of Weeks (Shavuot)', description='Celebrated fifty days after the Firstfruits. Also known as Pentecost.', lunar_month=1, days=[50], bible_refs=['Leviticus 23:15-21', 'Acts 2:1-4'])
    FEAST_OF_TRUMPETS = FeastDay(name='Feast of Trumpets (Rosh Hashanah)', description="New Year's festival marked by the blowing of trumpets.", lunar_month=7, days=[1], bible_refs=['Leviticus 23:23-25', 'Psalm 81:3'])
    DAY_OF_ATONEMENT = FeastDay(name='Day of Atonement (Yom Kippur)', description='A day of fasting and repentance.', lunar_month=7, days=[10], bible_refs=['Leviticus 23:26-32', 'Leviticus 16:29-34'])
    FEAST_OF_TABERNACLES = FeastDay(name='Feast of Tabernacles (Sukkot)', description="A seven-day festival plus the 8th day assembly (Shemini Atzeret).", lunar_month=7, days=[15,16,17,18,19,20,21,22], bible_refs=['Leviticus 23:33-43', 'Zechariah 14:16-19', 'John 7:37-38', '2 Maccabees 10:6-8'])
    PURIM = FeastDay(name='Purim', description="Commemorates the deliverance of the Jewish people from Haman's plot.", lunar_month=12, days=[14,15], bible_refs=['Esther 9:20-32', '2 Maccabees 15:36'])
    FEAST_OF_DEDICATION = FeastDay(name='Hanukkah (Feast of Dedication)', description='Commemorates the Maccabean revolt and rededication of the Second Temple.', lunar_month=9, days=[25,26,27,28,29,30,31,32], bible_refs=['John 10:22-23', '1 Maccabees 4:36-59', '2 Maccabees 1:18'])

    @staticmethod
    def find_feast_days(year_start: dt.datetime, new_moons: List[dt.datetime] = None) -> Dict[dt.date, FeastDay]:
        """Calculate feast days for a lunar year.

        Args:
            year_start: The date of Nisan 1 (first month new moon)
            new_moons: Optional precomputed list of new moon dates. If not provided,
                       falls back to calculating moons on-the-fly (less accurate).
        """
        if new_moons is not None:
            return FeastDays._find_feast_days_from_moons(year_start, new_moons)
        # Fallback to old method
        result = {add_months_and_days(lunar_year_start=year_start, months=fd.value.lunar_month, days=d):fd.value for fd in FeastDays for d in fd.value.days}
        return result

    @staticmethod
    def _find_feast_days_from_moons(nisan_new_moon: dt.datetime, new_moons: List[dt.datetime]) -> Dict[dt.date, FeastDay]:
        """Calculate feast days using precomputed new moon dates.

        Handles leap years: In a leap year, there's an extra month between Elul (month 6)
        and Tishri (month 7). This is detected by checking whether using 7 months from Nisan
        would place Tishri significantly closer to the autumn equinox while still before it.
        """
        sorted_moons = sorted(new_moons)

        # Find the index of Nisan in the sorted moon list
        nisan_idx = None
        for i, m in enumerate(sorted_moons):
            if m.date() == nisan_new_moon.date():
                nisan_idx = i
                break

        if nisan_idx is None:
            # Fallback: find closest moon
            for i, m in enumerate(sorted_moons):
                if abs((m - nisan_new_moon).days) <= 1:
                    nisan_idx = i
                    break

        if nisan_idx is None:
            return {}

        # Determine if this is a leap year
        # Compare where Tishri would fall with 6 months vs 7 months from Nisan
        nisan_year = nisan_new_moon.year
        autumn_eq = get_autumn_equinox(nisan_year)

        # Calculate Tishri candidates (6 and 7 months from Nisan)
        tishri_6_idx = nisan_idx + 6
        tishri_7_idx = nisan_idx + 7

        leap_offset = 0
        if tishri_6_idx < len(sorted_moons) and tishri_7_idx < len(sorted_moons):
            tishri_6 = sorted_moons[tishri_6_idx].date()
            tishri_7 = sorted_moons[tishri_7_idx].date()

            days_6_before_eq = (autumn_eq - tishri_6).days
            days_7_before_eq = (autumn_eq - tishri_7).days

            # Use leap year (7 months) if:
            # 1. The 7-month Tishri is still before or at the equinox (not after)
            # 2. The 7-month Tishri is within 5 days of the equinox (very close)
            # This matches the observational pattern where leap months are added
            # to keep Tishri close to the autumn equinox
            if days_7_before_eq >= 0 and days_7_before_eq <= 5:
                leap_offset = 1

        result = {}
        for fd in FeastDays:
            # Month index: Nisan is month 1, so month N is at nisan_idx + (N-1)
            # For months 7+, add leap_offset if it's a leap year
            month_num = fd.value.lunar_month
            if month_num >= 7:
                month_idx = nisan_idx + month_num - 1 + leap_offset
            else:
                month_idx = nisan_idx + month_num - 1

            if month_idx < len(sorted_moons):
                month_start = sorted_moons[month_idx]
                for day in fd.value.days:
                    # For Nisan (month 1): the new moon appears at night, so the
                    # first DAY of the month is the next day. "The fourteenth day
                    # of the first month" = new_moon + 14. Use 'day' offset.
                    # For other months: day 1 is the new moon itself (e.g. Trumpets
                    # on Tishri 1 = new moon day). Use 'day - 1' offset.
                    if month_num == 1:
                        feast_date = month_start + dt.timedelta(days=day)
                    else:
                        feast_date = month_start + dt.timedelta(days=day - 1)
                    result[feast_date] = fd.value
        return result



class Location(Enum):
    NEW_YORK = Position(40.7128, -74.0060)
    LONDON = Position(51.5072, -0.1276)
    SYDNEY = Position(-33.8688, 151.2093)
    TOKYO = Position(35.6762, 139.6503)
    JERUSALEM = Position(31.7683, 35.2137)


def calculate_sunset(date_obs: dt.datetime, location: Location):
    import pvlib

    # Define the location (New York City in this example)
    latitude, longitude = (location.value.latitude, location.value.longitude)

    # Calculate sunset time
    solar_position = pvlib.solarposition.get_solarposition(date_obs, latitude, longitude)
    sunset_time = pvlib.solarposition.sun_rise_set_transit_spa(date_obs, latitude, longitude)['sunset']

    print(sunset_time)
    return sunset_time



def add_months_and_days(lunar_year_start: dt.datetime, months: int, days: int) -> dt.date:

    """Returns a date that is the given number of new moons (months)
    and additional days away from the start date."""

    date_cursor = lunar_year_start
    lunar_months_counted = 0
    yesterday_phase, _ = get_moon_phase(_at_noon(date_cursor - dt.timedelta(days=1)))

    # Count the number of new moons for the given months
    while lunar_months_counted < months-1:
        current_phase, _ = get_moon_phase(_at_noon(date_cursor))

        if current_phase == 'New Moon' and yesterday_phase != 'New Moon':
            lunar_months_counted += 1
            if lunar_months_counted < months-1:
                date_cursor += dt.timedelta(days=28)

        yesterday_phase = current_phase
        date_cursor += dt.timedelta(days=1)

    # Add the remaining days
    return date_cursor + dt.timedelta(days=days)


def _at_noon(d: dt.datetime) -> dt.datetime:
    """Return the same date at noon UTC, matching the time used for emoji display."""
    return d.replace(hour=12, minute=0, second=0, microsecond=0)


def get_vernal_equinox(year: int) -> dt.date:
    """Return the date of the vernal equinox for a given year.

    Finds the first day (at noon UTC) when the sun's declination is >= 0,
    searching from March 18 onward.
    """
    for day in range(18, 25):
        d = dt.datetime(year, 3, day, 12, 0, 0)
        t = Time(d.strftime('%Y-%m-%d %H:%M:%S'))
        sun = get_sun(t)
        if sun.dec.degree >= 0:
            return d.date()
    return dt.date(year, 3, 20)  # fallback


def get_autumn_equinox(year: int) -> dt.date:
    """Return the date of the autumn equinox for a given year.

    Finds the first day (at noon UTC) when the sun's declination goes below 0,
    searching from September 20 onward.
    """
    for day in range(20, 27):
        d = dt.datetime(year, 9, day, 12, 0, 0)
        t = Time(d.strftime('%Y-%m-%d %H:%M:%S'))
        sun = get_sun(t)
        if sun.dec.degree <= 0:
            return d.date()
    return dt.date(year, 9, 22)  # fallback


def get_lunar_year_starts(new_moons: Dict[dt.datetime, float],
                          start_year: int, end_year: int) -> Dict[int, dt.datetime]:
    """For each year, find Nisan 1 based on Passover timing relative to vernal equinox.

    The Hebrew year begins at Nisan 1, and Passover (Nisan 14) should fall in spring,
    close to the vernal equinox. This implementation matches observational/astronomical
    Hebrew calendars like GMS that prefer Passover in early spring.

    The rule: Use the earlier new moon (placing Passover before equinox) unless it would
    put Passover more than ~20 days before the equinox. This keeps Passover in the
    appropriate spring season while avoiding pushing it too late into April.
    """
    year_starts = {}
    sorted_moons = sorted(new_moons.keys())

    for y in range(start_year, end_year + 1):
        vernal_eq = get_vernal_equinox(y)

        # Find the two new moons that bracket the vernal equinox
        candidate_before = None
        candidate_after = None

        for m in sorted_moons:
            if m.date() < vernal_eq:
                candidate_before = m
            elif candidate_after is None:
                candidate_after = m
                break

        if candidate_before is None:
            continue

        # Calculate when Passover (Nisan 14) would fall for each candidate
        passover_before = candidate_before + dt.timedelta(days=13)
        passover_after = candidate_after + dt.timedelta(days=13) if candidate_after else None

        # Days before equinox for the earlier candidate's Passover
        days_before_eq = (vernal_eq - passover_before.date()).days

        # Prefer the earlier new moon unless Passover would be more than 20 days
        # before the equinox (which would make it too early in the season)
        if days_before_eq <= 20:
            year_starts[y] = candidate_before
        elif candidate_after:
            year_starts[y] = candidate_after
        else:
            year_starts[y] = candidate_before

    return year_starts


# Days run evening to evening, reckoned at Jerusalem, and the evening is taken
# as nightfall (sun 12° below the horizon) rather than sunset. Both fit the
# 2022-2026 reference list, but sunset would put the October 2026 conjunction
# (15:50 UTC, 37 minutes after Jerusalem sunset) on the 10th instead of the 9th.
DAY_START_LOCATION = Location.JERUSALEM
DAY_START_SUN_ALTITUDE = -12.0


def _elongation(jd):
    """Moon's ecliptic longitude minus the sun's in degrees, wrapped to [-180, 180)."""
    t = Time(jd, format='jd')
    frame = GeocentricTrueEcliptic(equinox=t)
    moon_lon = get_body("moon", t).transform_to(frame).lon.degree
    sun_lon = get_sun(t).transform_to(frame).lon.degree
    return (moon_lon - sun_lon + 180.0) % 360.0 - 180.0


def _sun_altitude(jd, position: Position):
    """Sun's altitude in degrees at a position, without refraction.

    Treats UTC as UT1 (under a second apart) so no earth-orientation data has
    to be downloaded; agrees with astropy's AltAz transform to about 0.005°.
    """
    t = Time(jd, format='jd')
    days = np.asarray(jd) - 2451545.0  # days since J2000
    sun_lon = get_sun(t).transform_to(GeocentricTrueEcliptic(equinox=t)).lon.radian
    obliquity = np.radians(23.4393 - 3.563e-7 * days)
    dec = np.arcsin(np.sin(obliquity) * np.sin(sun_lon))
    ra = np.arctan2(np.cos(obliquity) * np.sin(sun_lon), np.cos(sun_lon))
    hour_angle = np.radians(280.46061837 + 360.98564736629 * days + position.longitude) - ra
    lat = np.radians(position.latitude)
    return np.degrees(np.arcsin(np.sin(lat) * np.sin(dec) + np.cos(lat) * np.cos(dec) * np.cos(hour_angle)))


def _bisect(f, lo, hi, steps: int):
    """Vectorised bisection over arrays of Julian dates where f(lo) < 0 <= f(hi)."""
    for _ in range(steps):
        mid = (lo + hi) / 2
        before = f(mid) < 0
        lo, hi = np.where(before, mid, lo), np.where(before, hi, mid)
    return hi


def find_conjunctions(start_date: dt.datetime, end_date: dt.datetime) -> List[dt.datetime]:
    """Return the UTC instant of every astronomical new moon in the range.

    The new moon is the moment the moon and sun share the same geocentric
    ecliptic longitude, which is how published tables (e.g. USNO) define it.
    """
    jd = Time(start_date).jd + np.arange((end_date - start_date).days + 2)
    elongation = _elongation(jd)
    # Elongation climbs through zero at new moon (at full moon it wraps downward)
    i = np.where((elongation[:-1] < 0) & (elongation[1:] >= 0))[0]
    if len(i) == 0:
        return []
    lo, hi, f_lo, f_hi = jd[i], jd[i + 1], elongation[i], elongation[i + 1]
    # Elongation is nearly linear over a day, so three secant steps get well under a second
    for _ in range(3):
        slope = np.where(f_hi == f_lo, 1.0, f_hi - f_lo)
        lo, hi, f_lo = hi, hi - f_hi * (hi - lo) / slope, f_hi
        f_hi = _elongation(hi)
    found = Time(hi, format='jd').to_datetime()
    return [c for c in found if start_date <= c <= end_date]


def new_moon_days(conjunctions: List[dt.datetime]) -> List[dt.date]:
    """Return the date on which each conjunction's evening-to-evening day begins.

    A conjunction before nightfall belongs to the day that began the evening
    before, so it is dated one day earlier than its civil date.
    """
    if not conjunctions:
        return []
    position = DAY_START_LOCATION.value
    # Civil date at the day-start location, from local mean solar time
    local = [(c + dt.timedelta(hours=position.longitude / 15)).date() for c in conjunctions]
    noon = Time([dt.datetime(d.year, d.month, d.day, 12) for d in local]).jd - position.longitude / 360
    # 13 halvings of the half day from noon to midnight resolve nightfall to about 5 seconds
    nightfall = _bisect(lambda jd: DAY_START_SUN_ALTITUDE - _sun_altitude(jd, position), noon, noon + 0.5, steps=13)
    return [d if c >= n else d - dt.timedelta(days=1)
            for d, c, n in zip(local, Time(conjunctions).jd, nightfall)]


def enumerate_new_moons(start_date: dt.datetime, end_date: dt.datetime) -> Dict[dt.datetime,float]:
    """Return each new moon day in the range with its sun-moon angle at noon UTC.

    The new moon day is the evening-to-evening day containing the conjunction,
    dated by the evening it begins on.
    """
    margin = dt.timedelta(days=2)
    conjunctions = find_conjunctions(start_date - margin, end_date + margin)
    days = [dt.datetime.combine(d, dt.time()) for d in new_moon_days(conjunctions)]
    days = [d for d in days if start_date <= d <= end_date]
    if not days:
        return {}
    noon = Time([_at_noon(d) for d in days])
    angles = get_body("moon", noon).separation(get_body("sun", noon)).degree
    return dict(zip(days, angles))


def enumerate_sabbaths(new_moons: List[dt.datetime]) -> List[dt.datetime]:
    """Count the number of new moons from start_date to end_date."""
    return reduce(fn, new_moons[1:], [new_moons[0]])

def fn(nms: List[dt.datetime], nm: dt.datetime) -> List[dt.datetime]:
    last_sabbath = nms[-1]
    # Generate sabbaths at 7-day intervals using list comprehension
    sabbaths_between = [last_sabbath + dt.timedelta(days=i)
                        for i in range(7, (nm - last_sabbath).days, 7)]
    return nms + sabbaths_between + [nm]


# Print the result
if __name__ == '__main__':
    # Test for the given date and time
    date_obs_test = dt.datetime(2023, 8, 15, 20, 0,0)
    moon_phase = get_moon_phase(date_obs_test)
    print(f'The moon phase for {date_obs_test} is {moon_phase}.')
    start_date = dt.datetime(2022, 1, 1)
    end_date = dt.datetime(2028, 1, 1)
