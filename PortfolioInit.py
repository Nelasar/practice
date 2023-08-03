'''
# PortfolioInitialization.py
from priceable import *
from PortfolioImpl import *

def portfolio_initialization():
    portf = PortfolioImpl()
    #portf.addNewSecurityStorage("Bond")
    portf.addNewSecurityStorage("Stock")

    return portf
'''