import calendar
import datetime as dt
from dash import Dash, html, dcc, callback, Output, Input, State, ALL, ctx, clientside_callback
import dash_bootstrap_components as dbc
from moon import FeastDays, enumerate_sabbaths, enumerate_new_moons, get_moon_phase, get_lunar_year_starts
from scriptures import SCRIPTURE_TEXT

# Initialize the app with Bootstrap styling
app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
server = app.server  # For deployment


# ---------------------------------------------------------------------------
# Pre-compute lunar data for 2024-2028
# ---------------------------------------------------------------------------

def _normalise_date(d):
    return d.date() if isinstance(d, dt.datetime) else d


MOON_EMOJI = {
    "New Moon":        "\U0001F311",   # 🌑
    "Waxing Crescent": "\U0001F312",   # 🌒
    "First Quarter":   "\U0001F313",   # 🌓
    "Waxing Gibbous":  "\U0001F314",   # 🌔
    "Full Moon":       "\U0001F315",   # 🌕
    "Waning Gibbous":  "\U0001F316",   # 🌖
    "Third Quarter":   "\U0001F317",   # 🌗
    "Waning Crescent": "\U0001F318",   # 🌘
}

FEAST_EMOJI = "\U0001F389"   # 🎉
SABBATH_EMOJI = "\U0001F54A\uFE0F"  # 🕊️
NEW_YEAR_EMOJI = "\U0001F387"  # 🎇


def _build_data():
    """Compute new moons, sabbaths and feast days for multiple lunar years."""
    raw_moons = enumerate_new_moons(dt.datetime(2024, 1, 1), dt.datetime(2028, 1, 1))
    new_moon_dates = {_normalise_date(k): v for k, v in raw_moons.items()}

    sabbath_list = enumerate_sabbaths(list(raw_moons.keys()))
    sabbath_dates = {_normalise_date(d) for d in sabbath_list}

    year_starts = get_lunar_year_starts(raw_moons, 2024, 2027)
    new_moon_list = list(raw_moons.keys())

    feast_dates = {}
    for y, start in year_starts.items():
        raw = FeastDays.find_feast_days(start, new_moon_list)
        for k, v in raw.items():
            feast_dates[_normalise_date(k)] = v

    new_year_dates = {_normalise_date(d) for d in year_starts.values()}

    return new_moon_dates, sabbath_dates, feast_dates, new_year_dates


NEW_MOON_DATES, SABBATH_DATES, FEAST_DATES, NEW_YEAR_DATES = _build_data()


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def get_moon_emoji(day_date):
    """Return moon phase emoji for a given date."""
    phase, _ = get_moon_phase(dt.datetime.combine(day_date, dt.time(12, 0)))
    return MOON_EMOJI.get(phase, "")


def get_day_badges(day_date):
    """Return list of emoji badges for a calendar day."""
    badges = []
    if day_date in NEW_YEAR_DATES:
        badges.append(NEW_YEAR_EMOJI)
    if day_date in FEAST_DATES:
        badges.append(FEAST_EMOJI)
    if day_date in SABBATH_DATES:
        badges.append(SABBATH_EMOJI)
    return badges


def create_calendar_grid(year, month, selected_day):
    """Generate the calendar grid for a given month."""
    cal = calendar.monthcalendar(year, month)
    weekdays = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]

    header = html.Tr([
        html.Th(d, style={"textAlign": "center", "padding": "8px 4px", "fontWeight": "bold", "fontSize": "0.85rem"})
        for d in weekdays
    ])

    rows = [header]
    for week in cal:
        cells = []
        for day in week:
            if day == 0:
                cells.append(html.Td("", style={"padding": "4px", "minWidth": "50px", "minHeight": "55px"}))
            else:
                day_date = dt.date(year, month, day)
                moon_em = get_moon_emoji(day_date)
                badges = get_day_badges(day_date)
                badge_str = " ".join(badges)

                style = {
                    "textAlign": "center",
                    "padding": "4px 2px",
                    "cursor": "pointer",
                    "minWidth": "50px",
                    "minHeight": "55px",
                    "verticalAlign": "top",
                    "userSelect": "none",
                    "borderRadius": "6px",
                }
                if day == selected_day:
                    style["border"] = "2px solid #ffc107"
                    style["backgroundColor"] = "rgba(255, 193, 7, 0.15)"

                cell_children = [
                    html.Div(str(day), style={"fontSize": "0.95rem", "fontWeight": "bold" if day == selected_day else "normal"}),
                    html.Div(moon_em, style={"fontSize": "1.1rem", "lineHeight": "1"}),
                ]
                if badge_str:
                    cell_children.append(
                        html.Div(badge_str, style={"fontSize": "0.75rem", "lineHeight": "1"})
                    )

                cells.append(html.Td(
                    cell_children,
                    style=style,
                    id={"type": "day-cell", "day": day},
                    n_clicks=0,
                ))
        rows.append(html.Tr(cells))

    return html.Table(rows, style={"width": "100%", "borderCollapse": "collapse"})


