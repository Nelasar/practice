import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
import yfinance as yf
import ta
from sklearn.linear_model import LinearRegression
plt.style.use('seaborn')
warnings.filterwarnings("ignore")

# sortino ratio
# like sharpe ratio
# SortinoRatio < 0 - not profitable
# SortinoRatio < 1 - profitable, but risk is higher than the returns
# SortinoRatio > 1 - very good, risk lower that the returns
# sortino = mu / sigma(down)

"""
# ПЕРЕПИСЫВАЮ ЗДЕСЬ АНАЛИЗАТОР CAMP
f = yf.download('GOOG')  # , end='2021-01-01')
return_serie = f['Adj Close'].pct_change(1).dropna()
return_serie.name = 'return'

# Compute the sortino
mean = np.mean(return_serie)  # 252 trading days
vol = np.std(return_serie[return_serie < 0])  # sqrt(252)
sortino = np.sqrt(252) * mean / vol
print(f"Sortino: {'%.3f', sortino}")

# we need to compute the covariance between the market and the portfolio
sp500 = yf.download("^GSPC")["Adj Close"].pct_change(1)
sp500.name = 'SP500'

# we concatenate them to do the covariances
val = pd.concat((return_serie, sp500), axis=1).dropna()

# we compute beta
# covariation var matrix
cov_var_mat = np.cov(val.values, rowvar=False)
cov = cov_var_mat[0][1]
var = cov_var_mat[1][1]

beta = cov / var

print(f"Beta: {'%.3f' % beta}")

# ALPHA is a statistic  that indicates whether the portfolio outperforms the market in terms of risk return
# alpha > 0: outperforms
# alpha < 0: underperforms

alpha = 252 * mean * (1 - beta)
alpha_perc = alpha * 100
print(f"Alpha: {'%.1f' % alpha_perc}")  # in percentage


#

# drawdown - is the measure of the risk of the strategy
# it represents the maximum loss of a strategy over a period of time
# which allows you to understand if the strategy is risky
# and thus choose it according to your level of risk aversion

def drawdown_function(serie):
    # we compute Cumsum of the returns
    cum = serie.dropna().cumsum() + 1
    # we compute max of the cumsum on the period (accumulate max)
    # (1, 3, 5, 3, 1) ->  (1, 3, 5, 5, 5)
    running_max = np.maximum.accumulate(cum)
    # we compute drawdown
    drawdown = cum / running_max - 1
    return drawdown


# adapt figure size
dd = drawdown_function(return_serie)

plt.figure(figsize=(15, 8))
# plot the drawdown
plt.fill_between(dd.index, dd * 100, 0, dd, color="#CE5757", alpha=0.65)
# put a title
plt.ylabel('Drawdown in %')
plt.title("Drawdown")
plt.show()

max_dropdown = -np.min(dd) * 100
print(f"Max dd: {'%.1f' % max_dropdown} % ")


def BackTest(serie, annualized_scalar=252):  # a_s = 12 - monthly
    # sp500 = yf.download(", annualized_scalar^GSPC")["Adj Close"].pct_change(1)
    # sp500.name = "SP500"

    val = pd.concat((serie, sp500), axis=1).dropna()
    drawdown = drawdown_function(serie) * 100

    max_drawdown = -np.min(drawdown)

    sortino = np.sqrt(annualized_scalar) * serie.mean() / serie.loc[serie < 0].std()

    beta = np.cov(val[["return", "SP500"]].values, rowvar=False)[0][1] / np.var(val["SP500"].values)

    alpha = annualized_scalar * serie.mean() - annualized_scalar * serie.mean()

    print(f"Sortino: {np.round(sortino, 3)}")
    print(f"Beta: {np.round(beta, 3)}")
    print(f"Alpha: {np.round(alpha, 3)}")
    print(f"Max Drawdown: {np.round(max_drawdown, 3)}")


BackTest(return_serie)


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
    df['return'] = df['strategy']

    BackTest(df['return'].iloc[split:])

    plt.plot(df['strategy'].cumsum() * 100, label='strategy')
    plt.xlabel('Date')
    plt.ylabel('Values')
    plt.title('Strategy Result')
    plt.legend()
    plt.show()

# lin_reg_trading("ETH-EUR") in main
"""