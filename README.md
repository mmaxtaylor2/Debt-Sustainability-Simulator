## Debt Sustainability Simulator

A Python-based simulator for sovereign debt dynamics, inspired by frameworks used by IMF and World Bank country teams.

It models Debt/GDP paths under baseline assumptions and stress scenarios such as recessions, interest rate spikes, and fiscal reform programs.

## Overview

The simulator applies the standard debt sustainability identity:
Debt(t+1) = Debt(t) + (r - g) * Debt(t) - PrimaryBalance(t)

Where:

Debt/GDP is the public debt ratio
r is the effective interest rate
g is nominal GDP growth
PrimaryBalance is the fiscal position (surplus or deficit)

Shock scenarios adjust these variables to demonstrate how debt evolves under stress conditions.

## Key Features

Baseline debt projection over time
Recession, rate spike, and IMF program scenarios
Command-line interface for fast evaluation
Streamlit dashboard for visualization
Simple classification of outcomes: Stable, Vulnerable, Unsustainable
Modular structure for future expansion

## Why This Project Matters

This tool reflects core concepts used in sovereign debt sustainability analysis:

Interest-growth dynamics (r vs g)
Primary balance adjustments
Stress testing and scenario overlays
Threshold-based risk classification

It is useful for:

Economic policy and risk analysis practice
Internship and analyst recruiting portfolios
Building intuition for sovereign credit and macro-fiscal vulnerabilities

## Installation

Clone the repository:

git clone https://github.com/mmaxtaylor2/Debt-Sustainability-Simulator.git
cd Debt-Sustainability-Simulator

Install dependencies:

pip install -r requirements.txt

## Running the Simulator

CLI Version

python3 -m ui.cli_simulator

Streamlit Dashboard

streamlit run ui/dashboards_streamlit.py

## Repository Structure

data/                # Baseline and shock assumptions
models/              # Debt projection and scenario engines
ui/                  # CLI and Streamlit dashboard
requirements.txt     # Python dependencies
README.md            # Documentation
