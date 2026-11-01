"""criteria.py - the operational fuel requirement.

Required fuel = taxi + trip + contingency + alternate + final reserve.
The total is rounded UP to a whole kg so rounding never understates it.
Assumption: the alternate leg is flown in still air at cruise speed.
"""
import math

import config
import fuel_calc


def required_fuel(f, calc):
    """Return each fuel component and the total required, as a dictionary."""
    taxi = config.TAXI_FUEL_KG
    trip = calc["trip_fuel_kg"]
    contingency = config.CONTINGENCY_FRACTION * trip
    alternate = fuel_calc.fuel_burn(f["alternate_km"] / f["tas_kph"], f["burn_rate_kgph"])
    hold_rate = f["burn_rate_kgph"] * config.HOLD_BURN_FACTOR
    reserve = fuel_calc.fuel_burn(config.FINAL_RESERVE_MIN / 60, hold_rate)
    return {
        "taxi_kg": taxi,
        "trip_kg": trip,
        "contingency_kg": contingency,
        "alternate_kg": alternate,
        "reserve_kg": reserve,
        "total_kg": math.ceil(taxi + trip + contingency + alternate + reserve),
    }
