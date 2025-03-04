# -*- coding: utf-8 -*-

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

BTC = yf.download("BTC-USD", start="2024-02-04", end="2025-03-04", period="1d")

ETH = yf.download("ETH-USD", start="2024-02-04", end="2025-02-04", period="1d")
XRP = yf.download("XRP-USD", start="2024-02-04", end="2025-02-04", period="1d")
SOL = yf.download("SOL-USD", start="2024-02-04", end="2025-02-04", period="1d")
ADA = yf.download("ADA-USD", start="2024-02-04", end="2025-02-04", period="1d")

CRYPTOS = [BTC, ETH, XRP, SOL, ADA]
print(  CRYPTOS[0].head() )
print ( CRYPTOS[1].head() )
print ( CRYPTOS[2].head() )
print ( CRYPTOS[3].head() )
print ( CRYPTOS[4].head() )

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



df["CryptoIndex"] = (    df["CryptoIndex"] / df["CryptoIndex"].iloc[0] * 1000 )

# 🔹 Graph
plt.figure(figsize=(12, 6))
plt.plot(df.index, df["CryptoIndex"], label="T5 Index", color="blue")
plt.title("BTC ( 50% ), ETH ( 25% ), SOLANA ( 10% ), XRP ( 10% ), ADA( 5% )")
plt.xlabel("Date")
plt.ylabel("Value")
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.show()
