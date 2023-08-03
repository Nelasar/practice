from priceable import Priceable
from matlib import *


class Bond(Priceable):
    def __init__(self, b_name="", b_price=0.0, s_quantity=0, s_price_hist=list()):
        self.name = b_name
        self.price = b_price
        self.quantity = s_quantity
        self.price_history = s_price_hist
        self.type = "Bond"

        n = random.randint(20, 50)

        self.price_history = GBM(n, T, r, q, sigma, self.price)

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

    def getType(self):
        return self.type
