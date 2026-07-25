import streamlit as st
import pandas as pd
import requests
from secret import ALPHA_VANTAGE_API_KEY

st.set_page_config(page_title="Stock Price Fetcher", page_icon="📈")

st.title("Stock Price Fetcher")
st.write("Developed by Sahej Vir Singh Pasay")
st.write("Enter any US-listed stock symbol (e.g., AAPL, MSFT, TSLA)")

symbol = st.text_input("Stock Symbol", placeholder="AAPL, MSFT, TSLA")

@st.cache_data
def fetch_daily_prices(symbol: str) -> pd.DataFrame | None:
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol.upper(),
        "apikey": ALPHA_VANTAGE_API_KEY,
    }
    response = requests.get(url, params=params, timeout=10)
    data = response.json()

    time_series = data.get("Time Series (Daily)")
    if not time_series:
        return None

    rows = []
    for date, daily_data in time_series.items():
        rows.append({
            "Date": date,
            "Open": float(daily_data["1. open"]),
            "High": float(daily_data["2. high"]),
            "Low": float(daily_data["3. low"]),
            "Close": float(daily_data["4. close"]),
        })

    df = pd.DataFrame(rows)
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")
    return df

if symbol:
    with st.spinner(f"Fetching data for {symbol.upper()}..."):
        df = fetch_daily_prices(symbol)

    if df is None:
        st.error("Could not fetch data. Check the symbol or try again later.")
    elif df.empty:
        st.warning("No data returned for this symbol.")
    else:
        st.success(f"Showing latest {len(df)} days for {symbol.upper()}")

        st.subheader("Price table")
        st.dataframe(df, use_container_width=True)

        st.subheader("Open vs Close")
        df_plot = df.set_index("Date")
        st.line_chart(df_plot[["Open", "Close"]])
else:
    st.info("Please enter a stock symbol above to fetch data.")