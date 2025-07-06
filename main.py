import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Fed Day SPY Strategy", layout="wide")
st.title("📈 Fed Day SPY Strategy Backtester")

# Sidebar parameters
holding_days = st.sidebar.slider("Holding Period (Days)", min_value=1, max_value=10, value=5)
pre_fomc_threshold = st.sidebar.slider("Pre-FOMC Drop Threshold (%)", min_value=-5.0, max_value=0.0, value=-1.0, step=0.1)

# FOMC Dates
fomc_dates = pd.to_datetime([
    "2020-01-29", "2020-03-15", "2020-04-29", "2020-06-10", "2020-07-29", "2020-09-16", "2020-11-05", "2020-12-16",
    "2021-01-27", "2021-03-17", "2021-04-28", "2021-06-16", "2021-07-28", "2021-09-22", "2021-11-03", "2021-12-15",
    "2022-01-26", "2022-03-16", "2022-05-04", "2022-06-15", "2022-07-27", "2022-09-21", "2022-11-02", "2022-12-14",
    "2023-02-01", "2023-03-22", "2023-05-03", "2023-06-14", "2023-07-26", "2023-09-20", "2023-11-01", "2023-12-13",
    "2024-01-31", "2024-03-20", "2024-05-01", "2025-01-29", "2025-03-19", "2025-05-07", "2025-06-18",
    "2025-07-30", "2025-09-17", "2025-10-29", "2025-12-10"
])

# Download SPY data
data = yf.download("SPY", start="2019-12-01", end="2025-12-31", auto_adjust=True)["Close"]

# Filter FOMC dates to ensure we have data after them
latest_valid_entry = data.index[-(holding_days + 1)]
valid_fomc_dates = [d for d in fomc_dates if d <= latest_valid_entry]

# Backtest logic
results = []

for date in valid_fomc_dates:
    entry_idx = data.index.searchsorted(date) + 1
    if entry_idx + holding_days >= len(data) or entry_idx - 3 < 0:
        continue

    pre_event_ret = ((data.iloc[entry_idx - 1] / data.iloc[entry_idx - 3]) - 1).item()
    if pre_event_ret > (pre_fomc_threshold / 100):
        continue

    entry_date = data.index[entry_idx]
    exit_date = data.index[entry_idx + holding_days]
    entry_price = data.loc[entry_date].item()
    exit_price = data.loc[exit_date].item()
    trade_return = (exit_price - entry_price) / entry_price

    results.append({
        "entry_date": entry_date,
        "exit_date": exit_date,
        "entry_price": entry_price,
        "exit_price": exit_price,
        "return": trade_return
    })

# Display results
if results:
    df = pd.DataFrame(results)
    df["cumulative_return"] = (1 + df["return"]).cumprod()

    cagr = df["cumulative_return"].iloc[-1]**(1 / ((df["exit_date"].iloc[-1] - df["entry_date"].iloc[0]).days / 365)) - 1
    sharpe = df["return"].mean() / df["return"].std() * np.sqrt(252 / holding_days)
    max_dd = (df["cumulative_return"] / df["cumulative_return"].cummax() - 1).min()

    st.subheader("📊 Strategy Performance")
    st.write(f"**Number of trades:** {len(df)}")
    st.write(f"**Final return:** {df['cumulative_return'].iloc[-1]:.2f}")
    st.write(f"**CAGR:** {cagr:.2%}")
    st.write(f"**Sharpe Ratio:** {sharpe:.2f}")
    st.write(f"**Max Drawdown:** {max_dd:.2%}")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["exit_date"], y=df["cumulative_return"], mode='lines+markers', name='Cumulative Return'))
    fig.add_trace(go.Scatter(x=df["entry_date"], y=[1]*len(df), mode='markers', name='Entries', marker=dict(symbol='triangle-up', color='green', size=8)))
    fig.add_trace(go.Scatter(x=df["exit_date"], y=df["cumulative_return"], mode='markers', name='Exits', marker=dict(symbol='x', color='red', size=6)))
    fig.update_layout(title="Fed Day SPY Strategy", xaxis_title="Exit Date", yaxis_title="Cumulative Return", template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🔍 Trade-Level Details")
    st.dataframe(df.round(4))

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Trade Log as CSV", csv, "fomc_strategy_results.csv", "text/csv")

else:
    st.warning("No qualifying trades found with current parameters.")
