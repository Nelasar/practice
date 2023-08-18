from abc import ABC, abstractmethod


class Priceable(ABC):
    @abstractmethod
    def getTicket(self):
        pass

    @abstractmethod
    def getType(self):
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