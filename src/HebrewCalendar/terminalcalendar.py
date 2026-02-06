import calendar
import curses
import datetime as dt
from dataclasses import dataclass, field
from typing import Any, Dict, List
from moon import FeastDays, enumerate_sabbaths, enumerate_new_moons


@dataclass
class TerminalCalendar:
    start_of_lunar_year: dt.date
    stdscr: Any = curses.initscr()
    current_date: dt.date = dt.datetime.today()
    feast_dates: Dict[dt.datetime, FeastDays] = field(init=False)
    sabbath_dates: List[dt.datetime] = field(init=False)
    new_moon_dates: List[dt.datetime] = field(init=False)
    
    def __post_init__(self):
        self.new_moon_dates = enumerate_new_moons(self.start_of_lunar_year, self.start_of_lunar_year + dt.timedelta(days=365))
        new_moon_list = list(self.new_moon_dates.keys())
        self.feast_dates = FeastDays.find_feast_days(self.start_of_lunar_year, new_moon_list)
        self.sabbath_dates = enumerate_sabbaths(new_moon_list)
        curses.curs_set(0)  # Hide the cursor
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)  
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLUE,  curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
    
    @property
    def highlighted_day(self):
        return self.current_date.day
    
    def add_days(self, value: int):
        self.current_date += dt.timedelta(days=value)
        
    def draw_calendar(self):
        self.stdscr.clear()
        cal = calendar.monthcalendar(self.current_date.year, self.current_date.month)
        month_name = self.current_date.strftime('%B %Y')
        self.stdscr.addstr(0, 0, month_name, curses.A_BOLD)

        for idx, day in enumerate(calendar.day_name):
            self.stdscr.addstr(2, idx * 4, day[:2], curses.A_BOLD)

        for row, week in enumerate(cal):
            for col, day in enumerate(week):
                if day:
                    mode = self.set_ink_color(day)
                    self.stdscr.addstr(row + 3, col * 4, f"{day:2}", mode)

        current_date = dt.date(self.current_date.year, self.current_date.month, self.highlighted_day)
        if current_date in self.feast_dates:
            feast = self.feast_dates[current_date]
            self.stdscr.addstr(10, 0, f"{feast.name}  ({', '.join(feast.bible_refs) if feast.bible_refs else ''}) ")
            self.stdscr.addstr(11, 0, f"{feast.description}")
        if current_date in self.new_moon_dates:
            phase_angle = self.new_moon_dates[current_date]
            self.stdscr.addstr(9, 0, f"New Moon  (phase angle {phase_angle}) ")
            
        
        
        self.stdscr.refresh()

    def set_ink_color(self, day):
        current_actual_date = dt.date(self.current_date.year, self.current_date.month, day)
        if day == self.highlighted_day:
            return curses.A_REVERSE 
        if current_actual_date in self.new_moon_dates:
            return curses.color_pair(4)
        if current_actual_date in self.sabbath_dates:
            return curses.color_pair(3)
        if current_actual_date in self.feast_dates:
            return curses.color_pair(2)
        return curses.A_NORMAL