import random
from priceable import Priceable
from matlib import *
import numpy as np


class NPStock(Priceable):
    def __init__(self, s_name="", s_price=0.0, s_quantity=0, s_price_hist=np.array([])):
        self.name = s_name
        self.price = s_price
        self.quantity = s_quantity
        self.price_history = s_price_hist
        self.numpy_price_history = s_price_hist
        self.type = "Stock"

        n = random.randint(20, 50)

        self.price_history = GBM(n, T, r, q, sigma, self.price)
        self.numpy_price_history = numpyGBM(self.price, 100.50, n)
        self.history = simulateHistory(self.price)

    def getName(self):
        return self.name

    def getPrice(self):
        return self.price

    def getQuantity(self):
        return self.quantity

    def setPrice(self, p):
        self.price = p

    def getPriceHistory(self):
        return self.price_history

    def getHistory(self):
        return self.history

    def getNP(self):
        return self.numpy_price_history

    def getType(self):
        return self.type