def get_day_info(day_date):
    """Get information about a specific day."""
    phase, angle = get_moon_phase(dt.datetime.combine(day_date, dt.time(12, 0)))
    moon_em = MOON_EMOJI.get(phase, "")

    info = [html.H6(day_date.strftime("%A, %d %B %Y"), className="mb-3")]
    info.append(html.P(f"{moon_em} {phase} (angle: {angle:.1f}°)", style={"fontSize": "1.1rem"}))

    if day_date in NEW_YEAR_DATES:
        info.append(html.P(
            f"{NEW_YEAR_EMOJI} Nisan 1 — Head of the Year (Rosh HaShanah)",
            style={"color": "#ffc107", "fontWeight": "bold", "fontSize": "1.1rem"}
        ))
    if day_date in NEW_MOON_DATES:
        info.append(html.P(
            f"\U0001F311 New Moon — start of lunar month",
            style={"color": "#17a2b8", "fontWeight": "bold"}
        ))
    if day_date in SABBATH_DATES:
        info.append(html.P(
            f"{SABBATH_EMOJI} Sabbath — day of rest",
            style={"color": "#6ea8fe"}
        ))
    if day_date in FEAST_DATES:
        feast = FEAST_DATES[day_date]
        children = [html.H5(f"{FEAST_EMOJI} {feast.name}", style={"color": "#75b798"})]
        if feast.description:
            children.append(html.P(feast.description))
        if feast.bible_refs:
            children.append(dbc.Accordion(
                [dbc.AccordionItem(
                    html.P(SCRIPTURE_TEXT.get(ref, ""), style={"whiteSpace": "pre-wrap"}),
                    title=ref,
                ) for ref in feast.bible_refs],
                start_collapsed=True,
                always_open=True,
                flush=True,
                className="mt-2",
            ))
        info.append(html.Div(children))
    return info


# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------

today = dt.date.today()
initial_grid = create_calendar_grid(today.year, today.month, today.day)
initial_month = today.strftime("%B %Y")
initial_info = get_day_info(today)

app.layout = dbc.Container([
    html.H1("\U0001F319 Hebrew Calendar", className="text-center my-4"),
    html.P("Biblical feast days, sabbaths, and new moons based on lunar calculations",
           className="text-center text-muted mb-2"),
    dbc.Alert(
        "\U0001F319 Feasts and Sabbaths begin at sunset on the date shown (evening to evening)",
        color="info",
        className="text-center mb-3",
        style={"fontSize": "0.9rem"}
    ),
    html.P("Click a day or use arrow keys (\u2190 \u2192 \u2191 \u2193) to navigate",
           className="text-center text-muted mb-2", style={"fontSize": "0.85rem"}),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    dbc.Button("\u25c0", id="prev-month", color="secondary", size="sm", className="me-2"),
                    html.Span(initial_month, id="month-year", className="mx-3", style={"fontSize": "1.2rem"}),
                    dbc.Button("\u25b6", id="next-month", color="secondary", size="sm", className="ms-2"),
                ], className="d-flex justify-content-center align-items-center"),
                dbc.CardBody(initial_grid, id="calendar-grid")
            ])
        ], lg=8),

        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Selected Day"),
                dbc.CardBody(initial_info, id="day-info")
            ]),
            html.Div(className="mt-3"),
            dbc.Card([
                dbc.CardHeader("Legend"),
                dbc.CardBody([
                    html.Div([
                        html.Span("\U0001F311", style={"marginRight": "8px"}),
                        "New Moon"
                    ], className="mb-2"),
                    html.Div([
                        html.Span("\U0001F313", style={"marginRight": "8px"}),
                        "First Quarter"
                    ], className="mb-2"),
                    html.Div([
                        html.Span("\U0001F315", style={"marginRight": "8px"}),
                        "Full Moon"
                    ], className="mb-2"),
                    html.Div([
                        html.Span("\U0001F317", style={"marginRight": "8px"}),
                        "Third Quarter"
                    ], className="mb-2"),
                    html.Hr(),
                    html.Div([
                        html.Span(FEAST_EMOJI, style={"marginRight": "8px"}),
                        "Feast Day"
                    ], className="mb-2"),
                    html.Div([
                        html.Span(SABBATH_EMOJI, style={"marginRight": "8px"}),
                        "Sabbath"
                    ], className="mb-2"),
                    html.Div([
                        html.Span(NEW_YEAR_EMOJI, style={"marginRight": "8px"}),
                        "New Year (Nisan 1)"
                    ]),
                ])
            ])
        ], lg=4)
    ]),

    # Stores
    dcc.Store(id="current-date", data={"year": today.year, "month": today.month, "day": today.day}),
    dcc.Store(id="key-press", data=0),
    dcc.Store(id="key-direction", data=""),
], fluid=True, className="py-4")


