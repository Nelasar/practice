import random
from priceable import Priceable
from matlib import *
import numpy as np
import pandas as pd
from datetime import datetime
import pandas_datareader as pdr

class yfStock(Priceable):
    def __init__(self, ticket):
        self.type = "Stock"
        self.ticket = ticket
        self.name = yf.Ticker(ticket).info['shortName']
        self.country = yf.Ticker(ticket).info['country']
        self.industry = yf.Ticker(ticket).info['industry']

        self.price_history = yf.download(ticket)
        self.price_history = self.price_history[["Adj Close"]]
        self.price_history.columns = ["close"]
        self.price = yf.Ticker(ticket).info['currentPrice']
        self.quantity = 0
        #self.price = self.price_history["close"].iloc[-1]

    def __copy__(self):
        return type(self)(self.ticket, self.name, self.country, self.industry, self.price_history, self.price, self.quantity)

    def __str__(self):
        return f"Information:\nTicker: {self.ticket}\n" \
                f"Company Name: {self.name}\n" \
                f"Country: {self.country}\n" \
                f"Current Price: {self.price}\n" \
                f"Industry: {self.industry}\n"

    def str_line(self):
        return f"{self.ticket} --- {self.name} --- {self.industry} --- {self.price}"

    def print_historical(self):
        plt.plot(self.price_history)
        plt.xlabel('Date')
        plt.ylabel('Values')
        plt.title('Historical Data')
        plt.legend()
        plt.show()

    def getTicket(self):
        return self.ticket

    def getName(self):
        return self.name

    def getPrice(self):
        return self.price

    def getQuantity(self):
        return self.quantity

    def setQuantity(self, quantity):
        self.quantity = quantity

    def changeQuantity(self, change):
        self.quantity -= change

    def setPrice(self, p):
        self.price = p

    def getPriceHistory(self):
        return self.price_history

    def getType(self):
        return self.type

