"""data_generator.py - seeded simulated flight and fuel data.

Each flight is a dictionary. A fixed seed makes every run repeatable.
"""
import random

import config

AIRPORTS = ["EGLL", "EGCC", "EGPH", "LFPG", "EHAM", "EDDF", "LEMD", "LIRF", "EIDW", "ENGM"]


def generate_flights(n=config.NUM_FLIGHTS, seed=config.SEED, add_faults=True):
    """Return a list of n simulated flights (plus 3 faulty ones if add_faults)."""
    rng = random.Random(seed)
    flights = []
    for i in range(1, n + 1):
        origin, destination = rng.sample(AIRPORTS, 2)
        distance = round(rng.uniform(300, 2000))

        # Simulated fuel load: rough distance-based estimate, varied by 0.85-1.20.
        estimate = distance / config.CRUISE_TAS_KPH * config.CRUISE_BURN_KGPH + 1500
        onboard = min(estimate * rng.uniform(0.85, 1.20), config.FUEL_CAPACITY_KG)

        flights.append({
            "flight_id": f"AF{100 + i}",
            "origin": origin,
            "destination": destination,
            "distance_km": distance,
            "alternate_km": round(rng.uniform(60, 400)),
            "tas_kph": config.CRUISE_TAS_KPH,
            "wind_kph": round(rng.uniform(-80, 80)),
            "burn_rate_kgph": config.CRUISE_BURN_KGPH,
            "fuel_capacity_kg": config.FUEL_CAPACITY_KG,
            "fuel_onboard_kg": round(onboard),
        })

    if add_faults and flights:
        first = flights[0]
        flights.append(dict(first, flight_id="AF901", fuel_onboard_kg=-50))    # negative fuel
        flights.append(dict(first, flight_id="AF902", fuel_onboard_kg=9000))   # over capacity
        flights.append(dict(first, flight_id="AF903", tas_kph=0, wind_kph=0))  # zero speed
    return flights
