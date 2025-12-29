"""
Simple Streamlit dashboard for the Debt Sustainability Simulator.

Run with:
    streamlit run ui/dashboards_streamlit.py
"""

import streamlit as st
import pandas as pd

from models.debt_dynamics import project_debt_path, classify_risk
from models.scenario_engine import load_baseline, load_shocks, apply_shock


def main():
    st.title("Debt Sustainability Simulator")

    st.sidebar.header("Inputs")

    debt_start_pct = st.sidebar.slider(
        "Initial Debt/GDP (%)", min_value=20, max_value=150, value=65, step=5
    )
    threshold_pct = st.sidebar.slider(
        "Debt/GDP Risk Threshold (%)", min_value=50, max_value=120, value=80, step=5
    )

    debt_start = debt_start_pct / 100.0
    threshold = threshold_pct / 100.0

    r_baseline, g_baseline, pb_baseline = load_baseline()
    shocks = load_shocks()

    scenario_name = st.sidebar.selectbox("Scenario", list(shocks.keys()))

    shock = shocks.get(scenario_name, {"rate_spike": 0.0, "recession": 0.0, "fiscal_slippage": 0.0})
    r_series, g_series, pb_series = apply_shock(r_baseline, g_baseline, pb_baseline, shock)

    debt_path = project_debt_path(debt_start, r_series, g_series, pb_series)
    risk = classify_risk(debt_path, threshold=threshold)

    years = list(range(len(debt_path)))
    df = pd.DataFrame({
        "Year": years,
        "Debt/GDP (%)": [x * 100 for x in debt_path],
    })

    st.subheader(f"Scenario: {scenario_name}")
    st.line_chart(df.set_index("Year"))

    st.markdown(f"**Final Debt/GDP:** {debt_path[-1]*100:.1f}%")
    st.markdown(f"**Max Debt/GDP:** {max(debt_path)*100:.1f}%")
    st.markdown(f"**Risk classification:** {risk}")


if __name__ == "__main__":
    main()
