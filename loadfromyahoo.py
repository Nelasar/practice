import yfinance as yf
import ta

"""

tickets = ["GOOG", "EURUSD=X", "^GSPC"] # start="date", end="date", interval="1mo"

data = yf.download("GOOG")
ticker_list = yf.download(tickets)

# sma
df = yf.download("GOOG")
df = df[["Adj Close"]]
df.columns = ["close"]

# sma on 15 days
df["SMA 15"] = df["close"].rolling(15).mean().shift(1) # mean for 15 days
df["SMA 60"] = df["close"].rolling(60).mean().shift(1) # mean for 60

# MSD - moving standard deviation
# It is the volatility of returns

df = yf.download("GOOG")
df = df[["Adj Close"]]
df.columns = ["close"]

df["returns"] = df["close"].pct_change(1)
df["MSD 15"] = df[["returns"]].rolling(15).mean().shift(1) # mean for 15 days
df["MSD 60"] = df[["returns"]].rolling(60).mean().shift(1) # mean for 60


df = yf.download("GOOG")
df = df[["Adj Close"]]
df.columns = ["close"]
RSI = ta.momentum.RSIIndicator(df["close"], window=14)
"""

"""
df = yf.download("GOOG")
df = df[["Adj Close"]]
df.columns = ["close"]
df = df.loc["2010"]
RSI = ta.momentum.RSIIndicator(df["close"], window=14, fillna=False)

df["rsi"] = RSI.rsi()

plt.figure(figsize=(10, 6))
plt.plot(df['rsi'], label='SPA 15')
plt.xlabel('Date')
plt.ylabel('RSI')
plt.title('Generated Values over Time')
plt.legend()
plt.show()
"""