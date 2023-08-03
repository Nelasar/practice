from abc import ABC, abstractmethod


class Priceable(ABC):
    @abstractmethod
    def setPrice(self, p):
        pass

    @abstractmethod
    def getName(self):
        pass

    @abstractmethod
    def getPrice(self):
        pass

    @abstractmethod
    def getPriceHistory(self):
        pass