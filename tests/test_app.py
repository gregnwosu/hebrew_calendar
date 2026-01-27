import datetime as dt
import pytest
from app import (
    app, server,
    FEAST_DATES, NEW_MOON_DATES, SABBATH_DATES,
    get_day_style, create_calendar_grid, get_day_info,
)
from moon import FeastDays, FeastDay, get_moon_phase, enumerate_new_moons, enumerate_sabbaths, add_months_and_days


# ---------------------------------------------------------------------------
# Date normalisation – all lookup keys must be dt.date, not dt.datetime
# ---------------------------------------------------------------------------

class TestDateNormalisation:
    def test_feast_dates_keys_are_date(self):
        for k in FEAST_DATES:
            assert type(k) is dt.date, f"Expected dt.date but got {type(k)} for {k}"

    def test_new_moon_dates_keys_are_date(self):
        for k in NEW_MOON_DATES:
            assert type(k) is dt.date, f"Expected dt.date but got {type(k)} for {k}"

    def test_sabbath_dates_are_date(self):
        for d in SABBATH_DATES:
            assert type(d) is dt.date, f"Expected dt.date but got {type(d)} for {d}"


# ---------------------------------------------------------------------------
# Moon phase calculations
# ---------------------------------------------------------------------------

class TestMoonPhase:
    @pytest.mark.parametrize("date_obs, expected", [
        (dt.datetime(2024, 2, 10, 12, 0), "New Moon"),
        (dt.datetime(2024, 3, 10, 12, 0), "New Moon"),
        (dt.datetime(2024, 4, 8, 12, 0),  "New Moon"),
    ])
    def test_known_new_moons_2024(self, date_obs, expected):
        phase, angle = get_moon_phase(date_obs)
        assert phase == expected, f"Expected {expected} but got {phase} (angle={angle:.1f})"

    def test_full_moon(self):
        # 24 Feb 2024 was a full moon
        phase, angle = get_moon_phase(dt.datetime(2024, 2, 24, 12, 0))
        assert phase == "Full Moon", f"Expected Full Moon but got {phase} (angle={angle:.1f})"

    def test_phase_returns_tuple(self):
        result = get_moon_phase(dt.datetime(2024, 6, 15, 12, 0))
        assert isinstance(result, tuple)
        assert len(result) == 2
        phase, angle = result
        assert isinstance(phase, str)
        assert isinstance(angle, float)

    def test_all_phase_names_valid(self):
        valid = {"New Moon", "Waxing Crescent", "First Quarter", "Waxing Gibbous",
                 "Full Moon", "Waning Gibbous", "Third Quarter", "Waning Crescent"}
        # Sample one date per week across a month
        for day in range(1, 29):
            phase, _ = get_moon_phase(dt.datetime(2024, 3, day, 12, 0))
            assert phase in valid, f"Unexpected phase: {phase}"


# ---------------------------------------------------------------------------
# New moon enumeration
# ---------------------------------------------------------------------------

class TestEnumerateNewMoons:
    def test_roughly_one_per_month(self):
        start = dt.datetime(2024, 1, 1)
        end = dt.datetime(2024, 12, 31)
        moons = enumerate_new_moons(start, end)
        # There should be 12 or 13 new moons in a calendar year
        assert 12 <= len(moons) <= 13, f"Got {len(moons)} new moons in 2024"

    def test_new_moons_are_sorted(self):
        start = dt.datetime(2024, 1, 1)
        end = dt.datetime(2024, 12, 31)
        moons = list(enumerate_new_moons(start, end).keys())
        assert moons == sorted(moons)

    def test_spacing_roughly_29_days(self):
        start = dt.datetime(2024, 1, 1)
        end = dt.datetime(2024, 12, 31)
        dates = list(enumerate_new_moons(start, end).keys())
        for i in range(1, len(dates)):
            gap = (dates[i] - dates[i - 1]).days
            assert 28 <= gap <= 31, f"Gap between new moons was {gap} days"


# ---------------------------------------------------------------------------
# Sabbath enumeration
# ---------------------------------------------------------------------------

class TestEnumerateSabbaths:
    def test_sabbaths_spaced_by_seven_days(self):
        start = dt.datetime(2024, 2, 9)
        moons = enumerate_new_moons(start, start + dt.timedelta(days=90))
        sabbaths = enumerate_sabbaths(list(moons.keys()))
        for i in range(1, len(sabbaths)):
            gap = (sabbaths[i] - sabbaths[i - 1]).days
            # Gap should be 7 or less (new moon resets)
            assert 1 <= gap <= 7, f"Sabbath gap was {gap} days between {sabbaths[i-1]} and {sabbaths[i]}"

    def test_sabbaths_include_new_moons(self):
        start = dt.datetime(2024, 2, 9)
        moons = enumerate_new_moons(start, start + dt.timedelta(days=90))
        moon_list = list(moons.keys())
        sabbaths = enumerate_sabbaths(moon_list)
        for nm in moon_list:
            assert nm in sabbaths, f"New moon {nm} not in sabbath list"


