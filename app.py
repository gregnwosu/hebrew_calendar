import calendar
import datetime as dt
from dash import Dash, html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
from moon import FeastDays, enumerate_sabbaths, enumerate_new_moons, get_moon_phase

# Initialize the app with Bootstrap styling
app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
server = app.server  # For deployment

# Calculate feast days and moon data
LUNAR_YEAR_START = dt.datetime(2024, 2, 9)
FEAST_DATES = FeastDays.find_feast_days(LUNAR_YEAR_START)
NEW_MOON_DATES = enumerate_new_moons(LUNAR_YEAR_START, LUNAR_YEAR_START + dt.timedelta(days=400))
SABBATH_DATES = enumerate_sabbaths(list(NEW_MOON_DATES.keys()))

def get_day_style(day_date):
    """Return CSS style based on the type of day."""
    if day_date in NEW_MOON_DATES:
        return {"backgroundColor": "#17a2b8", "color": "white", "borderRadius": "50%"}
    if day_date in SABBATH_DATES:
        return {"backgroundColor": "#0d6efd", "color": "white", "borderRadius": "4px"}
    if day_date in FEAST_DATES:
        return {"backgroundColor": "#198754", "color": "white", "borderRadius": "4px"}
    return {}

def create_calendar_grid(year, month, selected_day):
    """Generate the calendar grid for a given month."""
    cal = calendar.monthcalendar(year, month)
    weekdays = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]

    header = html.Tr([html.Th(d, style={"textAlign": "center", "padding": "10px"}) for d in weekdays])

    rows = [header]
    for week in cal:
        cells = []
        for day in week:
            if day == 0:
                cells.append(html.Td("", style={"padding": "10px"}))
            else:
                day_date = dt.date(year, month, day)
                style = get_day_style(day_date)
                style.update({
                    "textAlign": "center",
                    "padding": "10px",
                    "cursor": "pointer",
                    "width": "40px",
                    "height": "40px"
                })
                if day == selected_day:
                    style["border"] = "2px solid #ffc107"
                cells.append(html.Td(str(day), style=style))
        rows.append(html.Tr(cells))

    return html.Table(rows, style={"width": "100%", "borderCollapse": "collapse"})

def get_day_info(day_date):
    """Get information about a specific day."""
    info = []
    if day_date in NEW_MOON_DATES:
        angle = NEW_MOON_DATES[day_date]
        info.append(html.P(f"New Moon (phase angle: {angle:.1f})", style={"color": "#17a2b8"}))
    if day_date in SABBATH_DATES:
        info.append(html.P("Sabbath", style={"color": "#0d6efd"}))
    if day_date in FEAST_DATES:
        feast = FEAST_DATES[day_date]
        info.append(html.Div([
            html.H5(feast.name, style={"color": "#198754"}),
            html.P(feast.description) if feast.description else None,
            html.Small(f"Reference: {feast.bible_ref}") if feast.bible_ref else None
        ]))
    if not info:
        phase, angle = get_moon_phase(dt.datetime.combine(day_date, dt.time(12, 0)))
        info.append(html.P(f"Moon phase: {phase} ({angle:.1f})"))
    return info

# Build initial calendar
today = dt.date.today()
initial_grid = create_calendar_grid(today.year, today.month, today.day)
initial_month = today.strftime("%B %Y")
initial_info = get_day_info(today)

# Layout
app.layout = dbc.Container([
    html.H1("Hebrew Calendar", className="text-center my-4"),
    html.P("Biblical feast days, sabbaths, and new moons based on lunar calculations",
           className="text-center text-muted mb-4"),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    dbc.Button("<", id="prev-month", color="secondary", size="sm", className="me-2"),
                    html.Span(initial_month, id="month-year", className="mx-3"),
                    dbc.Button(">", id="next-month", color="secondary", size="sm", className="ms-2"),
                ], className="d-flex justify-content-center align-items-center"),
                dbc.CardBody(initial_grid, id="calendar-grid")
            ])
        ], md=7),

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
                        html.Span("", style={"backgroundColor": "#17a2b8", "padding": "5px 15px", "borderRadius": "50%", "marginRight": "10px"}),
                        html.Span("New Moon")
                    ], className="mb-2"),
                    html.Div([
                        html.Span("", style={"backgroundColor": "#0d6efd", "padding": "5px 15px", "borderRadius": "4px", "marginRight": "10px"}),
                        html.Span("Sabbath")
                    ], className="mb-2"),
                    html.Div([
                        html.Span("", style={"backgroundColor": "#198754", "padding": "5px 15px", "borderRadius": "4px", "marginRight": "10px"}),
                        html.Span("Feast Day")
                    ])
                ])
            ])
        ], md=5)
    ]),

    # Store for current date
    dcc.Store(id="current-date", data={"year": today.year, "month": today.month, "day": today.day})
], fluid=True, className="py-4")

@callback(
    [Output("calendar-grid", "children"),
     Output("month-year", "children"),
     Output("day-info", "children"),
     Output("current-date", "data")],
    [Input("prev-month", "n_clicks"),
     Input("next-month", "n_clicks")],
    [State("current-date", "data")],
    prevent_initial_call=True
)
def update_calendar(prev_clicks, next_clicks, date_data):
    from dash import ctx

    year = date_data["year"]
    month = date_data["month"]
    day = date_data["day"]

    triggered = ctx.triggered_id
    if triggered == "prev-month":
        month -= 1
        if month < 1:
            month = 12
            year -= 1
    elif triggered == "next-month":
        month += 1
        if month > 12:
            month = 1
            year += 1

    day = 1
    cal_grid = create_calendar_grid(year, month, day)
    month_name = dt.date(year, month, 1).strftime("%B %Y")
    day_info = get_day_info(dt.date(year, month, day))

    return cal_grid, month_name, day_info, {"year": year, "month": month, "day": day}

if __name__ == "__main__":
    app.run(debug=True)
