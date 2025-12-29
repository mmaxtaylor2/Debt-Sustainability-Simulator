"""
Command-line Debt Sustainability Simulator.

Run with:
    python3 ui/cli_simulator.py
"""

from typing import List

from models.debt_dynamics import project_debt_path, classify_risk, find_breach_year
from models.scenario_engine import load_baseline, load_shocks, apply_shock


def format_percentage_series(series: List[float]) -> str:
    return " → ".join(f"{x*100:.1f}%" for x in series)


def run_scenario(scenario_name: str, debt_start: float = 0.65, threshold: float = 0.80) -> None:
    r_baseline, g_baseline, pb_baseline = load_baseline()
    shocks = load_shocks()

    shock = shocks.get(scenario_name, {"rate_spike": 0.0, "recession": 0.0, "fiscal_slippage": 0.0})

    r_series, g_series, pb_series = apply_shock(r_baseline, g_baseline, pb_baseline, shock)

    debt_path = project_debt_path(
        debt_start=debt_start,
        r_series=r_series,
        g_series=g_series,
        primary_balance_series=pb_series,
    )

    classification = classify_risk(debt_path, threshold=threshold)
    breached, year = find_breach_year(debt_path, threshold=threshold)

    print("\n====================================================")
    print(f"Scenario: {scenario_name}")
    print("----------------------------------------------------")
    print(f"Initial Debt/GDP: {debt_start*100:.1f}%")
    print(f"Final Debt/GDP:   {debt_path[-1]*100:.1f}%")
    print(f"Max Debt/GDP:     {max(debt_path)*100:.1f}%")
    print("Debt/GDP path:")
    print(f"  {format_percentage_series(debt_path)}")
    print("----------------------------------------------------")
    if breached:
        print(f"Debt/GDP first breaches {threshold*100:.0f}% in Year {year}.")
    else:
        print(f"Debt/GDP never breaches {threshold*100:.0f}% in this horizon.")
    print(f"Risk classification: {classification}")
    print("====================================================\n")


def main() -> None:
    scenarios = list(load_shocks().keys())

    print("Debt Sustainability Simulator")
    print("=============================")
    print("Select a scenario:\n")
    for idx, name in enumerate(scenarios, start=1):
        print(f"  {idx}. {name}")
    print()

    choice = input("Enter number (or 'q' to quit): ").strip()
    if choice.lower() == "q":
        return

    try:
        idx = int(choice) - 1
        if idx < 0 or idx >= len(scenarios):
            raise ValueError
    except ValueError:
        print("Invalid selection.")
        return

    scenario_name = scenarios[idx]
    run_scenario(scenario_name)


if __name__ == "__main__":
    main()
