# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from datetime import datetime, timedelta
from pycoingecko import CoinGeckoAPI

# Inicializar a API do CoinGecko
cg = CoinGeckoAPI()

# Título do aplicativo
st.title('T5 Index - Análise de Criptomoedas por um índice teórico')

# Explicação sobre a limitação da API
st.write("""
### Limitação da API
A API pública do CoinGecko permite buscar dados históricos de até **365 dias atrás** a partir da data atual.
Por favor, selecione um intervalo de datas dentro desse limite.
""")

# Seleção de datas pelo usuário
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Data de Início (Start)", value=datetime.now() - timedelta(days=365))
with col2:
    end_date = st.date_input("Data de Término (End)", value=datetime.now())

# Validação do intervalo de datas
if (end_date - start_date).days > 365:
    st.error("Erro: O intervalo de datas não pode ser maior que 365 dias.")
    st.stop()

# Conversão de datas para timestamp UNIX
start_timestamp = int(datetime.combine(start_date, datetime.min.time()).timestamp())
end_timestamp = int(datetime.combine(end_date, datetime.min.time()).timestamp())

# Lista de criptomoedas e seus IDs no CoinGecko
coins = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "XRP": "ripple",
    "SOL": "solana",
    "ADA": "cardano"
}

# Dicionário para armazenar os DataFrames
dfs = {}

# Baixar dados das criptomoedas
for symbol, coin_id in coins.items():
    try:
        data = cg.get_coin_market_chart_range_by_id(
            id=coin_id,
            vs_currency='usd',
            from_timestamp=start_timestamp,
            to_timestamp=end_timestamp
        )
        prices = data['prices']
        df = pd.DataFrame(prices, columns=['timestamp', f'{symbol}-USD'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        dfs[symbol] = df
    except Exception as e:
        st.error(f"Erro ao baixar os dados para {symbol}: {e}")
        st.stop()

# Combinar os DataFrames em um único DataFrame
df_combined = pd.concat(dfs.values(), axis=1)

# Exibir os primeiros registros de cada criptomoeda
st.write("### Primeiros 10 Registros de Cada Criptomoeda")
for symbol in coins.keys():
    st.write(f"**{symbol}:**")
    st.write(dfs[symbol].head(10))

# Exibir os últimos registros de cada criptomoeda
st.write("### Últimos 10 Registros de Cada Criptomoeda")
for symbol in coins.keys():
    st.write(f"**{symbol}:**")
    st.write(dfs[symbol].tail(10))

# Preparar os dados para o índice
weights = {
    "BTC": 0.50,   # 50%
    "ETH": 0.25,   # 25%
    "XRP": 0.10,   # 10%
    "SOL": 0.10,   # 10%
    "ADA": 0.05    # 5%
}

# Calcular o índice
df_combined['CryptoIndex'] = sum(
    df_combined[f'{symbol}-USD'] * weight for symbol, weight in weights.items()
)
df_combined['CryptoIndex'] = (df_combined['CryptoIndex'] / df_combined['CryptoIndex'].iloc[0]) * 1000

# Exibir o gráfico
st.write("### Índice de Criptomoedas")
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(df_combined.index, df_combined['CryptoIndex'], label="T5 Index", color="blue")
ax.set_title("BTC (50%), ETH (25%), XRP (10%), SOL (10%), ADA (5%)")
ax.set_xlabel("Data")
ax.set_ylabel("Valor do Índice")
ax.legend()
ax.grid(True)
plt.xticks(rotation=45)
st.pyplot(fig)
