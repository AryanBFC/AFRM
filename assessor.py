"""assessor.py - compares fuel on board with fuel required and sets a status."""
import config


def classify(margin, required):
    """Below 0 = INSUFFICIENT, 0 up to 5% of required = MARGINAL, otherwise SUFFICIENT."""
    if margin < 0:
        return "INSUFFICIENT"
    if margin < config.MARGIN_BAND * required:
        return "MARGINAL"
    return "SUFFICIENT"


def assess(f, calc, req):
    """Return one result dictionary for the report."""
    margin = f["fuel_onboard_kg"] - req["total_kg"]
    return {
        "flight_id": f["flight_id"],
        "onboard_kg": f["fuel_onboard_kg"],
        "required_kg": req["total_kg"],
        "margin_kg": margin,
        "margin_pct": 100 * margin / req["total_kg"],
        "range_km": calc["range_km"],
        "endurance_h": calc["endurance_h"],
        "status": classify(margin, req["total_kg"]),
        "breakdown": req,
    }
