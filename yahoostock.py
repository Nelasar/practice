from priceable import Priceable
import yfinance as yf


class yfStock(Priceable):
    def __init__(self, ticket):
        self.__type = "Stock"
        self.__ticket = ticket
        self.__name = yf.Ticker(ticket).info['shortName']
        self.__long_name = yf.Ticker(ticket).info['longName']
        self.__country = str(yf.Ticker(ticket).info['country'])
        self.__industry = str(yf.Ticker(ticket).info['industry'])

        self.__price_history = yf.download(ticket)
        self.__price_history = self.__price_history[["Adj Close"]]
        self.__price_history.columns = ["close"]

        self.__price = yf.Ticker(ticket).info['currentPrice']
        self.__beta = str(yf.Ticker(ticket).info['beta'])
        self.__low = str(yf.Ticker(ticket).info['dayLow'])
        self.__high = str(yf.Ticker(ticket).info['dayHigh'])
        self.__open = str(yf.Ticker(ticket).info['open'])

        self.__quantity = 0

        self.__info = {'Ticket':   self.__ticket,
                       'Name':     self.__name,
                       'FullName': self.__long_name,
                       'Country':  self.__country,
                       'Industry': self.__industry,
                       'Price':    str(self.__price),
                       'Beta':     self.__beta,
                       'Low':      self.__low,
                       'High':     self.__high,
                       'Open':     self.__open}

    def __str__(self):
        return f"Information:\nTicker: {self.__ticket}\n" \
                f"Company Name: {self.__name}\n" \
                f"Country: {self.__country}\n" \
                f"Current Price: {self.__price}\n" \
                f"Industry: {self.__industry}\n"

    def getInfoValues(self, key=None):
        if key is None:
            return self.__info
        else:
            return self.__info[key]

    def getTicket(self):
        return self.__ticket

    def getName(self):
        return self.__name

    def getPrice(self):
        return self.__price

    def getQuantity(self):
        return self.__quantity

    def changeQuantity(self, change):
        self.__quantity += change

    def getPriceHistory(self):
        return self.__price_history

    def getType(self):
        return self.__type
