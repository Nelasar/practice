import pandas as pd
import numpy as np
import scipy.optimize as sco
import matplotlib.pyplot as plt


plt.rc('axes', axisbelow=True)
class MarkowitzAnalyzer:
    def __init__(self, num_portfolios=10000, risk_free_rate=0.0):
        self.__tickets = []
        self.__assets_copies = []
        self.__assets = pd.DataFrame()

        self.__num_portfolios = num_portfolios
        self.__risk_free_rate = risk_free_rate
        self.__num_periods_annually = 252

        self.__returns = pd.DataFrame()
        self.__mean_returns = pd.DataFrame()
        self.__cov_matrix = pd.DataFrame()

    def set_options(self, num_portfolios, risk_rate):
        self.__num_portfolios = num_portfolios
        self.__risk_free_rate = risk_rate

    def getAssetsCount(self):
        return len(self.__tickets)

    def checkTicket(self, ticket):
        if ticket in self.__tickets:
            return True
        else:
            return False

    def check(self, ticket):
        for t in self.__tickets:
            if t == ticket:
                return True
        return False

    def addAsset(self, asset):
        self.__assets_copies.append(asset)
        self.__assets[asset.getTicket()] = asset.getPriceHistory()
        print(asset.getPriceHistory())
        self.__tickets.append(asset.getTicket())
        print("TICKETS:", self.__tickets)
        print("COPIES:", self.__assets_copies)
        print(self.__assets)

    def removeAsset(self, asset):
        self.__assets = self.__assets.drop(str(asset), axis=1)
        for ast in self.__assets_copies:
            if ast.getTicket() == asset:
                self.__assets_copies.remove(ast)
        self.__tickets.remove(asset)
        print("TICKETS:", self.__tickets)
        print("COPIES:\n", self.__assets_copies)
        print("DATAFRAME:\n", self.__assets)

    def clearAnalyzer(self):
        self.__assets = pd.DataFrame()
        self.__assets_copies.clear()
        self.__tickets.clear()
        print("TICKETS:", self.__tickets)
        print("ASSET COPIES:", self.__assets_copies)
        print(self.__assets)

    def printTickets(self):
        print(self.__tickets)

    def print(self):
        print(self.__assets)

    def getAsset(self, ticket):
        for asset in self.__assets:
            if asset.getTicket() == ticket:
                return asset

    def __setup(self):
        self.__assets = pd.DataFrame()
        for asset in self.__assets_copies:
            self.__assets[asset.getTicket()] = asset.getPriceHistory()

        self.__assets = self.__assets.dropna()
        self.__returns = self.__assets.pct_change()
        self.__mean_returns = self.__returns.mean()
        self.__cov_matrix = self.__returns.cov()

    def __portfolio_annualised_performance(self, weights, mean_returns, cov_matrix):
        returns = np.sum(mean_returns * weights) * self.__num_periods_annually
        std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(self.__num_periods_annually)

        return std, returns

    def __neg_sharp_ratio(self, weights, mean_returns, cov_matrix, risk_free_rate):
        p_var, p_ret = self.__portfolio_annualised_performance(weights, mean_returns, cov_matrix)

        return -(p_ret - risk_free_rate) / p_var

    def __max_sharp_ratio(self, mean_returns, cov_matrix, risk_free_rate):
        num_assets = len(mean_returns)
        args = (mean_returns, cov_matrix, risk_free_rate)
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bound = (0.0, 1.0)
        bounds = tuple(bound for asset in range(num_assets))

        result = sco.minimize(self.__neg_sharp_ratio, num_assets * [1. / num_assets, ], args=args,
                              method='SLSQP', bounds=bounds, constraints=constraints)

        return result

    # Также можно определить оптимизирующую функцию для расчета минимального показателя риска.
    # #На этот раз минимизируем целевую функцию – риск (min_variance), используя разные показатели долей акций.
    # #"Constraints" и "bounds" такие же, как и выше.

    def __portfolio_volatility(self, weights, mean_returns, cov_matrix):
        return self.__portfolio_annualised_performance(weights, mean_returns, cov_matrix)[0]

    def __min_variance(self, mean_returns, cov_matrix):
        num_assets = len(mean_returns)
        args = (mean_returns, cov_matrix)
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bound = (0.0, 1.0)
        bounds = tuple(bound for asset in range(num_assets))

        result = sco.minimize(self.__portfolio_volatility, num_assets * [1. / num_assets, ], args=args,
                              method='SLSQP', bounds=bounds, constraints=constraints)

        return result

    def __efficient_return(self, mean_returns, cov_matrix, target):
        num_assets = len(mean_returns)
        args = (mean_returns, cov_matrix)

        def portfolio_return(weights):
            return self.__portfolio_annualised_performance(weights, mean_returns, cov_matrix)[1]

        constraints = ({'type': 'eq', 'fun': lambda x: portfolio_return(x) - target},
                       {'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bounds = tuple((0, 1) for asset in range(num_assets))
        result = sco.minimize(self.__portfolio_volatility, num_assets * [1. / num_assets, ], args=args,
                              method='SLSQP', bounds=bounds, constraints=constraints)
        return result

    def __efficient_frontier(self, mean_returns, cov_matrix, returns_range):
        efficients = []
        for ret in returns_range:
            efficients.append(self.__efficient_return(mean_returns, cov_matrix, ret))
        return efficients

    def __random_portfolios(self, num_portfolios, mean_returns, cov_matrix, risk_free_rate, stocks):
        results = np.zeros((3, num_portfolios))
        weights_record = []
        for i in range(num_portfolios):
            weights = np.random.random(len(stocks))
            weights /= np.sum(weights)
            weights_record.append(weights)
            portfolio_std_dev, portfolio_return = self.__portfolio_annualised_performance(weights, mean_returns,
                                                                                        cov_matrix)
            results[0, i] = portfolio_std_dev
            results[1, i] = portfolio_return
            results[2, i] = (portfolio_return - risk_free_rate) / portfolio_std_dev

        return results, weights_record

    def perform_analysis(self, ):
        if len(self.__tickets) == 0:
            return

        self.__setup()
        max_sharpe = self.__max_sharp_ratio(self.__mean_returns, self.__cov_matrix, self.__risk_free_rate)
        min_vol = self.__min_variance(self.__mean_returns, self.__cov_matrix)

        sdp, rp = self.__portfolio_annualised_performance(max_sharpe['x'], self.__mean_returns, self.__cov_matrix)
        max_sharpe_allocation = pd.DataFrame(max_sharpe.x.copy(), index=self.__assets.columns, columns=['allocation'])
        max_sharpe_allocation.allocation = [round(i * 100, 2) for i in max_sharpe_allocation.allocation]
        max_sharpe_allocation = max_sharpe_allocation.T

        sdp_min, rp_min = self.__portfolio_annualised_performance(min_vol['x'], self.__mean_returns, self.__cov_matrix)
        min_vol_allocation = pd.DataFrame(min_vol.x.copy(), index=self.__assets.columns, columns=['allocation'])
        min_vol_allocation.allocation = [round(i * 100, 2) for i in min_vol_allocation.allocation]
        min_vol_allocation = min_vol_allocation.T

        target = np.linspace(rp_min, 0.00081, 20)
        efficient_portfolios = self.__efficient_frontier(self.__mean_returns, self.__cov_matrix, target)

        results, _ = self.__random_portfolios(
            self.__num_portfolios, self.__mean_returns, self.__cov_matrix, self.__risk_free_rate, self.__tickets)

        ind = np.arange(self.__assets.columns.size)
        width = 0.35

        return { 'year_profit_max_sharpe': round(rp, 3),
                 'year_risk_max_sharpe': round(sdp, 3),
                 'sharpe_max_sharpe': round((rp - self.__risk_free_rate) / sdp, 3),
                 'year_profit_min_vol': round(rp_min, 3),
                 'year_risk_min_vol': round(sdp_min, 3),
                 'sharpe_min_vol': round((rp_min - self.__risk_free_rate) / sdp_min, 3), # 5
                 'results': results, 'efficient_portfolios': efficient_portfolios,
                 'target': target,
                 'index': ind, 'width': width, 'max_sharpe': max_sharpe,
                 'min_vol': min_vol, 'asset_count': self.getAssetsCount(),
                 'tickets': self.__tickets, 'min_vol_alloc': min_vol_allocation,
                 'max_sharpe_alloc': max_sharpe_allocation
                }
