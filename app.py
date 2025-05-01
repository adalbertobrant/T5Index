import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from datetime import datetime, timedelta

st.title('T5 Index - Análise de Criptomoedas por um índice teórico')

st.write("""
### Limitação da API
A API do Yahoo Finance (`yfinance`) só consegue buscar dados de até **1 ano atrás** a partir da data atual.
Por favor, selecione um intervalo de datas dentro desse limite.
""")

col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Data de Início (Start)", value=datetime.now() - timedelta(days=365))
with col2:
    end_date = st.date_input("Data de Término (End)", value=datetime.now())

if (end_date - start_date).days > 365:
    st.error("Erro: O intervalo de datas não pode ser maior que 1 ano (365 dias).")
    st.stop()

# Função com cache para download de dados
@st.cache_data(ttl=3600)  # cache de 1 hora (3600 segundos)
def load_crypto_data(tickers, start, end):
    return yf.download(tickers, start=start, end=end)["Close"]

tickers = ["BTC-USD", "ETH-USD", "XRP-USD", "SOL-USD", "ADA-USD"]

try:
    data = load_crypto_data(tickers, start_date, end_date)
except Exception as e:
    st.error(f"Erro ao baixar os dados: {e}")
    st.stop()

st.write("### Primeiros 10 Registros")
st.dataframe(data.head(10))

st.write("### Últimos 10 Registros")
st.dataframe(data.tail(10))

weights = {
    "BTC-USD": 0.50,
    "ETH-USD": 0.25,
    "XRP-USD": 0.10,
    "SOL-USD": 0.10,
    "ADA-USD": 0.05
}

crypto_index = sum(data[ticker] * weight for ticker, weight in weights.items())
crypto_index = crypto_index / crypto_index.iloc[0] * 1000
data["CryptoIndex"] = crypto_index

# Gráfico
st.write("### Índice de Criptomoedas")
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(data.index, data["CryptoIndex"], label="T5 Index", color="blue")
ax.set_title("BTC (50%), ETH (25%), XRP (10%), SOL (10%), ADA (5%)")
ax.set_xlabel("Data")
ax.set_ylabel("Valor do Índice")
ax.grid(True)
ax.legend()
plt.xticks(rotation=45)
st.pyplot(fig)