# ---------------------------------------------------------------------------
# Clientside JS for keyboard arrow capture
# ---------------------------------------------------------------------------

app.clientside_callback(
    """
    function(n) {
        if (!window._hcKeyBound) {
            window._hcKeyBound = true;
            document.addEventListener('keydown', function(e) {
                var dir = '';
                if (e.key === 'ArrowRight') dir = 'right';
                else if (e.key === 'ArrowLeft') dir = 'left';
                else if (e.key === 'ArrowDown') dir = 'down';
                else if (e.key === 'ArrowUp') dir = 'up';
                if (dir) {
                    e.preventDefault();
                    window.dash_clientside.set_props('key-direction', {data: dir});
                    window.dash_clientside.set_props('key-press', {data: Date.now()});
                }
            });
        }
        return window.dash_clientside.no_update;
    }
    """,
    Output("key-press", "id"),
    Input("key-press", "data"),
)


# ---------------------------------------------------------------------------
# Main callback
# ---------------------------------------------------------------------------

@callback(
    [Output("calendar-grid", "children"),
     Output("month-year", "children"),
     Output("day-info", "children"),
     Output("current-date", "data")],
    [Input("prev-month", "n_clicks"),
     Input("next-month", "n_clicks"),
     Input({"type": "day-cell", "day": ALL}, "n_clicks"),
     Input("key-press", "data")],
    [State("current-date", "data"),
     State("key-direction", "data")],
    prevent_initial_call=True,
)
def update_calendar(prev_clicks, next_clicks, day_clicks, key_ts, date_data, key_dir):
    year = date_data["year"]
    month = date_data["month"]
    day = date_data["day"]

    triggered = ctx.triggered_id

    if triggered == "prev-month":
        month -= 1
        if month < 1:
            month = 12
            year -= 1
        day = 1
    elif triggered == "next-month":
        month += 1
        if month > 12:
            month = 1
            year += 1
        day = 1
    elif isinstance(triggered, dict) and triggered.get("type") == "day-cell":
        day = triggered["day"]
    elif triggered == "key-press" and key_dir:
        current = dt.date(year, month, day)
        if key_dir == "right":
            current += dt.timedelta(days=1)
        elif key_dir == "left":
            current -= dt.timedelta(days=1)
        elif key_dir == "down":
            current += dt.timedelta(days=7)
        elif key_dir == "up":
            current -= dt.timedelta(days=7)
        year, month, day = current.year, current.month, current.day

    max_day = calendar.monthrange(year, month)[1]
    day = min(day, max_day)

    cal_grid = create_calendar_grid(year, month, day)
    month_name = dt.date(year, month, 1).strftime("%B %Y")
    day_info = get_day_info(dt.date(year, month, day))

    return cal_grid, month_name, day_info, {"year": year, "month": month, "day": day}


if __name__ == "__main__":
    app.run(debug=True)
