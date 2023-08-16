import random
import math
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import ta

r = 0.04
q = 0.0
sigma = 0.20
T = 1
N0 = 20
N1 = 15
N2 = 33
N3 = 48
S0 = 1423.0
S1 = 2334.213
S2 = 254.3434
S3 = 100.34

#np.random.seed(0)
date_range = pd.date_range(start='2022-07-24', end='2023-07-24', freq='D')

# создать массив со случайной даты до текущей
# потом разделять созданный массив как захочется - по годам, месяцам, дням

# sma для ценной бумаги
def SMA(security):
    df = makeDataFrame(security)
    df["SMA 15"] = df[["close"]].rolling(15).mean().shift(1)  # mean for 15 days
    df["SMA 60"] = df[["close"]].rolling(60).mean().shift(1)  # mean for 60

    # можно задавать, чтобы выводить инфу по конкретному году
    #df = df[["close", 'SMA 15', 'SMA 60']].loc['2010']

    plt.figure(figsize=(10, 6))

    plt.plot(df['close'], label='values')
    plt.plot(df['SMA 15'], label='SPA 15')
    plt.plot(df['SMA 60'], label='SPA 60')

    plt.xlabel('Date')
    plt.ylabel('Values')
    plt.title('Generated Values over Time')
    plt.legend()
    plt.show()

def MSD(security):
    df = makeDataFrame(security)
    df["returns"] = df["close"].pct_change(1)
    df["MSD 15"] = df[["returns"]].rolling(15).mean().shift(1)  # mean for 15 days
    df["MSD 60"] = df[["returns"]].rolling(60).mean().shift(1)  # mean for 60

    plt.figure(figsize=(10, 6))

    plt.plot(df['returns'], label='values')
    plt.plot(df['MSD 15'], label='SPA 15')
    plt.plot(df['MSD 60'], label='SPA 60')

    plt.xlabel('Date')
    plt.ylabel('Values')
    plt.title('Generated Values over Time')
    plt.legend()
    plt.show()

# симуляция истории цен через нормальное распределение (random walk)
def simulateHistory(start_price):
    #val1 = np.random.uniform(33, 41,len(date_range))
    #val2 = 40*np.sin(np.linspace(0, 4*np.pi, len(date_range))) + 50
    # Simulate stock price history in a range of 14-120 using a simple random walk model
    initial_price = start_price
    lower_bound = 0.0
    upper_bound = start_price + 2000

    random_walk = np.random.normal(0, 1, len(date_range))
    history = np.cumsum(random_walk) + initial_price
    # Make sure the simulated stock price stays within the range
    history = np.clip(history, lower_bound, upper_bound)

    return history
    #######

# сделать дата фрейм истории
def makeDataFrame(security):
    df = pd.DataFrame({
        'date': date_range,
        'close': security.getHistory()
    })

    df.set_index('date', inplace=True)

    return df

# напечатать график истории цен
def printGraphHistory(security):
    df = makeDataFrame(security)
    # Print DataFrame
    print(df)
    # Plot the data
    plt.figure(figsize=(10, 6))

    plt.plot(df['close'], label='values - rand walk')

    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.title('Generated Values over Time')
    plt.legend()
    plt.show()

# GBM из плюсов
def GBM(N, T, r, q, sigma, S0):
    dt = T / N
    ret = [S0]

    drift = math.exp(dt * ((r - q) - 0.5 * sigma * sigma))
    vol = math.sqrt(sigma * sigma * dt)

    for i in range(1, N):
        Z = random.normalvariate(0.0, 1.0)
        ret.append(ret[i - 1] * drift * math.exp(vol * Z))

    return ret

# numpy GBM
def numpyGBM(mu, sigma, size):
    return np.random.normal(mu, sigma, size)


