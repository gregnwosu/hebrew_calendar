"""Tests comparing calendar calculations against reference observational data.

Reference data source: YouTube channel dates for new moons and holy days.
These represent one interpretation of the Hebrew calendar based on observation.
"""

import pytest
import datetime as dt
from moon import enumerate_new_moons, FeastDays, get_vernal_equinox, get_lunar_year_starts, get_autumn_equinox


# Reference New Moons from observational data
REFERENCE_NEW_MOONS = [
    dt.date(2026, 1, 18),   # January 18, 2026; Sunday eve
    dt.date(2025, 12, 19),  # December 19, 2025; Friday eve
    dt.date(2025, 11, 19),  # November 19, 2025; Wednesday eve
    dt.date(2025, 10, 20),  # October 20, 2025; Monday eve
    dt.date(2025, 9, 21),   # September 21, 2025; Sunday eve
    dt.date(2025, 8, 22),   # August 22, 2025; Friday eve
    dt.date(2025, 7, 24),   # July 24, 2025; Thursday eve
    dt.date(2025, 6, 24),   # June 24, 2025; Tuesday eve
    dt.date(2025, 5, 26),   # May 26, 2025; Monday eve
    dt.date(2025, 4, 27),   # April 27, 2025; Sunday eve
    dt.date(2025, 3, 28),   # March 28, 2025; Friday eve
    dt.date(2025, 2, 27),   # February 27, 2025; Thursday eve
    dt.date(2025, 1, 28),   # January 28, 2025; Tuesday eve
    dt.date(2024, 12, 30),  # December 30, 2024; Monday eve
    dt.date(2024, 11, 30),  # November 30, 2024; Saturday eve
    dt.date(2024, 10, 31),  # October 31, 2024; Thursday eve
    dt.date(2024, 10, 2),   # October 02, 2024; Wednesday eve
    dt.date(2024, 9, 2),    # September 02, 2024; Monday eve
    dt.date(2024, 8, 3),    # August 03, 2024; Saturday eve
    dt.date(2024, 7, 5),    # July 05, 2024; Friday eve
]

# Reference Feast Days
REFERENCE_FEASTS_2025 = {
    'Trumpets': dt.date(2025, 9, 21),
    'Atonement': dt.date(2025, 9, 30),
    'Tabernacles Start': dt.date(2025, 10, 5),
    'Tabernacles End': dt.date(2025, 10, 12),
    'Hanukkah Start': dt.date(2025, 12, 13),
    'Hanukkah End': dt.date(2025, 12, 20),
}

REFERENCE_FEASTS_2024 = {
    'Atonement': dt.date(2024, 9, 11),
    'Tabernacles Start': dt.date(2024, 9, 16),
    'Tabernacles End': dt.date(2024, 9, 23),
    'Hanukkah Start': dt.date(2024, 11, 24),
    'Hanukkah End': dt.date(2024, 12, 1),
}


@pytest.fixture
def calculated_new_moons():
    """Calculate new moons for the test period."""
    start_date = dt.datetime(2024, 7, 1)
    end_date = dt.datetime(2026, 2, 1)
    return enumerate_new_moons(start_date, end_date)


@pytest.fixture
def full_new_moons():
    """Calculate new moons for a wider range."""
    start_date = dt.datetime(2024, 1, 1)
    end_date = dt.datetime(2026, 12, 31)
    return enumerate_new_moons(start_date, end_date)


@pytest.fixture
def year_starts(full_new_moons):
    """Calculate lunar year starts."""
    return get_lunar_year_starts(full_new_moons, 2024, 2025)


