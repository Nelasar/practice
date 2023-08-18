from market import Market
from linearregression import StockAnalysis
from markovitz import MarkowitzAnalyzer
from PortfolioImpl import PortfolioImpl


class Creator:
    def create_market(self):
        return Market()

    def create_portfolio(self):
        return PortfolioImpl()

    def create_markovitz(self, num_portfolios=10000, risk_free_rate=0.0, num_periods_annually=252):
        return MarkowitzAnalyzer()

    def create_analyzer(self, asset):
        return StockAnalysis(asset)