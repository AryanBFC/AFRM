"""validator.py - range and unit checks, run before any calculation."""
import config


def validate_flight(f):
    """Return a list of error messages. An empty list means the flight is valid."""
    errors = []
    for name, (low, high) in config.LIMITS.items():
        if not low <= f[name] <= high:
            errors.append(f"{name}={f[name]} outside {low} to {high}")
    if f["fuel_onboard_kg"] < 0:
        errors.append("fuel_onboard_kg is negative")
    if f["fuel_onboard_kg"] > f["fuel_capacity_kg"]:
        errors.append("fuel_onboard_kg exceeds fuel capacity")
    if f["tas_kph"] - f["wind_kph"] < config.MIN_GROUND_SPEED_KPH:
        errors.append("ground speed too low")
    return errors


def validate_all(flights):
    """Split flights into (valid, rejected). Rejected holds (flight, errors) pairs."""
    valid = []
    rejected = []
    for f in flights:
        errors = validate_flight(f)
        if errors:
            rejected.append((f, errors))
        else:
            valid.append(f)
    return valid, rejected
