"""test_afrm.py - verification tests (standard library unittest).

Hand calculation for the reference flight below
(1000 km, no wind, 800 km/h, 1800 kg/h, alternate 100 km):
  trip time 1.25 h -> trip fuel 2250 kg      contingency 5% = 112.5 kg
  alternate 100/800 h x 1800 = 225 kg        reserve 0.5 h x 1530 = 765 kg
  taxi 150 kg  ->  total 3502.5, rounded up to 3503 kg
"""
import unittest

import assessor
import criteria
import data_generator
import fuel_calc
import main
import validator

REF = {"flight_id": "T1", "origin": "EGLL", "destination": "EGCC", "distance_km": 1000,
       "alternate_km": 100, "tas_kph": 800, "wind_kph": 0, "burn_rate_kgph": 1800,
       "fuel_capacity_kg": 6000, "fuel_onboard_kg": 4000}


def status_for(onboard):
    f = dict(REF, fuel_onboard_kg=onboard)
    calc = fuel_calc.calculate(f)
    return assessor.assess(f, calc, criteria.required_fuel(f, calc))["status"]


class TestAFRM(unittest.TestCase):
    def test_ground_speed(self):
        self.assertEqual(fuel_calc.ground_speed(800, 50), 750)    # headwind
        self.assertEqual(fuel_calc.ground_speed(800, -50), 850)   # tailwind

    def test_trip_fuel_endurance_range(self):
        calc = fuel_calc.calculate(REF)
        self.assertAlmostEqual(calc["trip_fuel_kg"], 2250)
        self.assertAlmostEqual(calc["endurance_h"], 3850 / 1800)
        self.assertAlmostEqual(calc["range_km"], 3850 / 1800 * 800)

    def test_required_fuel_matches_hand_calculation(self):
        req = criteria.required_fuel(REF, fuel_calc.calculate(REF))
        self.assertAlmostEqual(req["contingency_kg"], 112.5)
        self.assertAlmostEqual(req["alternate_kg"], 225)
        self.assertAlmostEqual(req["reserve_kg"], 765)
        self.assertEqual(req["total_kg"], 3503)

    def test_status_boundaries(self):
        # required 1000 -> marginal band is 0 <= margin < 50
        self.assertEqual(assessor.classify(-0.1, 1000), "INSUFFICIENT")
        self.assertEqual(assessor.classify(0, 1000), "MARGINAL")
        self.assertEqual(assessor.classify(49.9, 1000), "MARGINAL")
        self.assertEqual(assessor.classify(50, 1000), "SUFFICIENT")

    def test_status_end_to_end(self):
        self.assertEqual(status_for(4000), "SUFFICIENT")
        self.assertEqual(status_for(3600), "MARGINAL")      # margin 97 < 175.15
        self.assertEqual(status_for(3400), "INSUFFICIENT")

    def test_valid_flight_passes(self):
        self.assertEqual(validator.validate_flight(REF), [])

    def test_invalid_flights_rejected(self):
        bad_changes = [{"fuel_onboard_kg": -1}, {"fuel_onboard_kg": 6001},
                       {"distance_km": 0}, {"tas_kph": 0, "wind_kph": 0},
                       {"wind_kph": 700}]
        for change in bad_changes:
            self.assertTrue(validator.validate_flight(dict(REF, **change)), change)

    def test_same_seed_gives_same_data(self):
        self.assertEqual(data_generator.generate_flights(10, 7),
                         data_generator.generate_flights(10, 7))
        self.assertNotEqual(data_generator.generate_flights(10, 7),
                            data_generator.generate_flights(10, 8))

    def test_pipeline_rejects_only_the_faulty_flights(self):
        results, rejected = main.run(20, 42, True)
        self.assertEqual(len(results), 20)
        self.assertEqual([f["flight_id"] for f, _ in rejected], ["AF901", "AF902", "AF903"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
