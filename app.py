# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("T5 Index - Análise de Criptomoedas (via CoinGecko API)")

st.write("""
### Fonte de Dados: CoinGecko
A API do CoinGecko permite buscar dados de até **365 dias atrás** gratuitamente e sem autenticação.
""")

# Seleção de datas
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Data de Início", value=datetime.now() - timedelta(days=365))
with col2:
    end_date = st.date_input("Data de Término", value=datetime.now())

# Validação
if start_date >= end_date:
    st.error("Erro: A data de início deve ser anterior à data de término.")
    st.stop()

# Cálculo do número de dias (CoinGecko permite até 365)
num_days = (end_date - start_date).days
if num_days > 365:
    st.error("Erro: O intervalo não pode ultrapassar 365 dias.")
    st.stop()

# IDs e pesos
coins = {
    "bitcoin": 0.50,
    "ethereum": 0.25,
    "ripple": 0.10,
    "solana": 0.10,
    "cardano": 0.05
}

@st.cache_data(ttl=3600)
def get_coin_data(coin_id, days):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {
        "vs_currency": "usd",
        "days": days,
        "interval": "daily"
    }
    r = requests.get(url, params=params)
    prices = r.json().get("prices", [])
    df = pd.DataFrame(prices, columns=["timestamp", coin_id])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.set_index("timestamp", inplace=True)
    return df

# Download e construção do índice
dfs = []
for coin_id, weight in coins.items():
    df = get_coin_data(coin_id, num_days)
    df *= weight
    dfs.append(df)

# Unificar
df_combined = pd.concat(dfs, axis=1)
df_combined["CryptoIndex"] = df_combined.sum(axis=1)

# Normalizar para índice base 1000
df_combined["CryptoIndex"] = df_combined["CryptoIndex"] / df_combined["CryptoIndex"].iloc[0] * 1000

# Filtrar pelo intervalo de datas real
df_filtered = df_combined[(df_combined.index.date >= start_date) & (df_combined.index.date <= end_date)]

# Exibir dados
st.write("### Últimos dados disponíveis")
st.dataframe(df_filtered.tail())

# Gráfico
st.write("### Gráfico do Índice T5")
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(df_filtered.index, df_filtered["CryptoIndex"], label="T5 Index", color="blue")
ax.set_title("T5 Index (BTC 50%, ETH 25%, XRP 10%, SOL 10%, ADA 5%)")
ax.set_xlabel("Data")
ax.set_ylabel("Valor do Índice")
ax.grid(True)
ax.legend()
plt.xticks(rotation=45)
st.pyplot(fig)

