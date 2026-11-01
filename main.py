"""main.py - runs the AFRM pipeline:
generate -> validate -> calculate -> apply criteria -> assess -> report."""
import assessor
import criteria
import data_generator
import fuel_calc
import report
import validator
import config


def run(n=20, seed=42, add_faults=True):
    flights = data_generator.generate_flights(n, seed, add_faults)
    valid, rejected = validator.validate_all(flights)

    results = []
    for f in valid:
        calc = fuel_calc.calculate(f)
        req = criteria.required_fuel(f, calc)
        results.append(assessor.assess(f, calc, req))
    return results, rejected


if __name__ == "__main__":
    results, rejected = run()
    report.print_summary(results, rejected)
    report.write_files(results, rejected)
