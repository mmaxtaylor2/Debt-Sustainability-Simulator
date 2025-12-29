# Debt Sustainability Simulator

This project models sovereign Debt/GDP dynamics and stress scenarios,
similar to the tools used by IMF and World Bank country teams.

It focuses on:
- Debt/GDP projections under baseline assumptions
- Interest-growth dynamics (r versus g)
- Primary balance paths
- Shock scenarios such as recessions and rate spikes
- Simple risk classifications (Stable, Vulnerable, Unsustainable)

## How it works

The core identity is:

Debt(t+1) = Debt(t) + (r - g) * Debt(t) - PrimaryBalance(t)

All variables are expressed as percentages of GDP:
- Debt is Debt/GDP
- r is the effective interest rate on debt
- g is nominal GDP growth
- Primary balance is the government's fiscal position (surplus or deficit)

Baseline assumptions and shock parameters are stored in CSV files in the
`data/` folder. The Python models read these inputs and generate Debt/GDP
paths over time.

## Running the CLI simulator

From the project root:

    python3 ui/cli_simulator.py

You can then choose between baseline and different shock scenarios
(e.g., recession, rate spike, IMF program) and see the resulting
Debt/GDP trajectory and a simple risk label.

## Running the Streamlit dashboard

If you have Streamlit installed:

    streamlit run ui/dashboards_streamlit.py

The dashboard lets you:
- Adjust initial Debt/GDP and a risk threshold
- Switch between scenarios
- Visualize the Debt/GDP path over time

This project is designed to showcase sovereign risk analysis and
debt sustainability skills for entry-level macro and policy roles.
