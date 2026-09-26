from datetime import date, datetime, timedelta
from functools import lru_cache
from zoneinfo import ZoneInfo

from skyfield.api import load, wgs84
from skyfield import almanac
from skyfield.framelib import ecliptic_frame


ts = load.timescale()
eph = load("de421.bsp")

earth = eph["earth"]
sun = eph["sun"]
moon = eph["moon"]
venus = eph["venus"]


class Observer:
    def __init__(self, slug: str, name: str, lat: float, lon: float, tz_name: str):
        self.slug = slug
        self.name = name
        self.location = wgs84.latlon(lat, lon)
        self.tz = ZoneInfo(tz_name)

    def __repr__(self):
        return f"Observer({self.name!r})"


OBSERVERS = {
    "seattle":       Observer("seattle",       "Seattle",       47.6062, -122.3321, "America/Los_Angeles"),
    "san_francisco": Observer("san_francisco", "San Francisco", 37.7749, -122.4194, "America/Los_Angeles"),
    "mexico_city":   Observer("mexico_city",   "Mexico City",   19.4326,  -99.1332, "America/Mexico_City"),
    "guadalajara":   Observer("guadalajara",   "Guadalajara",   20.6597, -103.3496, "America/Mexico_City"),
    "dc":            Observer("dc",            "Washington DC", 38.9072,  -77.0369, "America/New_York"),
    "philadelphia":  Observer("philadelphia",  "Philadelphia",  39.9526,  -75.1652, "America/New_York"),
    "boston":        Observer("boston",        "Boston",        42.3601,  -71.0589, "America/New_York"),
}


# ---------------------------------------------------------------------------
# Rise / set (cached by observer + date + body)
# ---------------------------------------------------------------------------
@lru_cache(maxsize=4096)
def _rise_set_cached(observer_name: str, body_name: str, iso_date: str):
    observer = OBSERVERS[observer_name]
    body = {"sun": sun, "moon": moon, "venus": venus}[body_name]
    gregorian_date = date.fromisoformat(iso_date)

    t0 = ts.utc(gregorian_date.year, gregorian_date.month, gregorian_date.day - 1, 12)
    t1 = ts.utc(gregorian_date.year, gregorian_date.month, gregorian_date.day + 1, 12)

    f = almanac.risings_and_settings(eph, body, observer.location)
    times, events = almanac.find_discrete(t0, t1, f)

    rise_str, set_str = "—", "—"
    for t, event in zip(times, events):
        local_dt = t.utc_datetime().astimezone(observer.tz)
        if local_dt.date() != gregorian_date:
            continue
        if event == 1:
            rise_str = local_dt.strftime("%-I:%M %p")
        else:
            set_str = local_dt.strftime("%-I:%M %p")
    return rise_str, set_str


def _rise_set(body_name: str, observer: Observer, gregorian_date: date):
    return _rise_set_cached(observer.slug, body_name, gregorian_date.isoformat())


def get_sun_rise_set(observer, gregorian_date):
    return _rise_set("sun", observer, gregorian_date)


def get_moon_rise_set(observer, gregorian_date):
    return _rise_set("moon", observer, gregorian_date)


def get_venus_rise_set(observer, gregorian_date):
    return _rise_set("venus", observer, gregorian_date)


# ---------------------------------------------------------------------------
# Day length and trend
# ---------------------------------------------------------------------------
_TIME_FMT = "%I:%M %p"


