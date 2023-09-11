from yahoostock import yfStock
from bond import *


class Market:
    def __init__(self):
        self.tickers = ('GOOG', 'MSFT', 'PYPL', 'EVGO', 'U', 'GAZP.ME')
                        # 'SHOP', 'HOOD', 'TTOO', 'QCOM', 'WIX',
                        # 'HAS',  'SAVE', 'MRNA', 'ETSY', 'MELI',
                        # 'RR.L', 'AMZN', 'DRVN', 'RAD',  'AAPL',
                        # 'FSLY', 'OXY',  'BUD',  'DASH', 'UPWK') # ДО СЮДА РАБОТАЕТ
                        #'RUN',  'SDGR', 'SPR',  'WAVD') #'CFLT')
                        #'ALIT', 'AFRM', 'TSLA', 'UBER', 'SOFI',
                        #'ROCK', 'FTDR', 'NKLA', 'NVDA', 'INTC',
                        #'PAYC', 'GNRC', 'DNA',  'LFUS', 'EXAS')
        self.assets = {ticker: yfStock(ticker) for ticker in self.tickers}

    def addAsset(self, asset):
        ticker = asset.getTicket()
        self.assets[ticker] = asset

    def getAsset(self, symbol: str):
        return self.assets[symbol]

    def allAssets(self):
        return self.assets.values()


    def printMarket(self):
        for asset in self.assets.values():
            print(asset.str_line())

    def printTickers(self):
        print(self.tickers)
