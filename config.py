"""config.py - all assumptions in one place.

Units: fuel in kg, distance in km, speed in km/h, time in hours.
"""

# Simulated aircraft
FUEL_CAPACITY_KG = 6000
CRUISE_TAS_KPH = 800
CRUISE_BURN_KGPH = 1800      # constant cruise fuel flow
HOLD_BURN_FACTOR = 0.85      # holding burn as a fraction of cruise burn

# Operational criteria
TAXI_FUEL_KG = 150
CONTINGENCY_FRACTION = 0.05  # 5% of trip fuel
FINAL_RESERVE_MIN = 30       # minutes of holding fuel
MARGIN_BAND = 0.05           # surplus below 5% of required fuel = MARGINAL

# Validation limits (min, max)
LIMITS = {
    "distance_km": (50, 3000),
    "alternate_km": (20, 600),
    "tas_kph": (300, 950),
    "wind_kph": (-150, 150),
    "burn_rate_kgph": (500, 4000),
}
MIN_GROUND_SPEED_KPH = 200

# Data generation
SEED = 42
NUM_FLIGHTS = 20
OUTPUT_DIR = "output"
