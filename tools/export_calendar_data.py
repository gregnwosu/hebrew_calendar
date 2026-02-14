#!/usr/bin/env python3
"""Export precomputed Hebrew Calendar data as JSON for the Flutter app.

Reuses moon.py to generate identical data to the web app, bundled as a
static asset so the Flutter app needs no astronomy library at runtime.
"""

import datetime as dt
import json
import sys
from pathlib import Path

# Add project root to path so we can import moon / scriptures
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from moon import (
    FeastDays,
    enumerate_new_moons,
    enumerate_sabbaths,
    get_lunar_year_starts,
    get_moon_phase,
)
from scriptures import SCRIPTURE_TEXT

# Date range to export
START = dt.datetime(2024, 1, 1)
END = dt.datetime(2028, 1, 1)
YEAR_START = 2024
YEAR_END = 2027


def _date_str(d):
    """Normalise datetime/date to ISO date string."""
    if isinstance(d, dt.datetime):
        return d.strftime("%Y-%m-%d")
    return d.isoformat()


def main():
    print("Computing new moons …")
    raw_moons = enumerate_new_moons(START, END)
    new_moon_list = list(raw_moons.keys())
    sorted_moon_dates = sorted(raw_moons.keys())

    print("Computing sabbaths …")
    sabbath_list = enumerate_sabbaths(sorted_moon_dates)

    print("Computing lunar year starts …")
    year_starts = get_lunar_year_starts(raw_moons, YEAR_START, YEAR_END)

    print("Computing feast days …")
    feast_dates = {}
    for y, start in year_starts.items():
        raw = FeastDays.find_feast_days(start, new_moon_list)
        for k, v in raw.items():
            d = k.date() if isinstance(k, dt.datetime) else k
            feast_dates[d] = v

    new_year_dates = {
        (d.date() if isinstance(d, dt.datetime) else d) for d in year_starts.values()
    }

    print("Computing daily moon phases …")
    days = {}
    current = START.date()
    end_date = END.date()
    while current < end_date:
        noon = dt.datetime.combine(current, dt.time(12, 0))
        phase, angle = get_moon_phase(noon)

        day_data = {
            "phase": phase,
            "angle": round(angle, 2),
        }

        nm_date = current
        if nm_date in {
            (k.date() if isinstance(k, dt.datetime) else k) for k in raw_moons
        }:
            day_data["isNewMoon"] = True
            # Find the angle from raw_moons
            for k, v in raw_moons.items():
                kd = k.date() if isinstance(k, dt.datetime) else k
                if kd == current:
                    day_data["newMoonAngle"] = round(v, 2)
                    break

        sabbath_date_set = {
            (d.date() if isinstance(d, dt.datetime) else d) for d in sabbath_list
        }
        if current in sabbath_date_set:
            day_data["isSabbath"] = True

        if current in new_year_dates:
            day_data["isNewYear"] = True

        if current in feast_dates:
            feast = feast_dates[current]
            day_data["feast"] = {
                "name": feast.name,
                "description": feast.description,
                "bibleRefs": feast.bible_refs or [],
            }

        days[current.isoformat()] = day_data
        current += dt.timedelta(days=1)

    # Build the output
    output = {
        "generatedAt": dt.datetime.now().isoformat(),
        "dateRange": {
            "start": START.date().isoformat(),
            "end": (END.date() - dt.timedelta(days=1)).isoformat(),
        },
        "newMoons": [
            {"date": _date_str(k), "angle": round(v, 2)}
            for k, v in sorted(raw_moons.items())
        ],
        "sabbaths": sorted(_date_str(d) for d in sabbath_list),
        "newYears": sorted(_date_str(d) for d in year_starts.values()),
        "scriptures": SCRIPTURE_TEXT,
        "days": days,
    }

    # Write JSON
    out_dir = Path(__file__).resolve().parent.parent / "flutter" / "assets"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "calendar_data.json"

    with open(out_path, "w") as f:
        json.dump(output, f, separators=(",", ":"))

    size_mb = out_path.stat().st_size / (1024 * 1024)
    print(f"Wrote {out_path} ({size_mb:.1f} MB)")
    print(f"  {len(days)} days, {len(output['newMoons'])} new moons, "
          f"{len(output['sabbaths'])} sabbaths, {len(output['newYears'])} new years")


if __name__ == "__main__":
    main()
