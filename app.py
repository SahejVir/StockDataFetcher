import streamlit as st
import pandas as pd
import requests
from secret import ALPHA_VANTAGE_API_KEY

st.title("Stock Price Fetcher")

st.write("Enter a stock symbol")

symbol = st.text_input("Stock Symbol", placeholder="AAPL, MSFT, TSLA")

if symbol:
    st.success(f"Fetching data for {symbol.upper()}....")

if symbol:

    url = "https://www.alphavantage.co/query"

    param = {
        "function" : "TIME_SERIES_DAILY",
        "symbol" : symbol.upper(),
        "apikey" : ALPHA_VANTAGE_API_KEY
    }

    response = requests.get(url, params=param)
    data = response.json()

    time_series = data.get("Time Series (Daily)", {})

    rows = []

    for date, daily_data in time_series.items():
        rows.append({
            "Date" : date,
            "Open" : float(daily_data["1. open"]),
            "High" : float(daily_data["2. high"]),
            "Low"  : float(daily_data["3. low"]),
            "Close": float(daily_data["4. close"])
        })

    df = pd.DataFrame(rows)

    df = df.sort_values("Date")

    st.markdown(df.to_html(index=False), unsafe_allow_html=True)

    if not df.empty:
        df_plot = df.set_index("Date")
        st.line_chart(df_plot[["Open","Close"]])