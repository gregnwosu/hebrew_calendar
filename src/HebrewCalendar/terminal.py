import curses
from .terminalcalendar import TerminalCalendar
import datetime as dt

key_callbacks = {
    curses.KEY_RIGHT: [],
    curses.KEY_LEFT: [],
    curses.KEY_DOWN: [],
    curses.KEY_UP: [],
    ord('q'): [],
    ord('Q'): []
}

def add_key_callback(key, callback):
    key_callbacks[key].append(callback)

def run(tc: TerminalCalendar):
    add_key_callback(curses.KEY_RIGHT, lambda: tc.add_days(1))
    add_key_callback(curses.KEY_LEFT,  lambda: tc.add_days(-1))
    add_key_callback(curses.KEY_DOWN,  lambda: tc.add_days(7))
    add_key_callback(curses.KEY_UP,    lambda: tc.add_days(-7))
    add_key_callback(ord('q'), exit)
    add_key_callback(ord('Q'), exit)

    while True:
        tc.draw_calendar()
        ch = tc.stdscr.getch()
        # Trigger callbacks based on keypress
        if ch in key_callbacks:
            for fn in key_callbacks[ch]:
                fn()

    lunar_year_start = dt.date(2024, 2, 19)
>>>>>>> ca2b5eb8ed2fa45a68e137704f9442d6cfe8ee03
    calendar_app = TerminalCalendar(lunar_year_start, stdscr)
    run(calendar_app)
=======
    lunar_year_start = dt.date(2024, 2, 19)
>>>>>>> ca2b5eb8ed2fa45a68e137704f9442d6cfe8ee03
    calendar_app = TerminalCalendar(lunar_year_start, stdscr)
    run(calendar_app)

if __name__ == '__main__':
    curses.wrapper(main)
