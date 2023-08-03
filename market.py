import numpy as np
import yfinance as yf
from yahoostock import yfStock


class Market:
    def __init__(self):
        self.tickers = ('GOOG', 'MSFT', 'PYPL', 'QCOM', 'U')
        #'SHOP', 'HOOD', 'TTOO', 'EVGO', 'WIX',
        #'HAS',  'SAVE', 'MRNA', 'ETSY', 'MELI',
        #'RR.L', 'AMZN', 'DRVN', 'RAD',  'AAPL',
        #'FSLY', 'OXY',  'BUD',  'DASH', 'UPWK',
        #'RUN',  'SDGR', 'SPR',  'WAVD', 'CFLT',
        #'ALIT', 'AFRM', 'TSLA', 'UBER', 'SOFI',
        #'ROCK', 'FTDR', 'NKLA', 'NVDA', 'INTC',
        #'PAYC', 'GNRC', 'DNA',  'LFUS', 'EXAS')
        self.assets = {ticker: yfStock(ticker) for ticker in self.tickers}

    def getAsset(self, symbol: str):
        return self.assets[symbol]

    def allAssets(self):
        return self.assets.values()

    def printMarketFull(self):
        for asset in self.assets.values():
            print(asset)

    def printMarket(self):
        for asset in self.assets.values():
            print(asset.str_line())

    def printTickers(self):
        print(self.tickers)




