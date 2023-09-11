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

        self.type = "Bond"

        self.ticket = b_tick
        self.name = b_name
        self.country = b_country
        self.industry = b_industry
        self.quantity = 0
        self.price = price
        self.maturity_date = b_date
        self.dividends = b_divs

        n = b_n #random.randint(100, 10000)

        self.price_history = GBM(n, T, r, q, sigma, self.price)
        self.price = round(self.price_history[-1], 4)
        self.low = self.price - 1.342
        self.high = self.price + 2.74
        self.open = self.price

        dates = pd.date_range(b_start_date, '20230913')
        self.price_history = pd.DataFrame(self.price_history, index=dates, columns=["close"])

        self.info = {'Ticket':    self.ticket,
                     'Name':      self.name,
                     'Country':   self.country,
                     'Industry':  self.industry,
                     'Price':     str(self.price),
                     'Low':       self.low,
                     'High':      self.high,
                     'Open':      self.open,
                     'Dividends': self.dividends,
                     'Maturity':  self.maturity_date}

    def __str__(self):
        return f"Information:\nTicker: {self.ticket}\n" \
                f"Company Name: {self.name}\n" \
                f"Country: {self.country}\n" \
                f"Current Price: {self.price}\n" \
                f"Industry: {self.industry}\n"

    def getInfoValues(self, key=None):
        if key is None:
            return self.info
        else:
            return self.info[key]

    def getTicket(self):
        return self.ticket

    def getName(self):
        return self.name

    def getPrice(self):
        return self.price

    def getQuantity(self):
        return self.quantity

    def changeQuantity(self, change):
        self.quantity += change

    def setPrice(self, p):
        self.price = p

    def getPriceHistory(self):
        return self.price_history

    def getType(self):
        return self.type


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
