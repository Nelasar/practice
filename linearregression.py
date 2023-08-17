import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
import yfinance as yf
import ta
from yahoostock import *
from sklearn.linear_model import LinearRegression
plt.style.use('default')
warnings.filterwarnings("ignore")

class StockAnalysis:
    def __init__(self, asset):
        self.history = asset.getPriceHistory().copy()
        self.history = self.history.dropna()

        self.indexies = []

    def sma(self, first_period, second_period, save=None):
        df_copy = self.history.copy()

        first_index = 'SMA ' + str(first_period)
        second_index = 'SMA ' + str(second_period)

        df_copy[first_index] = df_copy[['close']].rolling(first_period).mean().shift(1)
        df_copy[second_index] = df_copy[['close']].rolling(second_period).mean().shift(1)

        return df_copy

    def msd(self, first_period, second_period, save=None):
        df_copy = self.history.copy()
        df_copy['returns'] = df_copy['close'].pct_change(1)

        first_index = 'MSD ' + str(first_period)
        second_index = 'MSD ' + str(second_period)

        df_copy[first_index] = df_copy[['returns']].rolling(first_period).std().shift(1)
        df_copy[second_index] = df_copy[['returns']].rolling(second_period).std().shift(1)

        return df_copy

    def RSI(self, save=None):
        df_copy = self.history.copy()
        RSI = ta.momentum.RSIIndicator(df_copy['close'], window=14, fillna=False)
        df_copy['rsi'] = RSI.rsi()

        return df_copy

    def feature_engineering(self, sma_first_period, sma_second_period,
                                  msd_first_period, msd_second_period):
        df_copy = self.history.copy()
        df_copy['returns'] = df_copy['close'].pct_change(1)

        first_index = 'SMA ' + str(sma_first_period)
        second_index = 'SMA ' + str(sma_second_period)
        third_index = 'MSD ' + str(msd_first_period)
        fourth_index = 'MSD ' + str(msd_second_period)

        self.indexies = [first_index, second_index, third_index, fourth_index]

        # create SMAs
        df_copy[first_index] = df_copy[['close']].rolling(sma_first_period).mean().shift(1)
        df_copy[second_index] = df_copy[['close']].rolling(sma_second_period).mean().shift(1)

        df_copy[third_index] = df_copy[['returns']].rolling(msd_first_period).std().shift(1)
        df_copy[fourth_index] = df_copy[['returns']].rolling(msd_second_period).std().shift(1)

        RSI = ta.momentum.RSIIndicator(df_copy['close'], window=14, fillna=False)
        df_copy['rsi'] = RSI.rsi()

        return df_copy.dropna()

    def lin_reg_trading(self, day1, day2, day3, day4):
        df = self.feature_engineering(day1, day2, day3, day4)
        # percentage train set
        split = int(0.80 * len(df))

        # train set creation
        X_train = df[self.indexies].iloc[:split]
        y_train = df[['returns']].iloc[:split]

        # test set creation
        X_test = df[self.indexies].iloc[split:]
        y_test = df[['returns']].iloc[split:]

        linear = LinearRegression()
        linear.fit(X_train, y_train)

        # create predictions for the whole dataset
        X = np.concatenate((X_train, X_test), axis=0)
        df["prediction"] = linear.predict(X)
        # compute the position
        df['position'] = np.sign(df['prediction'])
        # compute the returns
        df['strategy'] = df['returns'] * df['position'].shift(1)

        return df

    '''
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
    '''

