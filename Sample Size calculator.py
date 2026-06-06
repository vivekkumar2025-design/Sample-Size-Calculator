# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 15:05:26 2026

@author: Vivek
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from scipy.stats import norm
import numpy as np

# Page Configuration
st.set_page_config(page_title="Sample Size Calculator", layout="centered")

st.title("📊 Research Sample Size Calculator")
st.markdown("Easily calculate the required sample size for your research, surveys, or A/B tests.")

# --- SIDEBAR INPUTS ---
st.sidebar.header("Calculation Parameters")

population_size = st.sidebar.number_input(
    "Population Size", 
    min_value=1, 
    value=1000, 
    help="The total number of people in the group you are studying."
)

# UPDATED: Now allows ANY number between 1.0 and 99.99 for Confidence Level
confidence_level = st.sidebar.number_input(
    "Confidence Level (%)", 
    min_value=1.0,
    max_value=99.99,
    value=95.0,
    step=1.0,
    help="Type any specific confidence level you need (e.g., 95, 99, 88.5)."
)

# UPDATED: Now allows ANY number for Margin of Error
margin_of_error = st.sidebar.number_input(
    "Margin of Error (%)", 
    min_value=0.01, 
    max_value=100.0, 
    value=5.0, 
    step=0.5,
    help="Type your exact acceptable error range. (e.g., 5, 2.5, 10.5)"
)

# --- MATHEMATICAL LOGIC ---
# Convert percentages to decimals
moe_decimal = margin_of_error / 100
conf_level_decimal = confidence_level / 100

# Calculate Z-Score
z_score = norm.ppf(1 - (1 - conf_level_decimal) / 2)
p = 0.5  # Assumes maximum variance for a conservative sample size

# Standard calculation
raw_sample_size = (z_score**2 * p * (1 - p)) / (moe_decimal**2)

# Apply Finite Population Correction (FPC)
final_sample_size = (raw_sample_size * population_size) / (raw_sample_size + population_size - 1)
final_sample_size = int(np.ceil(final_sample_size)) # Round up to nearest whole number

# --- DISPLAY OUTPUT ---
st.success(f"### Recommended Sample Size: **{final_sample_size}**")

st.divider()

# --- DYNAMIC VISUALIZATION ---
st.subheader("How Precision Impacts Your Sample Size")
st.markdown("This chart shows how your required sample size changes as you demand a smaller margin of error.")

# UPDATED: Make the chart dynamically scale based on whatever Margin of Error the user types
max_chart_range = max(0.15, moe_decimal * 1.5) # Ensures the red dot is always visible
error_margins_range = np.linspace(0.01, max_chart_range, 50) 
sample_sizes_range = []

for e in error_margins_range:
    n = (z_score**2 * p * (1 - p)) / (e**2)
    n_adj = (n * population_size) / (n + population_size - 1)
    sample_sizes_range.append(int(np.ceil(n_adj)))

# Create Chart
df = pd.DataFrame({
    "Margin of Error": error_margins_range, 
    "Sample Size": sample_sizes_range
})

fig = px.line(df, x="Margin of Error", y="Sample Size", markers=True)
fig.update_layout(xaxis_tickformat=".0%")

# Highlight the user's current selection on the chart
fig.add_scatter(x=[moe_decimal], y=[final_sample_size], mode='markers', 
                marker=dict(color='red', size=12), name="Your Selection")

st.plotly_chart(fig, use_container_width=True)

