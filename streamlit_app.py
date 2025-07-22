import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Scannerz", layout="centered", initial_sidebar_state="collapsed")

st.markdown(
    "<h1 style='text-align: center; color: white;'>📉 Scannerz - Options Trade Finder</h1>",
    unsafe_allow_html=True,
)

ticker = st.text_input("Enter stock symbol", value="AAPL")

col1, col2, col3 = st.columns(3)
with col1:
    min_iv = st.slider("Min Implied Volatility", 0.0, 1.0, 0.4)
with col2:
    min_vol = st.slider("Min Volume", 0, 1000, 100)
with col3:
    opt_type = st.selectbox("Option Type", ["Calls", "Puts", "Both"])

def scan_options(ticker_symbol, min_iv, min_vol, opt_type):
    try:
        ticker = yf.Ticker(ticker_symbol)
        exps = ticker.options
        if not exps:
            return f"No options data available for {ticker_symbol}.", None
        exp = exps[0]
        chain = ticker.option_chain(exp)
        if opt_type == "Calls":
            df = chain.calls
        elif opt_type == "Puts":
            df = chain.puts
        else:
            df = pd.concat([chain.calls, chain.puts])

        df = df.sort_values(by='impliedVolatility', ascending=False)
        filtered = df[(df['impliedVolatility'] >= min_iv) & (df['volume'] >= min_vol)]

        return f"Top option trades for {ticker_symbol} (Exp: {exp})", filtered[['contractSymbol', 'strike', 'lastPrice', 'impliedVolatility', 'volume']].head(10)
    except Exception as e:
        return f"Error: {str(e)}", None

if st.button("Scan"):
    msg, results = scan_options(ticker, min_iv, min_vol, opt_type)
    st.write(msg)
    if results is not None:
        st.dataframe(results)
