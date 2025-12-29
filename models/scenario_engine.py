"""
Scenario engine that reads baseline data and applies shocks.

Baseline is stored in data/baseline_macro.csv
Shocks are stored in data/shock_scenarios.csv
"""

import csv
from typing import Dict, List, Tuple
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def load_baseline() -> Tuple[List[float], List[float], List[float]]:
    """
    Loads baseline r, g, and primary balance series from CSV.

    Returns:
        (r_series, g_series, primary_balance_series)
    """
    baseline_file = DATA_DIR / "baseline_macro.csv"
    r_series, g_series, pb_series = [], [], []

    with baseline_file.open("r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            r_series.append(float(row["r"]))
            g_series.append(float(row["g"]))
            pb_series.append(float(row["primary_balance"]))

    return r_series, g_series, pb_series


def load_shocks() -> Dict[str, Dict[str, float]]:
    """
    Loads shock scenarios into a dict.

    Returns:
        {
          "Baseline": {"rate_spike": ..., "recession": ..., "fiscal_slippage": ...},
          ...
        }
    """
    shock_file = DATA_DIR / "shock_scenarios.csv"
    scenarios: Dict[str, Dict[str, float]] = {}

    with shock_file.open("r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["scenario"]
            scenarios[name] = {
                "rate_spike": float(row["rate_spike"]),
                "recession": float(row["recession"]),
                "fiscal_slippage": float(row["fiscal_slippage"]),
            }

    return scenarios


def apply_shock(
    r_series: List[float],
    g_series: List[float],
    pb_series: List[float],
    shock: Dict[str, float],
) -> Tuple[List[float], List[float], List[float]]:
    """
    Applies a shock to baseline series.

    Shocks:
      - rate_spike: adds to r
      - recession: subtracts from g
      - fiscal_slippage: subtracts from primary balance
    """
    rate_spike = shock.get("rate_spike", 0.0)
    recession = shock.get("recession", 0.0)
    fiscal_slippage = shock.get("fiscal_slippage", 0.0)

    r_shocked = [r + rate_spike for r in r_series]
    g_shocked = [g - recession for g in g_series]
    pb_shocked = [pb - fiscal_slippage for pb in pb_series]

    return r_shocked, g_shocked, pb_shocked
