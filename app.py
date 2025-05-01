import requests
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta

@st.cache_data(ttl=3600)
def get_crypto_history(coin_id, days=365):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {
        "vs_currency": "usd",
        "days": days,
        "interval": "daily"
    }
    response = requests.get(url, params=params)
    data = response.json()
    prices = data["prices"]
    df = pd.DataFrame(prices, columns=["timestamp", coin_id])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.set_index("timestamp", inplace=True)
    return df

# IDs do CoinGecko
coins = {
    "bitcoin": 0.50,
    "ethereum": 0.25,
    "ripple": 0.10,
    "solana": 0.10,
    "cardano": 0.05
}

st.title("T5 Index com dados do CoinGecko")

dfs = []
for coin, weight in coins.items():
    df = get_crypto_history(coin)
    df *= weight
    dfs.append(df)

# Combine os dados
df_index = pd.concat(dfs, axis=1)
df_index["CryptoIndex"] = df_index.sum(axis=1)
df_index["CryptoIndex"] = df_index["CryptoIndex"] / df_index["CryptoIndex"].iloc[0] * 1000

st.line_chart(df_index["CryptoIndex"])