class TestNewMoons:
    """Tests comparing calculated new moons with reference data."""

    def test_new_moon_july_2024(self, calculated_new_moons):
        """July 5, 2024 new moon."""
        calc_dates = [d.date() for d in calculated_new_moons.keys()]
        assert dt.date(2024, 7, 5) in calc_dates

    def test_new_moon_september_2024(self, calculated_new_moons):
        """September 2, 2024 new moon."""
        calc_dates = [d.date() for d in calculated_new_moons.keys()]
        assert dt.date(2024, 9, 2) in calc_dates

    def test_new_moon_october_2_2024(self, calculated_new_moons):
        """October 2, 2024 new moon."""
        calc_dates = [d.date() for d in calculated_new_moons.keys()]
        assert dt.date(2024, 10, 2) in calc_dates

    def test_new_moon_october_31_2024(self, calculated_new_moons):
        """October 31, 2024 new moon."""
        calc_dates = [d.date() for d in calculated_new_moons.keys()]
        assert dt.date(2024, 10, 31) in calc_dates

    def test_new_moon_november_2024(self, calculated_new_moons):
        """November 30, 2024 new moon."""
        calc_dates = [d.date() for d in calculated_new_moons.keys()]
        assert dt.date(2024, 11, 30) in calc_dates

    def test_new_moon_december_2024(self, calculated_new_moons):
        """December 30, 2024 new moon."""
        calc_dates = [d.date() for d in calculated_new_moons.keys()]
        assert dt.date(2024, 12, 30) in calc_dates

    def test_new_moon_february_2025(self, calculated_new_moons):
        """February 27, 2025 new moon."""
        calc_dates = [d.date() for d in calculated_new_moons.keys()]
        assert dt.date(2025, 2, 27) in calc_dates

    def test_new_moon_april_2025(self, calculated_new_moons):
        """April 27, 2025 new moon."""
        calc_dates = [d.date() for d in calculated_new_moons.keys()]
        assert dt.date(2025, 4, 27) in calc_dates

    def test_new_moon_may_2025(self, calculated_new_moons):
        """May 26, 2025 new moon."""
        calc_dates = [d.date() for d in calculated_new_moons.keys()]
        assert dt.date(2025, 5, 26) in calc_dates

    def test_new_moon_july_2025(self, calculated_new_moons):
        """July 24, 2025 new moon."""
        calc_dates = [d.date() for d in calculated_new_moons.keys()]
        assert dt.date(2025, 7, 24) in calc_dates

    def test_new_moon_august_2025(self, calculated_new_moons):
        """August 22, 2025 new moon."""
        calc_dates = [d.date() for d in calculated_new_moons.keys()]
        assert dt.date(2025, 8, 22) in calc_dates

    def test_new_moon_september_2025(self, calculated_new_moons):
        """September 21, 2025 new moon."""
        calc_dates = [d.date() for d in calculated_new_moons.keys()]
        assert dt.date(2025, 9, 21) in calc_dates

    def test_new_moon_october_2025(self, calculated_new_moons):
        """October 20, 2025 new moon."""
        calc_dates = [d.date() for d in calculated_new_moons.keys()]
        assert dt.date(2025, 10, 20) in calc_dates

    def test_new_moon_november_2025(self, calculated_new_moons):
        """November 19, 2025 new moon."""
        calc_dates = [d.date() for d in calculated_new_moons.keys()]
        assert dt.date(2025, 11, 19) in calc_dates

    def test_new_moon_december_2025(self, calculated_new_moons):
        """December 19, 2025 new moon."""
        calc_dates = [d.date() for d in calculated_new_moons.keys()]
        assert dt.date(2025, 12, 19) in calc_dates

    def test_new_moon_january_2026(self, calculated_new_moons):
        """January 18, 2026 new moon."""
        calc_dates = [d.date() for d in calculated_new_moons.keys()]
        assert dt.date(2026, 1, 18) in calc_dates

    @pytest.mark.xfail(reason="Calendar calculates Aug 4 instead of Aug 3 - 1 day difference")
    def test_new_moon_august_2024(self, calculated_new_moons):
        """August 3, 2024 new moon - KNOWN DISCREPANCY."""
        calc_dates = [d.date() for d in calculated_new_moons.keys()]
        assert dt.date(2024, 8, 3) in calc_dates

    @pytest.mark.xfail(reason="Calendar calculates Jan 29 instead of Jan 28 - 1 day difference")
    def test_new_moon_january_2025(self, calculated_new_moons):
        """January 28, 2025 new moon - KNOWN DISCREPANCY."""
        calc_dates = [d.date() for d in calculated_new_moons.keys()]
        assert dt.date(2025, 1, 28) in calc_dates

    @pytest.mark.xfail(reason="Calendar calculates Mar 29 instead of Mar 28 - 1 day difference")
    def test_new_moon_march_2025(self, calculated_new_moons):
        """March 28, 2025 new moon - KNOWN DISCREPANCY."""
        calc_dates = [d.date() for d in calculated_new_moons.keys()]
        assert dt.date(2025, 3, 28) in calc_dates

    @pytest.mark.xfail(reason="Calendar calculates Jun 25 instead of Jun 24 - 1 day difference")
    def test_new_moon_june_2025(self, calculated_new_moons):
        """June 24, 2025 new moon - KNOWN DISCREPANCY."""
        calc_dates = [d.date() for d in calculated_new_moons.keys()]
        assert dt.date(2025, 6, 24) in calc_dates