# ---------------------------------------------------------------------------
# Feast days
# ---------------------------------------------------------------------------

class TestFeastDays:
    def test_feast_dates_not_empty(self):
        assert len(FEAST_DATES) > 0

    def test_all_values_are_feast_day(self):
        for v in FEAST_DATES.values():
            assert isinstance(v, FeastDay), f"Expected FeastDay but got {type(v)}"

    def test_passover_present(self):
        names = [fd.name for fd in FEAST_DATES.values()]
        assert any("Passover" in n for n in names), "Passover not found in feast dates"

    def test_yom_kippur_present(self):
        names = [fd.name for fd in FEAST_DATES.values()]
        assert any("Atonement" in n for n in names), "Day of Atonement not found"

    def test_sukkot_seven_days_per_year(self):
        """Each lunar year should have exactly 7 Sukkot days."""
        sukkot_days = sorted(k for k, v in FEAST_DATES.items() if "Tabernacles" in v.name)
        # Group by contiguous blocks (7 consecutive days = one observance)
        assert len(sukkot_days) >= 7, f"Expected at least 7 Sukkot days, got {len(sukkot_days)}"
        assert len(sukkot_days) % 7 == 0, f"Sukkot days should be multiple of 7, got {len(sukkot_days)}"

    def test_unleavened_bread_seven_days_per_year(self):
        days = sorted(k for k, v in FEAST_DATES.items() if "Unleavened" in v.name)
        assert len(days) >= 7
        assert len(days) % 7 == 0, f"Unleavened Bread should be multiple of 7, got {len(days)}"

    def test_hanukkah_eight_days_per_year(self):
        days = sorted(k for k, v in FEAST_DATES.items() if "Hanukkah" in v.name)
        assert len(days) >= 8
        assert len(days) % 8 == 0, f"Hanukkah should be multiple of 8, got {len(days)}"

    def test_purim_two_days_per_year(self):
        days = sorted(k for k, v in FEAST_DATES.items() if "Purim" in v.name)
        assert len(days) >= 2
        assert len(days) % 2 == 0, f"Purim should be multiple of 2, got {len(days)}"

    def test_feast_data_covers_2026(self):
        """The app must have feast data for the current year (2026)."""
        feast_years = {k.year for k in FEAST_DATES}
        assert 2026 in feast_years, f"No feast data for 2026. Years covered: {sorted(feast_years)}"


# ---------------------------------------------------------------------------
# Multi-year data coverage
# ---------------------------------------------------------------------------

class TestMultiYearCoverage:
    def test_new_moons_span_multiple_years(self):
        years = {k.year for k in NEW_MOON_DATES}
        assert len(years) >= 3, f"Expected 3+ years of new moon data, got {sorted(years)}"

    def test_sabbaths_span_multiple_years(self):
        years = {d.year for d in SABBATH_DATES}
        assert len(years) >= 3, f"Expected 3+ years of sabbath data, got {sorted(years)}"

    def test_data_covers_2024_to_2027(self):
        moon_years = {k.year for k in NEW_MOON_DATES}
        for y in (2024, 2025, 2026, 2027):
            assert y in moon_years, f"Missing new moon data for {y}"

    def test_today_has_badge_data(self):
        """Today's month should have at least one special day."""
        today = dt.date.today()
        first = dt.date(today.year, today.month, 1)
        import calendar as cal_mod
        last_day = cal_mod.monthrange(today.year, today.month)[1]
        last = dt.date(today.year, today.month, last_day)
        has_special = any(
            first <= d <= last
            for d in list(NEW_MOON_DATES.keys()) + list(FEAST_DATES.keys()) + list(SABBATH_DATES)
        )
        assert has_special, f"No special days found for {today.strftime('%B %Y')}"


# ---------------------------------------------------------------------------
# Calendar grid rendering
# ---------------------------------------------------------------------------

