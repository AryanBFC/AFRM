"""fuel_calc.py - burn, endurance and range.
"""
import config


def ground_speed(tas, headwind):
    """A tailwind is a negative headwind, so it increases ground speed."""
    return tas - headwind


def fuel_burn(time_h, burn_rate):
    return time_h * burn_rate


def calculate(f):
    """Return trip fuel, endurance and range for one flight as a dictionary."""
    gs = ground_speed(f["tas_kph"], f["wind_kph"])
    trip_time = f["distance_km"] / gs
    usable_fuel = max(f["fuel_onboard_kg"] - config.TAXI_FUEL_KG, 0)
    endurance = usable_fuel / f["burn_rate_kgph"]
    return {
        "ground_speed_kph": gs,
        "trip_fuel_kg": fuel_burn(trip_time, f["burn_rate_kgph"]),
        "endurance_h": endurance,
        "range_km": endurance * gs,
    }
