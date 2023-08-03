# Super Vector Machine Regressor

import yfinance as yf
import ta
import pandas as pd
import matplotlib as mpl
from matplotlib import cycler
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import numpy as np
from sklearn.svm import SVR


def drawdown_function(serie):
    # we compute Cumsum of the returns
    cum = serie.dropna().cumsum() + 1
    # we compute max of the cumsum on the period (accumulate max)
    # (1, 3, 5, 3, 1) ->  (1, 3, 5, 5, 5)
    running_max = np.maximum.accumulate(cum)
    # we compute drawdown
    drawdown = cum / running_max - 1
    return drawdown


def feature_engineering_svm(df):
    # copy the dataframe
    df_copy = df.dropna().copy()

    # create new returns
    df_copy['returns'] = df_copy['close'].pct_change(1)

    df_indicators = ta.add_all_ta_features(
        df, open="open", high="high", low="low", close="close", volume="volume", fillna=True).shift(1)

    dfc = pd.concat((df_indicators, df_copy), axis=1)
    return dfc.dropna()


def BackTest(serie, annualized_scalar=252):  # a_s = 12 - monthly
    sp500 = yf.download("^GSPC")["Adj Close"].pct_change(1)
    sp500.name = "SP500"

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


# import data
# open - opening price
df = yf.download("GOOG")[["Open", "High", "Low", "Adj Close", "Volume"]]
df.columns = ['open', 'high', 'low', 'close', 'volume']

dfc = feature_engineering_svm(df)

# percentage train set
split = int(0.80 * len(dfc))

# train set
X_train = dfc.iloc[:split, 6:dfc.shape[1]-1]
y_train = dfc[['returns']].iloc[:split]

# test set
X_test = dfc.iloc[split:, 6:dfc.shape[1]-1]
y_test = dfc[['returns']].iloc[split:]

# STANDARTIZATION
#
sc = StandardScaler()

X_train_sc = sc.fit_transform(X_train)
X_test_sc = sc.transform(X_test)

#plt.plot(X_train.values[:,0:15])
#plt.title("WITHOUT std")
#plt.show()

plt.plot(X_train_sc[:, 0:15])
plt.title("WITH std")
plt.show()

# PRINCIPAL COMPONENT ANALYSIS
# Dimension reduction

pca = PCA(n_components=6)
X_train_pca = pca.fit_transform(X_train_sc)
X_test_pca = pca.transform(X_test_sc)

print(f"Without PCA: {np.shape(X_train)} \nWith PCA: {np.shape(X_train_pca)}")

# SVR
# Initialize the class
reg = SVR()
reg.fit(X_train_pca, y_train)

# Create predictions for the whole dataset
X = np.concatenate((X_train_pca, X_test_pca), axis=0)
dfc['prediction'] = reg.predict(X)
dfc['prediction'].plot()
plt.show()

dfc['position'] = np.sign(dfc['prediction'])
dfc['strategy'] = dfc['returns'] * dfc['position'].shift(1)
dfc['return'] = dfc['strategy']
BackTest(dfc['return'].iloc[split:])


def svm_reg_trading(symbol):
    def feature_engineering_svm(df):
        # copy the dataframe
        df_copy = df.dropna().copy()

        # create new returns
        df_copy['returns'] = df_copy['close'].pct_change(1)

        df_indicators = ta.add_all_ta_features(
            df, open="open", high="high", low="low", close="close", volume="volume", fillna=True).shift(1)

        dfc = pd.concat((df_indicators, df_copy), axis=1)
        return dfc.dropna()

    df = yf.download(symbol)[["Open", "High", "Low", "Adj Close", "Volume"]]
    df.columns = ['open', 'high', 'low', 'close', 'volume']

    dfc = feature_engineering_svm(df)
    # percentage train set
    split = int(0.80 * len(dfc))
    # train set
    X_train = dfc.iloc[:split, 6:dfc.shape[1] - 1]
    y_train = dfc[['returns']].iloc[:split]
    # test set
    X_test = dfc.iloc[split:, 6:dfc.shape[1] - 1]
    y_test = dfc[['returns']].iloc[split:]

    sc = StandardScaler()

    X_train_sc = sc.fit_transform(X_train)
    X_test_sc = sc.transform(X_test)

    pca = PCA(n_components=6)
    X_train_pca = pca.fit_transform(X_train_sc)
    X_test_pca = pca.transform(X_test_sc)

    reg = SVR()
    reg.fit(X_train_pca, y_train)

    # Create predictions for the whole dataset
    X = np.concatenate((X_train_pca, X_test_pca), axis=0)
    dfc['prediction'] = reg.predict(X)

    dfc['position'] = np.sign(dfc['prediction'])
    dfc['strategy'] = dfc['returns'] * dfc['position'].shift(1)
    dfc['return'] = dfc['strategy']
    BackTest(dfc['return'].iloc[split:])

svm_reg_trading("^IXIC")