def _length_minutes(rise_str: str, set_str: str):
    if rise_str == "—" or set_str == "—":
        return None
    rise = datetime.strptime(rise_str, _TIME_FMT)
    sett = datetime.strptime(set_str, _TIME_FMT)
    return int((sett - rise).total_seconds() // 60)


def get_day_length(observer: Observer, gregorian_date: date) -> str:
    rise, sett = get_sun_rise_set(observer, gregorian_date)
    minutes = _length_minutes(rise, sett)
    if minutes is None:
        return "—"
    h, m = divmod(minutes, 60)
    return f"{h}h {m:02d}m"


def get_day_length_trend(observer: Observer, gregorian_date: date) -> str:
    today_rise, today_set = get_sun_rise_set(observer, gregorian_date)
    yest = gregorian_date - timedelta(days=1)
    yest_rise, yest_set = get_sun_rise_set(observer, yest)

    today_min = _length_minutes(today_rise, today_set)
    yest_min = _length_minutes(yest_rise, yest_set)

    if today_min is None or yest_min is None:
        return "—"

    diff = today_min - yest_min
    if diff > 0:
        return f"gaining {diff}m"
    elif diff < 0:
        return f"losing {abs(diff)}m"
    return "steady"


# ---------------------------------------------------------------------------
# Moon phase
# ---------------------------------------------------------------------------
PHASE_NAMES = {
    0: "New Moon",
    1: "First Quarter",
    2: "Full Moon",
    3: "Last Quarter",
}


def get_moon_phase(gregorian_date: date) -> tuple[str, str]:
    t0 = ts.utc(gregorian_date.year, gregorian_date.month, gregorian_date.day)
    t1 = ts.utc(gregorian_date.year, gregorian_date.month, gregorian_date.day + 1)

    f = almanac.moon_phases(eph)
    times, events = almanac.find_discrete(t0, t1, f)

    if len(events) > 0:
        return PHASE_NAMES[int(events[0])], ""

    t_noon = ts.utc(gregorian_date.year, gregorian_date.month, gregorian_date.day, 12)
    angle = almanac.moon_phase(eph, t_noon).degrees

    if angle < 45 or angle >= 315:
        return "New Moon", "Waxing"
    elif angle < 90:
        return "Waxing Crescent", ""
    elif angle < 135:
        return "First Quarter", "Waxing"
    elif angle < 180:
        return "Waxing Gibbous", ""
    elif angle < 225:
        return "Full Moon", "Waning"
    elif angle < 270:
        return "Waning Gibbous", ""
    elif angle < 315:
        return "Last Quarter", "Waning"
    return "Waning Crescent", ""


# ---------------------------------------------------------------------------
# Moon sign (Tropical and Vedic)
# ---------------------------------------------------------------------------
ZODIAC_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer",
    "Leo", "Virgo", "Libra", "Scorpio",
    "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]


def _moon_longitude(gregorian_date: date, hour: int = 12) -> float:
    t = ts.utc(gregorian_date.year, gregorian_date.month, gregorian_date.day, hour)
    e = earth.at(t)
    _, lon, _ = e.observe(moon).apparent().frame_latlon(ecliptic_frame)
    return lon.degrees


def _ayanamsa(year: int) -> float:
    return 23.85 + 0.013972 * (year - 2000)


def _sign_from_longitude(lon_deg: float) -> str:
    return ZODIAC_SIGNS[int(lon_deg // 30) % 12]


def get_moon_signs(gregorian_date: date) -> dict:
    lon_start = _moon_longitude(gregorian_date, 0)
    lon_end = _moon_longitude(gregorian_date, 23)

    trop_start = _sign_from_longitude(lon_start)
    trop_end = _sign_from_longitude(lon_end)
    tropical = trop_start if trop_start == trop_end else f"{trop_start} → {trop_end}"

    ayan = _ayanamsa(gregorian_date.year)
    sid_start = (lon_start - ayan) % 360
    sid_end = (lon_end - ayan) % 360
    vedic_start = _sign_from_longitude(sid_start)
    vedic_end = _sign_from_longitude(sid_end)
    vedic = vedic_start if vedic_start == vedic_end else f"{vedic_start} → {vedic_end}"

    return {"tropical": tropical, "vedic": vedic}


# ---------------------------------------------------------------------------
# Venus visibility
# ---------------------------------------------------------------------------
UNDERWORLD = "Venus is in the underworld (not visible)"


def get_venus_visibility(gregorian_date: date) -> str:
    t = ts.utc(gregorian_date.year, gregorian_date.month, gregorian_date.day, 12)
    e = earth.at(t)
    _, sun_lon, _ = e.observe(sun).apparent().frame_latlon(ecliptic_frame)
    _, venus_lon, _ = e.observe(venus).apparent().frame_latlon(ecliptic_frame)
    diff = (venus_lon.degrees - sun_lon.degrees + 180) % 360 - 180
    if abs(diff) < 8:
        return UNDERWORLD
    return "Morning Star" if diff < 0 else "Evening Star"


# ---------------------------------------------------------------------------
# Seasons (with caching)
# ---------------------------------------------------------------------------
SEASON_NAMES = {
    0: "Spring Equinox",
    1: "Summer Solstice",
    2: "Autumnal Equinox",
    3: "Winter Solstice",
}


@lru_cache(maxsize=16)
def _season_events_for_year(year: int):
    t0 = ts.utc(year - 1, 1, 1)
    t1 = ts.utc(year + 1, 12, 31)

    f = almanac.seasons(eph)
    times, events = almanac.find_discrete(t0, t1, f)

    return tuple(
        (t.utc_datetime().date().isoformat(), int(event))
        for t, event in zip(times, events)
    )


def _season_events(gregorian_date: date):
    raw = _season_events_for_year(gregorian_date.year)
    return [(date.fromisoformat(s), idx) for s, idx in raw]


def get_solar_position(gregorian_date: date) -> str:
    """Nearest equinox or solstice as a descriptive string."""
    season_dates = _season_events(gregorian_date)

    prev_event = None
    next_event = None
    for d, idx in season_dates:
        if d <= gregorian_date:
            prev_event = (d, idx)
        elif next_event is None:
            next_event = (d, idx)
            break

    if prev_event is None or next_event is None:
        return "—"

    days_after_prev = (gregorian_date - prev_event[0]).days
    days_until_next = (next_event[0] - gregorian_date).days

    if days_after_prev <= days_until_next:
        name = SEASON_NAMES[prev_event[1]]
        if days_after_prev == 0:
            return f"{name} (today)"
        plural = "s" if days_after_prev != 1 else ""
        return f"{days_after_prev} day{plural} after {name}"
    else:
        name = SEASON_NAMES[next_event[1]]
        if days_until_next == 0:
            return f"{name} (today)"
        plural = "s" if days_until_next != 1 else ""
        return f"{days_until_next} day{plural} until {name}"


def get_solar_cycle(gregorian_date: date) -> dict:
    season_dates = _season_events(gregorian_date)

    last_equinox = None
    next_equinox = None
    last_solstice = None
    next_solstice = None

    for d, idx in season_dates:
        is_equinox = idx in (0, 2)
        is_solstice = idx in (1, 3)

        if d <= gregorian_date:
            if is_equinox:
                last_equinox = (d, idx)
            if is_solstice:
                last_solstice = (d, idx)
        else:
            if is_equinox and next_equinox is None:
                next_equinox = (d, idx)
            if is_solstice and next_solstice is None:
                next_solstice = (d, idx)

    def days_since(pair):
        return (gregorian_date - pair[0]).days if pair else None

    def days_until(pair):
        return (pair[0] - gregorian_date).days if pair else None

    return {
        "last_equinox_name":   SEASON_NAMES[last_equinox[1]] if last_equinox else "—",
        "last_equinox_date":   last_equinox[0].isoformat() if last_equinox else "—",
        "since_equinox":       days_since(last_equinox),
        "next_equinox_name":   SEASON_NAMES[next_equinox[1]] if next_equinox else "—",
        "next_equinox_date":   next_equinox[0].isoformat() if next_equinox else "—",
        "until_equinox":       days_until(next_equinox),
        "last_solstice_name":  SEASON_NAMES[last_solstice[1]] if last_solstice else "—",
        "last_solstice_date":  last_solstice[0].isoformat() if last_solstice else "—",
        "since_solstice":      days_since(last_solstice),
        "next_solstice_name":  SEASON_NAMES[next_solstice[1]] if next_solstice else "—",
        "next_solstice_date":  next_solstice[0].isoformat() if next_solstice else "—",
        "until_solstice":      days_until(next_solstice),
    }


# ---------------------------------------------------------------------------
# Combined per-day astro
# ---------------------------------------------------------------------------
def get_day_astro(observer: Observer, gregorian_date: date) -> dict:
    sun_rise, sun_set = get_sun_rise_set(observer, gregorian_date)
    moon_rise, moon_set = get_moon_rise_set(observer, gregorian_date)
    venus_rise, venus_set = get_venus_rise_set(observer, gregorian_date)
    phase_name, phase_dir = get_moon_phase(gregorian_date)
    moon_phase_str = f"{phase_name} ({phase_dir})" if phase_dir else phase_name

    signs = get_moon_signs(gregorian_date)
    solar = get_solar_cycle(gregorian_date)

    return {
        "sun_rise": sun_rise,
        "sun_set": sun_set,
        "day_length": get_day_length(observer, gregorian_date),
        "day_length_trend": get_day_length_trend(observer, gregorian_date),
        "moon_rise": moon_rise,
        "moon_set": moon_set,
        "moon_phase": moon_phase_str,
        "moon_sign_tropical": signs["tropical"],
        "moon_sign_vedic": signs["vedic"],
        "venus_rise": venus_rise,
        "venus_set": venus_set,
        "venus_visibility": get_venus_visibility(gregorian_date),
        "solar_position": get_solar_position(gregorian_date),
        "solar_cycle": solar,
    }