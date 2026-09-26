from datetime import date, timedelta
from icalendar import Calendar, Event

from aztec_calc import get_tonal_day, is_trecena_start, get_trecena_info
from astro_calc import OBSERVERS, get_day_astro


START_DATE = date(2026, 1, 1)
END_DATE = date(2026, 12, 31)

CITIES = [
    "seattle", "san_francisco", "mexico_city", "guadalajara",
    "dc", "philadelphia", "boston",
]


def make_all_day_event(summary: str, day: date, description: str = "") -> Event:
    event = Event()
    event.add("summary", summary)
    event.add("dtstart", day)
    event.add("dtend", day + timedelta(days=1))
    if description:
        event.add("description", description)
    return event


def build_description(astro: dict, tonal_label: str, trecena_name: str, day_of_trecena: int) -> str:
    sc = astro["solar_cycle"]
    return (
        f"Trecena: {trecena_name}\n"
        f"Tonal: {tonal_label}\n"
        f"Day {day_of_trecena} of 13\n"
        f"\n"
        f"Solar cycle:\n"
        f"  {sc['since_equinox']:>3} days since {sc['last_equinox_name']} "
        f"({sc['last_equinox_date']})\n"
        f"  {sc['until_equinox']:>3} days until {sc['next_equinox_name']} "
        f"({sc['next_equinox_date']})\n"
        f"  {sc['since_solstice']:>3} days since {sc['last_solstice_name']} "
        f"({sc['last_solstice_date']})\n"
        f"  {sc['until_solstice']:>3} days until {sc['next_solstice_name']} "
        f"({sc['next_solstice_date']})\n"
        f"\n"
        f"Sun rise: {astro['sun_rise']}\n"
        f"Sun set:  {astro['sun_set']}\n"
        f"Day length: {astro['day_length']} ({astro['day_length_trend']})\n"
        f"\n"
        f"Moon:     {astro['moon_phase']}\n"
        f"Moon sign (tropical): {astro['moon_sign_tropical']}\n"
        f"Moon sign (vedic):    {astro['moon_sign_vedic']}\n"
        f"Moon rise: {astro['moon_rise']}\n"
        f"Moon set:  {astro['moon_set']}\n"
        f"\n"
        f"Venus:     {astro['venus_visibility']}\n"
        f"Venus rise: {astro['venus_rise']}\n"
        f"Venus set:  {astro['venus_set']}"
    )

def generate_calendar(observer_key: str, start: date, end: date) -> Calendar:
    observer = OBSERVERS[observer_key]

    cal = Calendar()
    cal.add("prodid", f"-//Tonalpohualli {observer.name}//EN")
    cal.add("version", "2.0")
    cal.add("x-wr-calname", f"Tonalpohualli - {observer.name}")

    current = start
    while current <= end:
        num, name, name_en = get_tonal_day(current)
        tonal_label = f"{num} {name} ({name_en})"

        trecena_start, trecena_name, trecena_name_en = get_trecena_info(current)
        day_of_trecena = (current - trecena_start).days + 1

        trecena_label = f"{trecena_name} ({trecena_name_en})"

        astro = get_day_astro(observer, current)
        description = build_description(astro, tonal_label, trecena_label, day_of_trecena)

        cal.add_component(
            make_all_day_event(f"Tonal: {tonal_label}", current, description)
        )

        if is_trecena_start(num):
            cal.add_component(
                make_all_day_event(f"Trecena begins: {trecena_label}", current)
            )

        current += timedelta(days=1)

    return cal


if __name__ == "__main__":
    for key in CITIES:
        cal = generate_calendar(key, START_DATE, END_DATE)
        observer = OBSERVERS[key]
        filename = f"Tonalpohualli - {observer.name}.ics"
        with open(filename, "wb") as f:
            f.write(cal.to_ical())
        print(f"Wrote {filename}")