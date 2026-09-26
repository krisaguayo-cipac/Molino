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

## Subscribe to Calendars

Each calendar is available as a live subscription. Click the link for your city to automatically add it to your calendar app (Apple Calendar, Outlook, etc.).

- [Tonalpohualli — Seattle](webcal://www.molino.digital/tonalpohualli/calendars/tonalpohualli-seattle.ics)
- [Tonalpohualli — San Francisco](webcal://www.molino.digital/tonalpohualli/calendars/tonalpohualli-san-francisco.ics)
- [Tonalpohualli — Mexico City](webcal://www.molino.digital/tonalpohualli/calendars/tonalpohualli-mexico-city.ics)
- [Tonalpohualli — Guadalajara](webcal://www.molino.digital/tonalpohualli/calendars/tonalpohualli-guadalajara.ics)
- [Tonalpohualli — Washington DC](webcal://www.molino.digital/tonalpohualli/calendars/tonalpohualli-washington-dc.ics)
- [Tonalpohualli — Philadelphia](webcal://www.molino.digital/tonalpohualli/calendars/tonalpohualli-philadelphia.ics)
- [Tonalpohualli — Boston](webcal://www.molino.digital/tonalpohualli/calendars/tonalpohualli-boston.ics)
