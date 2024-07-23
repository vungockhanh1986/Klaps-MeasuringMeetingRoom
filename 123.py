import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

PRIMARY_COLOR = "#0072B5"
SECONDARY_COLOR = "#B54300"
CSV_FILE = (
    "https://raw.githubusercontent.com/holoviz/panel/main/examples/assets/occupancy.csv"
)

@st.cache_data
def get_data():
    return pd.read_csv(CSV_FILE, parse_dates=["date"], index_col="date")

data = get_data()

def transform_data(variable, window, sigma):
    avg = data[variable].rolling(window=window).mean()
    residual = data[variable] - avg
    std = residual.rolling(window=window).std()
    outliers = np.abs(residual) > std * sigma
    return avg, avg[outliers]

def get_plot(variable="Temperature", window=30, sigma=10):
    avg, highlight = transform_data(variable, window, sigma)

    fig = px.line(avg, title=f"{variable} with Outliers", labels={"value": variable})
    fig.add_scatter(x=highlight.index, y=highlight.values, mode="markers", name="Outliers")
    fig.update_traces(marker=dict(color=SECONDARY_COLOR), selector=dict(name="Outliers"))
    fig.update_traces(line_color=PRIMARY_COLOR, selector=dict(name=f"{variable} with Outliers"))
    return fig

variable = st.selectbox("Variable", list(data.columns), index=list(data.columns).index("Temperature"))
window = st.slider("Window", 1, 60, 30)
sigma = st.slider("Sigma", 0, 20, 10)

plot = get_plot(str(variable), window, sigma)
st.plotly_chart(plot)
