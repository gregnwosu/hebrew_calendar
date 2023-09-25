# Hebrew Lunar Calendar

## About
This project provides a Hebrew Lunar Calendar for a specified year, it incldues the following features:
* The calendar is based on the Hebrew calendar
* The calendar include details of Hebrew Feasts and Holidays
* Biblical References are printed for each feast and holiday when selected
* The calendar include details of new moons and sabbaths


## Installation
The project requirements can be installed using pip:
```bash
pip3 install -r requirements.txt
``` 
### Specifiying the Hebrew Year
In terminal.py, the year can be specified by changing the following line:
the start of the hebrew calendar year should be specified in Gregorian date format:
e.g. The hebrew year for 2023 started on 19th February 2023, so....
```python
def main(stdscr):
    lunar_year_start = dt.date(2023, 2, 19)
    calendar_app = TerminalCalendar(lunar_year_start, stdscr)
    run(calendar_app)
```
## Usage
The calendar can be used in two ways:
* As a command line tool
* As a library

### Command Line Tool

After requirements are installed, the command line tool can be used to print a calendar for a specified year, the following command starts the calendar:
```bash
The command line tool can be used to print a calendar for a specified year, the following command will print the calendar for the year 2020:
```bash
python3 terminal.py 2020
```

### Future Features
Streamlit is a great tool for building data apps, so I am planning to build a web app using streamlit to display the calendar.
