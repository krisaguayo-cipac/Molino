---
layout: default
title: Tonalpohualli Calendar
description: A location-aware Aztec calendar that integrates Mesoamerican calendrics with modern positional astronomy.
status: Active
---

# Tonalpohualli Calendar

This project generates `.ics` calendar files for the Aztec *tonalpohualli* — the 260-day ritual count — for seven cities across North America. Each day's entry includes the tonal (day-sign), trecena, and a full astronomical almanac: sun rise and set, moon phase and zodiac position, Venus visibility, and solar cycle tracking.

## What it does

- Computes the Aztec day-sign using the Caso correlation
- Calculates sun, moon, and Venus rise/set times for any observer location
- Tracks the moon's tropical and Vedic zodiac signs
- Outputs an importable `.ics` file for macOS Calendar, Google Calendar, or any iCal client

## Why it matters

The tonalpohualli was systematically suppressed during the colonial period. This project restores it as a lived, daily practice — not as a museum piece, but as a working calendar that runs alongside the Gregorian one.

## Source Code

The Python scripts that generate these calendars:

- [aztec_calc.py](/tonalpohualli/python/aztec_calc.py) — Tonalpohualli day-sign calculation (Caso correlation)
- [astro_calc.py](/tonalpohualli/python/astro_calc.py) — Skyfield-based rise/set, moon phase, moon sign, and season tracking
- [generate_ics.py](/tonalpohualli/python/generate_ics.py) — Builds the `.ics` files for each location

## Download Calendars

Each calendar is an `.ics` file you can import into macOS Calendar, Google Calendar, or any iCal-compatible app.

- [Tonalpohualli — Seattle](/tonalpohualli/calendars/tonalpohualli-seattle.ics)
- [Tonalpohualli — San Francisco](/tonalpohualli/calendars/tonalpohualli-san-francisco.ics)
- [Tonalpohualli — Mexico City](/tonalpohualli/calendars/tonalpohualli-mexico-city.ics)
- [Tonalpohualli — Guadalajara](/tonalpohualli/calendars/tonalpohualli-guadalajara.ics)
- [Tonalpohualli — Washington DC](/tonalpohualli/calendars/tonalpohualli-washington-dc.ics)
- [Tonalpohualli — Philadelphia](/tonalpohualli/calendars/tonalpohualli-philadelphia.ics)
- [Tonalpohualli — Boston](/tonalpohualli/calendars/tonalpohualli-boston.ics)