class TestCalendarGrid:
    def test_returns_table(self):
        from dash import html
        grid = create_calendar_grid(2024, 3, 15)
        assert isinstance(grid, html.Table)

    def test_header_row_has_seven_days(self):
        grid = create_calendar_grid(2024, 3, 1)
        header_row = grid.children[0]  # First Tr is the header
        assert len(header_row.children) == 7

    def test_selected_day_has_border(self):
        grid = create_calendar_grid(2024, 3, 15)
        found = False
        for row in grid.children[1:]:  # Skip header
            for cell in row.children:
                if cell.children == "15":
                    assert "border" in cell.style
                    assert "#ffc107" in cell.style["border"]
                    found = True
        assert found, "Day 15 cell not found"

    def test_all_month_days_present(self):
        import calendar as cal_mod
        grid = create_calendar_grid(2024, 2, 1)  # Feb 2024 = 29 days (leap year)
        day_texts = []
        for row in grid.children[1:]:
            for cell in row.children:
                if cell.children and cell.children != "":
                    day_texts.append(int(cell.children))
        assert max(day_texts) == 29
        assert min(day_texts) == 1
        assert len(day_texts) == 29

    def test_day_cells_have_click_id(self):
        grid = create_calendar_grid(2024, 3, 1)
        for row in grid.children[1:]:
            for cell in row.children:
                if cell.children and cell.children != "":
                    assert cell.id is not None
                    assert cell.id["type"] == "day-cell"
                    assert cell.id["day"] == int(cell.children)


# ---------------------------------------------------------------------------
# Day styling
# ---------------------------------------------------------------------------

class TestDayStyle:
    def test_new_moon_gets_teal(self):
        nm_date = list(NEW_MOON_DATES.keys())[0]
        style = get_day_style(nm_date)
        assert style["backgroundColor"] == "#17a2b8"

    def test_feast_gets_green(self):
        # Find a feast date that is NOT also a new moon
        for fd in FEAST_DATES:
            if fd not in NEW_MOON_DATES:
                style = get_day_style(fd)
                assert style["backgroundColor"] == "#198754"
                return
        pytest.skip("All feast dates are also new moons")

    def test_sabbath_gets_blue(self):
        # Find a sabbath that is not a new moon or feast
        for s in SABBATH_DATES:
            if s not in NEW_MOON_DATES and s not in FEAST_DATES:
                style = get_day_style(s)
                assert style["backgroundColor"] == "#0d6efd"
                return
        pytest.skip("All sabbaths overlap with moons or feasts")

    def test_regular_day_no_background(self):
        # Find a day with no special status
        for day_offset in range(1, 365):
            d = dt.date(2024, 1, 1) + dt.timedelta(days=day_offset)
            if d not in NEW_MOON_DATES and d not in FEAST_DATES and d not in SABBATH_DATES:
                style = get_day_style(d)
                assert style == {}
                return


# ---------------------------------------------------------------------------
# Day info panel
# ---------------------------------------------------------------------------

class TestDayInfo:
    def test_info_returns_list(self):
        info = get_day_info(dt.date(2024, 3, 15))
        assert isinstance(info, list)
        assert len(info) >= 1

    def test_info_starts_with_date_header(self):
        from dash import html
        info = get_day_info(dt.date(2024, 3, 15))
        assert isinstance(info[0], html.H6)

    def test_new_moon_date_shows_phase_angle(self):
        nm_date = list(NEW_MOON_DATES.keys())[0]
        info = get_day_info(nm_date)
        text = str(info)
        assert "New Moon" in text
        assert "phase angle" in text

    def test_feast_date_shows_name_and_ref(self):
        feast_date = list(FEAST_DATES.keys())[0]
        feast = FEAST_DATES[feast_date]
        info = get_day_info(feast_date)
        text = str(info)
        assert feast.name in text

    def test_regular_day_shows_moon_phase(self):
        # Find a non-special day
        for day_offset in range(1, 365):
            d = dt.date(2024, 1, 1) + dt.timedelta(days=day_offset)
            if d not in NEW_MOON_DATES and d not in FEAST_DATES and d not in SABBATH_DATES:
                info = get_day_info(d)
                text = str(info)
                assert "Moon phase" in text
                return


# ---------------------------------------------------------------------------
# Flask server / Dash app
# ---------------------------------------------------------------------------

class TestFlaskServer:
    def test_server_exists(self):
        assert server is not None

    def test_index_returns_200(self):
        with server.test_client() as client:
            resp = client.get("/")
            assert resp.status_code == 200

    def test_dash_layout_endpoint(self):
        with server.test_client() as client:
            resp = client.get("/_dash-layout")
            assert resp.status_code == 200
            data = resp.get_json()
            assert data is not None

    def test_layout_contains_title(self):
        with server.test_client() as client:
            resp = client.get("/_dash-layout")
            body = resp.get_data(as_text=True)
            assert "Hebrew Calendar" in body
