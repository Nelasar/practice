from priceable import Priceable
from matlib import *


class Bond(Priceable):
    def __init__(self, b_n, b_tick='',
                       b_name="",
                       b_country="",
                       b_industry="",
                       b_start_date="",
                       b_date='',
                       price=0.0,
                       b_divs=0.0
                       ):

        self.__type = "Bond"

        self.__ticket = b_tick
        self.__name = b_name
        self.__country = b_country
        self.__industry = b_industry
        self.__quantity = 0
        self.__price = price
        self.__maturity_date = b_date
        self.__dividends = b_divs

        n = b_n #random.randint(100, 10000)

        self.__price_history = GBM(n, T, r, q, sigma, self.__price)
        self.__price = round(self.__price_history[-1], 4)
        self.__low = self.__price - 1.342
        self.__high = self.__price + 2.74
        self.__open = self.__price

        dates = pd.date_range(b_start_date, '20230913')
        self.__price_history = pd.DataFrame(self.__price_history, index=dates, columns=["close"])

        self.__info = {'Ticket':    self.__ticket,
                     'Name':      self.__name,
                     'Country':   self.__country,
                     'Industry':  self.__industry,
                     'Price':     str(self.__price),
                     'Low':       self.__low,
                     'High':      self.__high,
                     'Open':      self.__open,
                     'Dividends': self.__dividends,
                     'Maturity':  self.__maturity_date}

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

    def __changeQuantity(self, change):
        self.__quantity += change

    def setPrice(self, p):
        self.__price = p

    def getPriceHistory(self):
        return self.__price_history

    def getType(self):
        return self.__type


bond1 = Bond(792,
             'ИСКЧ БО01',
             'ARTGEN-1-bob',
             'Russian Federation',
             'Medicine, Healthcare',
             '20210714',
             '08-07-2026',
             975.5,
             26.8)

bond2 = Bond(667,
             'RU000A1040V2',
             'Ohta-Group-BO-P02',
             'Russian Federation',
             'Real Estate',
             '20211116',
             '12-11-2024',
             975.5,
             31.16)

bond3 = Bond(441, 'RU000A104WZ7',
             "Электроаппарат БО-01",
             'Russian Federation',
             'Retail',
             '20220630',
             '28-09-2023',
             999.9,
             39.89)

bond4 = Bond(289, 'РНБАНК1Р10',
             'Авто Финанс Банк-001Р-10',
             'Russian Federation',
             'Banking',
             '20221129',
             '01-12-2025',
             960.2,
             53.15,
             )

bond5 = Bond(275, 'Реиннол1P2',
             'Реиннольц-001P-02',
             'Russian Federation',
             'Machine Building',
             '20221213',
             '08-12-2026',
             1068,
             44.88,)
