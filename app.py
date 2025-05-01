# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from datetime import datetime, timedelta
from pycoingecko import CoinGeckoAPI

# Inicializar a API
cg = CoinGeckoAPI()

# Dicionário com os ids das moedas na CoinGecko
crypto_ids = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "XRP": "ripple",
    "SOL": "solana",
    "ADA": "cardano"
}

# Título do aplicativo
st.title('T5 Index - Análise de Criptomoedas por um índice teórico')

# Explicação sobre a limitação da API
st.write("""
### Limitação da API
A API do CoinGecko permite dados históricos, mas a granularidade pode ser diária apenas para intervalos de até 90 dias.
""")

# Seleção de datas pelo usuário
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Data de Início (Start)", value=datetime.now() - timedelta(days=30))
with col2:
    end_date = st.date_input("Data de Término (End)", value=datetime.now())

# Validação do intervalo de datas
if (end_date - start_date).days > 90:
    st.error("Erro: O intervalo de datas não pode ser maior que 90 dias.")
    st.stop()

# Função para obter preços históricos diários
@st.cache_data
def get_price_history(coin_id, vs_currency, from_date, to_date):
    from_ts = int(datetime.combine(from_date, datetime.min.time()).timestamp())
    to_ts = int(datetime.combine(to_date, datetime.min.time()).timestamp())
    data = cg.get_coin_market_chart_range_by_id(id=coin_id,
                                                 vs_currency=vs_currency,
                                                 from_timestamp=from_ts,
                                                 to_timestamp=to_ts)
    prices = data['prices']
    df = pd.DataFrame(prices, columns=["timestamp", "price"])
    df["date"] = pd.to_datetime(df["timestamp"], unit="ms").dt.date
    df = df.groupby("date").first()  # Um valor por dia
    df = df.rename(columns={"price": f"{coin_id.upper()}-USD"})
    return df[[f"{coin_id.upper()}-USD"]]

# Baixar dados
try:
    BTC = get_price_history(crypto_ids["BTC"], "usd", start_date, end_date)
    ETH = get_price_history(crypto_ids["ETH"], "usd", start_date, end_date)
    XRP = get_price_history(crypto_ids["XRP"], "usd", start_date, end_date)
    SOL = get_price_history(crypto_ids["SOL"], "usd", start_date, end_date)
    ADA = get_price_history(crypto_ids["ADA"], "usd", start_date, end_date)
except Exception as e:
    st.error(f"Erro ao baixar os dados: {e}")
    st.stop()

# Exibir os primeiros registros
st.write("### Primeiros 10 Registros de Cada Criptomoeda")
st.write("**BTC:**"); st.write(BTC.head(10))
st.write("**ETH:**"); st.write(ETH.head(10))
st.write("**XRP:**"); st.write(XRP.head(10))
st.write("**SOL:**"); st.write(SOL.head(10))
st.write("**ADA:**"); st.write(ADA.head(10))

# Exibir os últimos registros
st.write("### Últimos 10 Registros de Cada Criptomoeda")
st.write("**BTC:**"); st.write(BTC.tail(10))
st.write("**ETH:**"); st.write(ETH.tail(10))
st.write("**XRP:**"); st.write(XRP.tail(10))
st.write("**SOL:**"); st.write(SOL.tail(10))
st.write("**ADA:**"); st.write(ADA.tail(10))

# Preparar os dados para o índice
df = pd.concat([BTC, ETH, XRP, SOL, ADA], axis=1).dropna()

weights = {
    "BTC": 0.50,
    "ETH": 0.25,
    "XRP": 0.10,
    "SOL": 0.10,
    "ADA": 0.05
}

df["CryptoIndex"] = (
    df["BITCOIN-USD"] * weights["BTC"] +
    df["ETHEREUM-USD"] * weights["ETH"] +
    df["RIPPLE-USD"] * weights["XRP"] +
    df["SOLANA-USD"] * weights["SOL"] +
    df["CARDANO-USD"] * weights["ADA"]
)
df["CryptoIndex"] = (df["CryptoIndex"] / df["CryptoIndex"].iloc[0] * 1000)

# Exibir o gráfico
st.write("### Índice de Criptomoedas")
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(df.index, df["CryptoIndex"], label="T5 Index", color="blue")
ax.set_title("BTC (50%), ETH (25%), SOLANA (10%), XRP (10%), ADA (5%)")
ax.set_xlabel("Data")
ax.set_ylabel("Valor")
ax.legend()
ax.grid(True)
plt.xticks(rotation=45)
st.pyplot(fig)
