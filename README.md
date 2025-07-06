# 📈 Fed Day SPY Strategy Backtester

This is a simple backtesting tool that evaluates a SPY trading strategy centered around U.S. Federal Reserve (FOMC) meeting dates. Built with Streamlit, it allows you to interactively adjust parameters and visualize the performance of the strategy.

## 🧠 Strategy Logic

The strategy goes long on SPY **one day after an FOMC meeting**, but only **if SPY declined in the 2 days leading up to the meeting**. The position is then held for a customizable number of days.

You can test how this rule performs historically by tweaking the holding period and pre-FOMC drop threshold.

## 📊 Features

- ✅ Select holding period: 1–10 days  
- ✅ Choose pre-FOMC drop threshold (e.g., -1%)  
- 📅 Built-in FOMC meeting dates from 2020 to 2025  
- 📈 Download SPY data via Yahoo Finance  
- 📉 Filters out invalid trades (e.g., insufficient data)  
- 🔢 Outputs performance metrics:
  - Total number of trades
  - Cumulative return
  - CAGR (Compounded Annual Growth Rate)
  - Sharpe ratio (annualized)
  - Max drawdown  
- 📉 Trade-level breakdown (entry/exit dates and returns)  
- 📥 Download trade log as CSV  
- 📊 Interactive cumulative return chart (Plotly)

## 📦 Tech Stack

- [Streamlit](https://streamlit.io/) – for the web UI  
- [yfinance](https://pypi.org/project/yfinance/) – to fetch SPY price data  
- [pandas](https://pandas.pydata.org/) and [numpy](https://numpy.org/) – for calculations  
- [Plotly](https://plotly.com/python/) – for charts  

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/your-username/fed-day-spy-strategy.git
cd fed-day-spy-strategy
