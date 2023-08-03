import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
import yfinance as yf
import ta
from sklearn.linear_model import LinearRegression
plt.style.use('seaborn')
warnings.filterwarnings("ignore")

"""
df = yf.download("GOOG")
df = df[["Adj Close"]]
df.columns = ["close"]

# print(df.columns)

df['returns'] = df['close'].pct_change(1)

df['SMA 15'] = df[['close']].rolling(15).mean().shift(1)
df['SMA 60'] = df[['close']].rolling(60).mean().shift(1)

# Create the volatilities
df['MSD 10'] = df[['returns']].rolling(10).std().shift(1)
df['MSD 30'] = df[['returns']].rolling(30).std().shift(1)

# Create the RSI
RSI = ta.momentum.RSIIndicator(df['close'], window=14, fillna=False)
df['rsi'] = RSI.rsi()

df = df.dropna()
print(df.columns)

# percentage train set
split = int(0.80 * len(df))

# train set creation
X_train = df[['SMA 15', 'SMA 60', 'MSD 10', 'MSD 30', 'rsi']].iloc[:split]
y_train = df[['returns']].iloc[:split]

# test set creation
X_test = df[['SMA 15', 'SMA 60', 'MSD 10', 'MSD 30', 'rsi']].iloc[split:]
y_test = df[['returns']].iloc[split:]

linear = LinearRegression()
linear.fit(X_train, y_train)

# create predictions for the whole dataset
X = np.concatenate((X_train, X_test), axis=0)
# print(pd.DataFrame(X))
df["prediction"] = linear.predict(X)

# verify that the algorithm does not predict only way (pos or neg)
print(df['prediction'])

plt.plot(df['prediction'], label='Predicted Values')
plt.xlabel('Date')
plt.ylabel('Values')
plt.title('Predicted Values ')
plt.legend()
plt.show()

# compute the position
df['position'] = np.sign(df['prediction'])
# compute the returns
df['strategy'] = df['returns'] * df['position'].shift(1)

plt.plot(df['strategy'].cumsum() * 100, label='strategy')
plt.xlabel('Date')
plt.ylabel('Values')
plt.title('Strategy Result')
plt.legend()
plt.show()
"""

# GOOG, NTFLX, ETH-USD, ETH-EUR
def lin_reg_trading(symbol):
    def feature_engineering(df):
        # copy the dataframe
        df_copy = df.dropna().copy()

        # create new returns
        df_copy['returns'] = df_copy['close'].pct_change(1)

        # create SMAs
        df_copy['SMA 15'] = df_copy[['close']].rolling(15).mean().shift(1)
        df_copy['SMA 60'] = df_copy[['close']].rolling(60).mean().shift(1)

        # create the volatilities
        df_copy['MSD 10'] = df_copy[['returns']].rolling(10).std().shift(1)
        df_copy['MSD 30'] = df_copy[['returns']].rolling(30).std().shift(1)

        RSI = ta.momentum.RSIIndicator(df_copy['close'], window=14, fillna=False)
        df_copy['RSI'] = RSI.rsi()

        return df_copy.dropna()

    df = yf.download(symbol)
    df = df[['Adj Close']]
    df.columns = ["close"]

    dfc = feature_engineering(df)
    # percentage train set
    split = int(0.80 * len(df))

    # train set creation
    X_train = df[['SMA 15', 'SMA 60', 'MSD 10', 'MSD 30', 'rsi']].iloc[:split]
    y_train = df[['returns']].iloc[:split]

    # test set creation
    X_test = df[['SMA 15', 'SMA 60', 'MSD 10', 'MSD 30', 'rsi']].iloc[split:]
    y_test = df[['returns']].iloc[split:]

    linear = LinearRegression()
    linear.fit(X_train, y_train)

    # create predictions for the whole dataset
    X = np.concatenate((X_train, X_test), axis=0)
    # print(pd.DataFrame(X))
    df["prediction"] = linear.predict(X)

    # verify that the algorithm does not predict only way (pos or neg)
    print(df['prediction'])

    plt.plot(df['prediction'], label='Predicted Values')
    plt.xlabel('Date')
    plt.ylabel('Values')
    plt.title('Predicted Values ')
    plt.legend()
    plt.show()

    # compute the position
    df['position'] = np.sign(df['prediction'])
    # compute the returns
    df['strategy'] = df['returns'] * df['position'].shift(1)

    plt.plot(df['strategy'].cumsum() * 100, label='strategy')
    plt.xlabel('Date')
    plt.ylabel('Values')
    plt.title('Strategy Result')
    plt.legend()
    plt.show()


