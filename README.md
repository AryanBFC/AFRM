# AFRM prototype (simulated data - not for operational use)

    python -m venv .venv
    # Windows: .venv\Scripts\activate    macOS/Linux: source .venv/bin/activate
    python main.py                 # run
    python -m unittest -v          # run the 9 verification tests

Outputs are written to `output/` (afrm_results.csv, afrm_log.txt).

List of flight and fuel terms:
    AFRM: Aircraft Fuel and Range Management, the name of the project.

    TAS: True Airspeed, the aircraft’s speed through the air. I use 800 km/h.

    GS / ground speed: speed over the ground. In the code it is TAS minus headwind.

    Headwind / tailwind: wind blowing against or with the aircraft. In the code a tailwind is a negative headwind, so it increases ground speed.

    kg, km, kph, h: kilograms, kilometres, kilometres per hour, hours.

    kgph: kilograms per hour, the fuel burn rate. For example, burn_rate_kgph is 1800.

    Alternate: a backup airport the aircraft could divert to. alternate_km is the distance to it.

    Contingency: extra fuel (5% of trip fuel) for unexpected deviations.

    Final reserve: the last fuel that should never be used, equal to 30 minutes of holding.

    Holding: circling in a fixed area while waiting to land, which burns less fuel than cruise.

    Endurance: how long the fuel on board will last, in hours

    ICAO: International Civil Aviation Organization. Annex 6 is its standard for aircraft operations, including fuel planning.
