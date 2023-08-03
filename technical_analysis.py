import ta
from matlib import *

def simple_analysis(security):
    df = makeDataFrame(security)

    # Create the returns
    df['returns'] = df['close'].pct_change(1)

    # Create the SMA's
    df['SMA 15'] = df[['close']].rolling(15).mean().shift(1)
    df['SMA 60'] = df[['close']].rolling(60).mean().shift(1)

    # Create the volatilities
    df['MSD 10'] = df[['returns']].rolling(10).std().shift(1)
    df['MSD 60'] = df[['returns']].rolling(30).std().shift(1)

    # Create the RSI
    RSI = ta.momentum.RSIIndicator(df['close'], window=14, fillna=False)
    df['rsi'] = RSI.rsi()

    return df

