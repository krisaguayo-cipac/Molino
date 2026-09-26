from datetime import date, timedelta

# The 20 day-names (tonal) of the Tonalpohualli in traditional order.
DAY_NAMES = [
    "Cipactli", "Ehecatl", "Calli", "Cuetzpalin", "Coatl",
    "Miquiztli", "Mazatl", "Tochtli", "Atl", "Itzcuintli",
    "Ozomahtli", "Malinalli", "Acatl", "Ocelotl", "Cuauhtli",
    "Cozcacuauhtli", "Ollin", "Tecpatl", "Quiahuitl", "Xochitl",
]

DAY_NAMES_EN = {
    "Cipactli":      "Crocodile",
    "Ehecatl":       "Wind",
    "Calli":         "House",
    "Cuetzpalin":    "Lizard",
    "Coatl":         "Serpent",
    "Miquiztli":     "Death",
    "Mazatl":        "Deer",
    "Tochtli":       "Rabbit",
    "Atl":           "Water",
    "Itzcuintli":    "Dog",
    "Ozomahtli":     "Monkey",
    "Malinalli":     "Grass",
    "Acatl":         "Reed",
    "Ocelotl":       "Jaguar",
    "Cuauhtli":      "Eagle",
    "Cozcacuauhtli": "Vulture",
    "Ollin":         "Movement",
    "Tecpatl":       "Flint",
    "Quiahuitl":     "Rain",
    "Xochitl":       "Flower",
}

# Caso correlation: 1 Coatl = August 13, 1521 (Julian) = August 23, 1521 (Gregorian)
CORRELATION_DATE = date(1521, 8, 23)
CORRELATION_NAME_INDEX = 4   # Coatl


def get_tonal_day(gregorian_date: date) -> tuple[int, str, str]:
    """Return (number, nahuatl_name, english_name) for a Gregorian date."""
    days_since = (gregorian_date - CORRELATION_DATE).days
    number = (days_since % 13) + 1
    name_index = (days_since % 20 + CORRELATION_NAME_INDEX) % 20
    nahuatl = DAY_NAMES[name_index]
    english = DAY_NAMES_EN[nahuatl]
    return number, nahuatl, english


def is_trecena_start(number: int) -> bool:
    """A trecena always begins on a '1' day."""
    return number == 1


def get_trecena_info(gregorian_date: date) -> tuple[date, str, str]:
    """Return (start_date, nahuatl_name, english_name) for the trecena."""
    num, _, _ = get_tonal_day(gregorian_date)
    days_into = num - 1
    start = date.fromordinal(gregorian_date.toordinal() - days_into)
    _, start_nahuatl, start_english = get_tonal_day(start)
    return start, start_nahuatl, start_english