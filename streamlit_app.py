import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from calculations import run_sustainability

st.set_page_config(page_title="Debt Sustainability Simulator", layout="wide")

st.title("Debt Sustainability Simulator")

st.markdown("""
This tool models medium-term debt sustainability under different growth, interest rate, and primary balance assumptions.
""")

uploaded = st.file_uploader("Upload baseline data (CSV)", type=["csv"])

if uploaded:
    baseline = pd.read_csv(uploaded)
else:
    baseline = pd.read_csv("sample_inputs.csv")

st.subheader("Input Parameters")

col1, col2, col3 = st.columns(3)

with col1:
    growth = st.slider("Real GDP Growth (%)", -5.0, 10.0, 2.0, 0.1)
with col2:
    rate = st.slider("Interest Rate on Debt (%)", 0.0, 12.0, 4.0, 0.1)
with col3:
    primary = st.slider("Primary Balance (% GDP)", -10.0, 5.0, -2.0, 0.1)

years = st.slider("Projection Horizon (Years)", 5, 30, 10)

df = run_sustainability(
    baseline=baseline,
    growth=growth / 100,
    rate=rate / 100,
    primary=primary / 100,
    years=years
)

st.subheader("Debt-to-GDP Projection")
fig = px.line(df, x="Year", y="Debt_GDP", title="Debt-to-GDP Path")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Interest Burden (% GDP)")
fig2 = px.line(df, x="Year", y="Interest_GDP", title="Interest Burden")
st.plotly_chart(fig2, use_container_width=True)

st.subheader("Primary Balance Requirement for Stabilization")

required_pb = df["Required_Primary"].iloc[-1]
st.metric("Required Primary Balance (% GDP)", f"{required_pb:.2%}")

st.markdown("---")
st.write("Simulation Output Table")
st.dataframe(df)
