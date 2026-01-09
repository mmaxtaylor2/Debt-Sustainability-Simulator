import streamlit as st
import pandas as pd

from models.scenario_engine import run_scenarios
from ui.dashboard import plot_debt, plot_interest

st.set_page_config(page_title="Debt Sustainability Dashboard", layout="wide")

st.title("Debt Sustainability Simulator")

baseline = pd.read_csv("data/baseline_macro.csv")
shocks = pd.read_csv("data/shock_scenarios.csv")

years = st.slider("Projection Horizon (Years)", 5, 30, 10)

df = run_scenarios(baseline, shocks, years)

st.subheader("Debt-to-GDP Projection")
plot_debt(df)

st.subheader("Interest Burden (% GDP)")
plot_interest(df)

st.subheader("Stabilization Metrics")
required = df.groupby("Scenario")["Required_Primary"].last().reset_index()
st.dataframe(required)

st.markdown("---")
st.write("Full Output Table")
st.dataframe(df)