class TestFeastDays:
    """Tests for feast day calculations."""

    def test_vernal_equinox_2024(self):
        """Vernal equinox 2024 should be around March 20."""
        equinox = get_vernal_equinox(2024)
        assert equinox == dt.date(2024, 3, 20)

    def test_vernal_equinox_2025(self):
        """Vernal equinox 2025 should be around March 20-21."""
        equinox = get_vernal_equinox(2025)
        assert equinox in [dt.date(2025, 3, 20), dt.date(2025, 3, 21)]

    def test_autumn_equinox_2024(self):
        """Autumn equinox 2024 should be around September 22-23."""
        equinox = get_autumn_equinox(2024)
        assert equinox in [dt.date(2024, 9, 22), dt.date(2024, 9, 23)]

    def test_autumn_equinox_2025(self):
        """Autumn equinox 2025 should be around September 22-23."""
        equinox = get_autumn_equinox(2025)
        assert equinox in [dt.date(2025, 9, 22), dt.date(2025, 9, 23)]

    def test_trumpets_2025(self, year_starts, full_new_moons):
        """Feast of Trumpets 2025 should be September 21."""
        new_moon_list = list(full_new_moons.keys())
        feasts = FeastDays.find_feast_days(year_starts[2025], new_moon_list)
        trumpets_dates = [d.date() for d, f in feasts.items() if 'Trumpets' in f.name]
        assert dt.date(2025, 9, 21) in trumpets_dates

    def test_atonement_2025(self, year_starts, full_new_moons):
        """Day of Atonement 2025 should be September 30."""
        new_moon_list = list(full_new_moons.keys())
        feasts = FeastDays.find_feast_days(year_starts[2025], new_moon_list)
        atonement_dates = [d.date() for d, f in feasts.items() if 'Atonement' in f.name]
        assert dt.date(2025, 9, 30) in atonement_dates

    def test_tabernacles_2025_start(self, year_starts, full_new_moons):
        """Feast of Tabernacles 2025 should start October 5."""
        new_moon_list = list(full_new_moons.keys())
        feasts = FeastDays.find_feast_days(year_starts[2025], new_moon_list)
        tabernacles_dates = sorted([d.date() for d, f in feasts.items() if 'Tabernacles' in f.name])
        assert tabernacles_dates[0] == dt.date(2025, 10, 5)

    def test_tabernacles_2025_end(self, year_starts, full_new_moons):
        """Feast of Tabernacles 2025 should end October 12."""
        new_moon_list = list(full_new_moons.keys())
        feasts = FeastDays.find_feast_days(year_starts[2025], new_moon_list)
        tabernacles_dates = sorted([d.date() for d, f in feasts.items() if 'Tabernacles' in f.name])
        assert tabernacles_dates[-1] == dt.date(2025, 10, 12)

    def test_hanukkah_2025_start(self, year_starts, full_new_moons):
        """Hanukkah 2025 should start December 13."""
        new_moon_list = list(full_new_moons.keys())
        feasts = FeastDays.find_feast_days(year_starts[2025], new_moon_list)
        hanukkah_dates = sorted([d.date() for d, f in feasts.items() if 'Hanukkah' in f.name])
        assert hanukkah_dates[0] == dt.date(2025, 12, 13)

    def test_hanukkah_2025_end(self, year_starts, full_new_moons):
        """Hanukkah 2025 should end December 20."""
        new_moon_list = list(full_new_moons.keys())
        feasts = FeastDays.find_feast_days(year_starts[2025], new_moon_list)
        hanukkah_dates = sorted([d.date() for d, f in feasts.items() if 'Hanukkah' in f.name])
        assert hanukkah_dates[-1] == dt.date(2025, 12, 20)

    def test_atonement_2024(self, year_starts, full_new_moons):
        """Day of Atonement 2024 should be September 11."""
        new_moon_list = list(full_new_moons.keys())
        feasts = FeastDays.find_feast_days(year_starts[2024], new_moon_list)
        atonement_dates = [d.date() for d, f in feasts.items() if 'Atonement' in f.name]
        assert dt.date(2024, 9, 11) in atonement_dates

    def test_tabernacles_2024_start(self, year_starts, full_new_moons):
        """Feast of Tabernacles 2024 should start September 16."""
        new_moon_list = list(full_new_moons.keys())
        feasts = FeastDays.find_feast_days(year_starts[2024], new_moon_list)
        tabernacles_dates = sorted([d.date() for d, f in feasts.items() if 'Tabernacles' in f.name])
        assert tabernacles_dates[0] == dt.date(2024, 9, 16)

    def test_tabernacles_2024_end(self, year_starts, full_new_moons):
        """Feast of Tabernacles 2024 should end September 23."""
        new_moon_list = list(full_new_moons.keys())
        feasts = FeastDays.find_feast_days(year_starts[2024], new_moon_list)
        tabernacles_dates = sorted([d.date() for d, f in feasts.items() if 'Tabernacles' in f.name])
        assert tabernacles_dates[-1] == dt.date(2024, 9, 23)

    def test_hanukkah_2024_start(self, year_starts, full_new_moons):
        """Hanukkah 2024 should start November 24."""
        new_moon_list = list(full_new_moons.keys())
        feasts = FeastDays.find_feast_days(year_starts[2024], new_moon_list)
        hanukkah_dates = sorted([d.date() for d, f in feasts.items() if 'Hanukkah' in f.name])
        assert hanukkah_dates[0] == dt.date(2024, 11, 24)

    def test_hanukkah_2024_end(self, year_starts, full_new_moons):
        """Hanukkah 2024 should end December 1."""
        new_moon_list = list(full_new_moons.keys())
        feasts = FeastDays.find_feast_days(year_starts[2024], new_moon_list)
        hanukkah_dates = sorted([d.date() for d, f in feasts.items() if 'Hanukkah' in f.name])
        assert hanukkah_dates[-1] == dt.date(2024, 12, 1)


class TestNewMoonSabbaths:
    """Test that new moon Sabbaths are correctly identified."""

    def test_new_moons_are_sabbaths(self, calculated_new_moons):
        """Every new moon should also be a Sabbath in this calendar system."""
        from moon import enumerate_sabbaths
        new_moon_dates = list(calculated_new_moons.keys())
        sabbath_dates = enumerate_sabbaths(new_moon_dates)

        for nm in new_moon_dates:
            assert nm in sabbath_dates, f"New moon {nm} should be a Sabbath"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
