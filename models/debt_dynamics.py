"""
Core debt dynamics engine.

This follows the classic debt sustainability identity:

Debt_{t+1} = Debt_t + (r - g) * Debt_t - PrimaryBalance_t

Where all flows are in % of GDP terms.
"""

from typing import List, Tuple

def project_debt_path(
    debt_start: float,
    r_series: List[float],
    g_series: List[float],
    primary_balance_series: List[float]
) -> List[float]:
    """
    Projects a debt-to-GDP path given series for r, g, and primary balance.

    Args:
        debt_start: Initial Debt/GDP (e.g., 0.65 for 65%)
        r_series: Effective interest rate each year (decimal)
        g_series: Nominal GDP growth each year (decimal)
        primary_balance_series: Primary balance each year as % of GDP
                                (positive = surplus, negative = deficit)

    Returns:
        List of Debt/GDP over time (including starting value).
    """
    if not (len(r_series) == len(g_series) == len(primary_balance_series)):
        raise ValueError("All input series must have the same length.")

    debt_path = [debt_start]

    for t in range(len(r_series)):
        debt_t = debt_path[-1]
        r = r_series[t]
        g = g_series[t]
        pb = primary_balance_series[t]

        next_debt = debt_t + (r - g) * debt_t - pb
        debt_path.append(next_debt)

    return debt_path


def classify_risk(debt_path: List[float], threshold: float = 0.80) -> str:
    """
    Simple classification of debt risk based on Debt/GDP threshold.

    Args:
        debt_path: List of Debt/GDP values (decimals).
        threshold: Level above which we say debt is "unsustainable".

    Returns:
        "Stable", "Vulnerable", or "Unsustainable"
    """
    final_debt = debt_path[-1]
    max_debt = max(debt_path)

    if max_debt < threshold:
        return "Stable"
    elif final_debt < threshold and max_debt >= threshold:
        return "Vulnerable"
    else:
        return "Unsustainable"


def find_breach_year(debt_path: List[float], threshold: float = 0.80) -> Tuple[bool, int]:
    """
    Returns whether and when the path first breaches a given Debt/GDP threshold.

    Args:
        debt_path: List of Debt/GDP values (decimals).
        threshold: Breach level.

    Returns:
        (breached, year_index)
        where year_index is the first year index where Debt/GDP >= threshold.
        If never breached, returns (False, -1).
    """
    for year, value in enumerate(debt_path):
        if value >= threshold:
            return True, year
    return False, -1
