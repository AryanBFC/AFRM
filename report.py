"""report.py - console summary, CSV results and a log of rejected flights.
   for now this will remain in the console until improvements are made for assignment 2."""
import csv
import os

import config


def print_summary(results, rejected):
    print("\nAFRM FUEL STATUS REPORT (simulated data - not for operational use)")
    print("-" * 78)
    print(f"{'Flight':<7}{'Onboard':>9}{'Required':>10}{'Margin':>9}{'Margin%':>9}"
          f"{'Range km':>10}{'Endur h':>9}  Status")
    for r in results:
        print(f"{r['flight_id']:<7}{r['onboard_kg']:>9.0f}{r['required_kg']:>10}"
              f"{r['margin_kg']:>9.0f}{r['margin_pct']:>8.1f}%{r['range_km']:>10.0f}"
              f"{r['endurance_h']:>9.2f}  {r['status']}")
    print("-" * 78)

    counts = {"SUFFICIENT": 0, "MARGINAL": 0, "INSUFFICIENT": 0}
    for r in results:
        counts[r["status"]] += 1
    print(f"Assessed: {len(results)} | Sufficient: {counts['SUFFICIENT']} | "
          f"Marginal: {counts['MARGINAL']} | Insufficient: {counts['INSUFFICIENT']} | "
          f"Rejected: {len(rejected)}")
    for f, errors in rejected:
        print(f"  REJECTED {f['flight_id']}: {'; '.join(errors)}")


def write_files(results, rejected):
    """Write the results CSV and the rejected-flight log to the output folder."""
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)

    with open(os.path.join(config.OUTPUT_DIR, "afrm_results.csv"), "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["flight_id", "onboard_kg", "taxi_kg", "trip_kg", "contingency_kg",
                         "alternate_kg", "reserve_kg", "required_kg", "margin_kg", "status"])
        for r in results:
            b = r["breakdown"]
            writer.writerow([r["flight_id"], r["onboard_kg"], b["taxi_kg"],
                             round(b["trip_kg"], 1), round(b["contingency_kg"], 1),
                             round(b["alternate_kg"], 1), round(b["reserve_kg"], 1),
                             r["required_kg"], r["margin_kg"], r["status"]])

    with open(os.path.join(config.OUTPUT_DIR, "afrm_log.txt"), "w") as file:
        for f, errors in rejected:
            file.write(f"REJECTED {f['flight_id']}: {'; '.join(errors)}\n")
