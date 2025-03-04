# 📊 T5 Index

This Python project uses the `yfinance` library to download historical data for cryptocurrencies BTC, ETH, XRP, SOL, and ADA, calculating a weighted index and displaying a chart 📈.

## 🚀 Virtual Environment Setup

To avoid conflicts between libraries, it is recommended to create a virtual environment. Run:

```sh
python3 -m venv crypto
source crypto/bin/activate  # Linux/macOS
crypto\Scripts\activate    # Windows
```

## 📦 Installing Dependencies

All necessary libraries are listed in the `requirements.txt` file. After activating the virtual environment, install the dependencies:

```sh
pip install -r requirements.txt
```

## 🛠️ Possible Issues

Due to library updates, the program may not run correctly. To ensure compatibility, it is recommended to install Jupyter Notebook and run the code inside it:

```sh
pip install jupyter
jupyter notebook
```

## 📜 Main Code

The script performs the following tasks:

- 📥 Downloads historical data for Bitcoin (BTC), Ethereum (ETH), Ripple (XRP), Solana (SOL), and Cardano (ADA) using `yfinance`
- 🔢 Applies different weights to each cryptocurrency and calculates a custom index
- 📊 Generates a chart of the index over time

## ⏳ Start and End Parameters in yf.download()

In the yf.download() function, the start and end parameters define the date range for fetching historical data. Future versions of the program can modify these values to analyze different time periods. For example:
```sh
BTC = yf.download("BTC-USD", start="2023-01-01", end="2024-01-01", period="1d")
```
A developer can adjust the start and end dates to focus on different periods of interest, whether for long-term trends or short-term analysis.

## 📈 Example of the Generated Chart

The final chart displays the evolution of the calculated index based on the closing prices of the selected cryptocurrencies.

## 🤝 Contribution

Feel free to suggest improvements or report issues via issues or pull requests!

## 📜 License

This project is under the The Unlicense. Feel free to use and modify it.

Happy coding! 🚀💻
