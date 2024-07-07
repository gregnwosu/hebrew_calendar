import calendar
import datetime as dt
from dataclasses import dataclass, field
from typing import Dict, List
from moon import FeastDays, enumerate_sabbaths, enumerate_new_moons
import streamlit as st
from typing import Dict, List, Any

@dataclass
class CalendarData:
    start_of_lunar_year: dt.date
    feast_dates: Dict[dt.date, FeastDays] = field(init=False)
    sabbath_dates: List[dt.date] = field(init=False)
    new_moon_dates: Dict[dt.date, float] = field(init=False)
    
    def __post_init__(self):
        self.feast_dates = FeastDays.find_feast_days(self.start_of_lunar_year)
        self.new_moon_dates = enumerate_new_moons(self.start_of_lunar_year, self.start_of_lunar_year + dt.timedelta(days=365))
        self.sabbath_dates = enumerate_sabbaths(list(self.new_moon_dates.keys()))

@dataclass
class Calendar:
    data: CalendarData
    current_date: dt.date = dt.date.today()

    def get_day_info(self, date: dt.date) -> Dict[str, str]:
        info = {}
        if date in self.data.feast_dates:
            feast = self.data.feast_dates[date]
            info['feast'] = f"{feast.name} ({feast.bible_ref}): {feast.description}"
        if date in self.data.new_moon_dates:
            phase_angle = self.data.new_moon_dates[date]
            info['new_moon'] = f"New Moon (phase angle {phase_angle:.2f})"
        if date in self.data.sabbath_dates:
            info['sabbath'] = "Sabbath"
        return info

    def get_month_calendar(self) -> List[List[Dict[str, Any]]]:
        cal = calendar.monthcalendar(self.current_date.year, self.current_date.month)
        month_data = []
        for week in cal:
            week_data = []
            for day in week:
                if day == 0:
                    week_data.append(None)
                else:
                    date = dt.date(self.current_date.year, self.current_date.month, day)
                    day_info = self.get_day_info(date)
                    week_data.append({
                        'day': day,
                        'info': day_info,
                        'is_current': date == self.current_date
                    })
            month_data.append(week_data)
        return month_data

def create_streamlit_calendar():
    st.set_page_config(page_title="Lunar Calendar", page_icon="🌙", layout="wide")
    st.title("Lunar Calendar")

    start_of_lunar_year = dt.date(2023, 1, 1)  # You may want to make this configurable
    calendar_data = CalendarData(start_of_lunar_year)
    calendar = Calendar(calendar_data)

    col1, col2 = st.columns([3, 1])

    with col1:
        st.header(calendar.current_date.strftime('%B %Y'))
        month_data = calendar.get_month_calendar()

        for week in month_data:
            cols = st.columns(7)
            for day, col in zip(week, cols):
                if day is None:
                    col.empty()
                else:
                    with col:
                        if day['is_current']:
                            st.markdown(f"**{day['day']}**")
                        else:
                            st.write(day['day'])
                        
                        if 'feast' in day['info']:
                            st.markdown("🎉")
                        if 'new_moon' in day['info']:
                            st.markdown("🌑")
                        if 'sabbath' in day['info']:
                            st.markdown("✡️")

    with col2:
        st.header("Day Information")
        day_info = calendar.get_day_info(calendar.current_date)
        if day_info:
            for key, value in day_info.items():
                st.write(f"**{key.capitalize()}:** {value}")
        else:
            st.write("No special information for this day.")

        st.write("---")
        st.write("Navigate:")
        col_prev, col_next = st.columns(2)
        with col_prev:
            if st.button("Previous Month"):
                calendar.current_date = calendar.current_date.replace(day=1) - dt.timedelta(days=1)
                st.experimental_rerun()
        with col_next:
            if st.button("Next Month"):
                calendar.current_date = (calendar.current_date.replace(day=1) + dt.timedelta(days=32)).replace(day=1)
                st.experimental_rerun()

if __name__ == "__main__":
    create_streamlit_calendar()