from yahoostock import yfStock
from bond import *


class Market:
    def __init__(self):
        self.__tickers = ('GOOG', 'MSFT', 'PYPL', 'EVGO', 'U', 'GAZP.ME',
                        'SHOP', 'HOOD', 'TTOO', 'QCOM', 'WIX',
                        'HAS',  'SAVE', 'MRNA', 'ETSY', 'MELI',
                        'RR.L', 'AMZN', 'DRVN', 'RAD',  'AAPL',
                        'FSLY', 'OXY',  'BUD',  'DASH', 'UPWK')  # POINT
                        #'RUN',  'SDGR', 'SPR',  'WAVD') #'CFLT')
                        #'ALIT', 'AFRM', 'TSLA', 'UBER', 'SOFI',
                        #'ROCK', 'FTDR', 'NKLA', 'NVDA', 'INTC',
                        #'PAYC', 'GNRC', 'DNA',  'LFUS', 'EXAS')
        self.__assets = {ticker: yfStock(ticker) for ticker in self.__tickers}

    def addAsset(self, asset):
        ticker = asset.getTicket()
        self.__assets[ticker] = asset

    def getAsset(self, symbol: str):
        return self.__assets[symbol]

    def allAssets(self):
        return self.__assets.values()

    def printMarket(self):
        for asset in self.__assets.values():
            print(asset.str_line())

    def printTickers(self):
        print(self.__tickers)
