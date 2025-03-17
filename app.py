# -*- coding: utf-8 -*-
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from datetime import datetime, timedelta

# Título do aplicativo
st.title('T5 Index - Análise de Criptomoedas por um indice teórico')

# Explicação sobre a limitação da API
st.write("""
### Limitação da API
A API do Yahoo Finance (`yfinance`) só consegue buscar dados de até **1 ano atrás** a partir da data atual.
Por favor, selecione um intervalo de datas dentro desse limite.
""")

# Seleção de datas pelo usuário
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Data de Início (Start)", value=datetime.now() - timedelta(days=730))
with col2:
    end_date = st.date_input("Data de Término (End)", value=datetime.now())

# Validação do intervalo de datas
if (end_date - start_date).days > 730:
    st.error("Erro: O intervalo de datas não pode ser maior que 1 ano (365 dias).")
    st.stop()

# Baixar dados das criptomoedas
try:
    BTC = yf.download("BTC-USD", start=start_date, end=end_date, period="1d")
    ETH = yf.download("ETH-USD", start=start_date, end=end_date, period="1d")
    XRP = yf.download("XRP-USD", start=start_date, end=end_date, period="1d")
    SOL = yf.download("SOL-USD", start=start_date, end=end_date, period="1d")
    ADA = yf.download("ADA-USD", start=start_date, end=end_date, period="1d")
except Exception as e:
    st.error(f"Erro ao baixar os dados: {e}")
    st.stop()

# Exibir os primeiros registros de cada criptomoeda
st.write("### Primeiros 10 Registros de Cada Criptomoeda")
st.write("**BTC:**")
st.write(BTC.head(10))
st.write("**ETH:**")
st.write(ETH.head(10))
st.write("**XRP:**")
st.write(XRP.head(10))
st.write("**SOL:**")
st.write(SOL.head(10))
st.write("**ADA:**")
st.write(ADA.head(10))

# Exibir os últimos registros de cada criptomoeda
st.write("### Últimos 10 Registros de Cada Criptomoeda")
st.write("**BTC:**")
st.write(BTC.tail(10))
st.write("**ETH:**")
st.write(ETH.tail(10))
st.write("**XRP:**")
st.write(XRP.tail(10))
st.write("**SOL:**")
st.write(SOL.tail(10))
st.write("**ADA:**")
st.write(ADA.tail(10))

# Preparar os dados para o índice
BTC_Close = pd.DataFrame(BTC['Close'])
ETH_Close = pd.DataFrame(ETH['Close'])
XRP_Close = pd.DataFrame(XRP['Close'])
SOL_Close = pd.DataFrame(SOL['Close'])
ADA_Close = pd.DataFrame(ADA['Close'])

weights = {
    "BTC": 0.50,   # 50% 
    "ETH": 0.25,   # 25% 
    "XRP": 0.10,   # 10% 
    "SOL": 0.10,   # 10% 
    "ADA": 0.05    # 5% 
}

df = pd.concat([BTC_Close, ETH_Close, XRP_Close, SOL_Close, ADA_Close], axis=1)
df["CryptoIndex"] = (
    df["BTC-USD"] * weights["BTC"] +
    df["ETH-USD"] * weights["ETH"] +
    df["XRP-USD"] * weights["XRP"] +
    df["SOL-USD"] * weights["SOL"] +
    df["ADA-USD"] * weights["ADA"]
)
df["CryptoIndex"] = (df["CryptoIndex"] / df["CryptoIndex"].iloc[0] * 1000)

# Exibir o gráfico
st.write("### Índice de Criptomoedas")
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(df.index, df["CryptoIndex"], label="T5 Index", color="blue")
ax.set_title("BTC ( 50% ), ETH ( 25% ), SOLANA ( 10% ), XRP ( 10% ), ADA( 5% )")
ax.set_xlabel("Date")
ax.set_ylabel("Value")
ax.legend()
ax.grid(True)
plt.xticks(rotation=45)
st.pyplot(fig)
