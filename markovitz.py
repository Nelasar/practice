import pandas as pd
import numpy as np
import scipy.optimize as sco
import matplotlib.pyplot as plt
import matplotlib.cm as cm

plt.rc('axes', axisbelow=True)
class MarkovitzAnalyzer:
    def __init__(self):
        self.tickets = []
        self.assets = pd.DataFrame()
        self.num_portfolios = 10000
        self.risk_free_rate = 0.0
        self.num_periods_annually = 252

        self.start = ''
        self.end = ''

        self.returns = pd.DataFrame()
        self.mean_returns = pd.DataFrame()
        self.cov_matrix = pd.DataFrame()

        #self.year_income_max_sharpe = 0
        #self.year_risk_max_sharpe = 0
        #self.sharpe_ratio = 0
        #self.year_income_min_risk = 0
        #self.year_risk_min_risk = 0
        #self.min_sharpe = 0
    def getAssetsCount(self):
        return len(self.tickets)

    def addTicketName(self, ticket):
        self.tickets.append(ticket)

    def checkTicket(self, ticket):
        if ticket in self.tickets:
            return True
        else:
            return False

    def check(self, ticket):
        for t in self.tickets:
            if t == ticket:
                return True
        return False
    def addAsset(self, asset):
        self.assets[asset.getTicket()] = asset.getPriceHistory()
        self.tickets.append(asset.getTicket())
        print("TICKETS:", self.tickets)
        print(self.assets)

    def removeAsset(self, asset):
        self.assets = self.assets.drop(str(asset), axis=1)
        self.tickets.remove(asset)
        print("TICKETS:", self.tickets)
        print(self.assets)

    def printTickets(self):
        print(self.tickets)

    def print(self):
        print(self.assets)

    def getAsset(self, ticket):
        for asset in self.assets:
            if asset.getTicket() == ticket:
                return asset

    def setPeriod(self, start, end):
        self.start = start
        self.end = end

    def setup(self):
        self.assets = self.assets.dropna()
        self.returns = self.assets.pct_change()
        self.mean_returns = self.returns.mean()
        self.cov_matrix = self.returns.cov()

    def portfolio_annualised_performance(self, weights, mean_returns, cov_matrix):
        returns = np.sum(mean_returns * weights) * self.num_periods_annually
        std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(self.num_periods_annually)

        return std, returns

    def neg_sharp_ratio(self, weights, mean_returns, cov_matrix, risk_free_rate):
        p_var, p_ret = self.portfolio_annualised_performance(weights, mean_returns, cov_matrix)

        return -(p_ret - risk_free_rate) / p_var

    def max_sharp_ratio(self, mean_returns, cov_matrix, risk_free_rate):
        num_assets = len(mean_returns)
        args = (mean_returns, cov_matrix, risk_free_rate)
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bound = (0.0, 1.0)
        bounds = tuple(bound for asset in range(num_assets))

        result = sco.minimize(self.neg_sharp_ratio, num_assets * [1. / num_assets, ], args=args,
                              method='SLSQP', bounds=bounds, constraints=constraints)

        return result

    # Также можно определить оптимизирующую функцию для расчета минимального показателя риска.
    # #На этот раз минимизируем целевую функцию – риск (min_variance), используя разные показатели долей акций.
    # #"Constraints" и "bounds" такие же, как и выше.

    def portfolio_volatility(self, weights, mean_returns, cov_matrix):
        return self.portfolio_annualised_performance(weights, mean_returns, cov_matrix)[0]

    def min_variance(self, mean_returns, cov_matrix):
        num_assets = len(mean_returns)
        args = (mean_returns, cov_matrix)
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bound = (0.0, 1.0)
        bounds = tuple(bound for asset in range(num_assets))

        result = sco.minimize(self.portfolio_volatility, num_assets * [1. / num_assets, ], args=args,
                              method='SLSQP', bounds=bounds, constraints=constraints)

        return result

    def efficient_return(self, mean_returns, cov_matrix, target):
        num_assets = len(mean_returns)
        args = (mean_returns, cov_matrix)

        def portfolio_return(weights):
            return self.portfolio_annualised_performance(weights, mean_returns, cov_matrix)[1]

        constraints = ({'type': 'eq', 'fun': lambda x: portfolio_return(x) - target},
                       {'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bounds = tuple((0, 1) for asset in range(num_assets))
        result = sco.minimize(self.portfolio_volatility, num_assets * [1. / num_assets, ], args=args,
                              method='SLSQP', bounds=bounds, constraints=constraints)
        return result

    def efficient_frontier(self, mean_returns, cov_matrix, returns_range):
        efficients = []
        for ret in returns_range:
            efficients.append(self.efficient_return(mean_returns, cov_matrix, ret))
        return efficients

    def random_portfolios(self, num_portfolios, mean_returns, cov_matrix, risk_free_rate, stocks):
        results = np.zeros((3, num_portfolios))
        weights_record = []
        for i in range(num_portfolios):
            weights = np.random.random(len(stocks))
            weights /= np.sum(weights)
            weights_record.append(weights)
            portfolio_std_dev, portfolio_return = self.portfolio_annualised_performance(weights, mean_returns,
                                                                                        cov_matrix)
            results[0, i] = portfolio_std_dev
            results[1, i] = portfolio_return
            results[2, i] = (portfolio_return - risk_free_rate) / portfolio_std_dev

        return results, weights_record

    def perform_analysis(self):
        if len(self.tickets) == 0:
            return

        self.setup()
        max_sharpe = self.max_sharp_ratio(self.mean_returns, self.cov_matrix, self.risk_free_rate)
        min_vol = self.min_variance(self.mean_returns, self.cov_matrix)

        sdp, rp = self.portfolio_annualised_performance(max_sharpe['x'], self.mean_returns, self.cov_matrix)

        max_sharpe_allocation = pd.DataFrame(max_sharpe.x.copy(), index=self.assets.columns, columns=['allocation'])
        max_sharpe_allocation.allocation = [round(i * 100, 2) for i in max_sharpe_allocation.allocation]
        max_sharpe_allocation = max_sharpe_allocation.T

        sdp_min, rp_min = self.portfolio_annualised_performance(min_vol['x'], self.mean_returns, self.cov_matrix)
        min_vol_allocation = pd.DataFrame(min_vol.x.copy(), index=self.assets.columns, columns=['allocation'])
        min_vol_allocation.allocation = [round(i * 100, 2) for i in min_vol_allocation.allocation]
        min_vol_allocation = min_vol_allocation.T

        target = np.linspace(rp_min, 0.00081, 20)
        efficient_portfolios = self.efficient_frontier(self.mean_returns, self.cov_matrix, target)

        results, _ = self.random_portfolios(
            self.num_portfolios, self.mean_returns, self.cov_matrix, self.risk_free_rate, self.tickets)


        print("-" * 80)
        print("Распределение долей акций в портфеле с максимальным коэффициентом Шарпа:\n")
        print("Годовая доходность:", round(rp, 3))
        #self.year_income_max_sharpe = round(rp, 3)
        print("Годовой риск:", round(sdp, 3))
        #self.year_risk_max_sharpe = round(sdp, 3)
        print("Коэффициент Шарпа:", round((rp - self.risk_free_rate) / sdp, 3))
        #self.sharpe_ratio = round((rp - self.risk_free_rate) / sdp, 3)
        print(max_sharpe_allocation)
        print("-" * 80)
        print("Распределение долей акций в портфеле с наименьшим показателем риска:\n")
        print("Годовая доходность:", round(rp_min, 3))
        #self.year_income_min_risk = round(rp_min, 3)
        print("Годовой риск:", round(sdp_min, 3))
        #self.year_risk_min_risk = round(sdp_min, 3)
        print("Коэффициент Шарпа:", round((rp_min - self.risk_free_rate) / sdp_min, 3))
        #self.min_sharpe = round((rp_min - self.risk_free_rate) / sdp_min, 3)
        print(min_vol_allocation)

        ind = np.arange(self.assets.columns.size)
        width = 0.35

        '''
        max_sharpe = self.max_sharp_ratio(self.mean_returns, self.cov_matrix, self.risk_free_rate)
        sdp, rp = self.portfolio_annualised_performance(max_sharpe['x'], self.mean_returns, self.cov_matrix)
        max_sharpe_allocation = pd.DataFrame(max_sharpe.x.copy(), index=self.assets.columns, columns=['allocation'])
        max_sharpe_allocation.allocation = [round(i * 100, 2) for i in max_sharpe_allocation.allocation]
        max_sharpe_allocation = max_sharpe_allocation.T

        min_vol = self.min_variance(self.mean_returns, self.cov_matrix)
        sdp_min, rp_min = self.portfolio_annualised_performance(min_vol['x'], self.mean_returns, self.cov_matrix)
        min_vol_allocation = pd.DataFrame(min_vol.x.copy(), index=self.assets.columns, columns=['allocation'])
        min_vol_allocation.allocation = [round(i * 100, 2) for i in min_vol_allocation.allocation]
        min_vol_allocation = min_vol_allocation.T

        an_vol = np.std(self.returns) * np.sqrt(self.num_periods_annually)
        an_rt = self.mean_returns * self.num_periods_annually

        target = np.linspace(rp_min, 0.00081, 20)
        efficient_portfolios = self.efficient_frontier(self.mean_returns, self.cov_matrix, target)

        print("-" * 80)
        print("Распределение долей акций в портфеле с максимальным коэффициентом Шарпа\n")
        print("Годовая доходность:", round(rp, 2))
        print("Годовой риск:", round(sdp, 2))
        print("Коэффициент Шарпа:", round((rp - self.risk_free_rate) / sdp, 3))
        print(max_sharpe_allocation)
        print("-" * 80)
        print("Распределение долей акций в портфеле с наименьшим показателем риска:\n")
        print("Годовая доходность:", round(rp_min, 2))
        print("Годовой риск:", round(sdp_min, 2))
        print("Коэффициент Шарпа:", round((rp_min - self.risk_free_rate) / sdp_min, 3))
        print(min_vol_allocation)
        print("-" * 80)

        print("Показатели доходности и риска каждой отдельной акции:\n")
        for i, txt in enumerate(self.assets.columns):
            print(txt, ":", "годовая доходность:", round(an_rt[i], 2), ", годовой риск:", round(an_vol[i], 2))
        print("-" * 80)

        plt.subplots(figsize=(10, 7))

        for i, txt in enumerate(self.assets.columns):
            plt.annotate(txt, (an_vol[i], an_rt[i]), xytext=(10, 0), textcoords='offset points')

        # coolwarm RdBu YlGnBu
        plt.scatter(results[0, :], results[1, :], c=results[2, :], cmap=cm.YlGnBu, marker='o', s=10, alpha=0.3)
        plt.colorbar(label='Коэффициент Шарпа')

        plt.scatter(sdp, rp, marker='s', color='r', s=150, label='Максимальный коэф-т Шарпа')
        plt.scatter(sdp_min, rp_min, marker='s', color='g', s=150, label='Минимальный риск')

        plt.scatter(an_vol, an_rt, marker='o', s=200, c='blue', edgecolors='black')

        plt.plot([p['fun'] for p in efficient_portfolios], target, 'k-x', linewidth=2,
                 label='граница эффективности')
        plt.title('Оптимизация портфеля и показатели отдельный акций')
        plt.xlabel('Риск (стандартное отклонение)')
        plt.ylabel('Доходность')
        plt.legend(labelspacing=0.8)
        plt.grid(True, linestyle='--')

        # plt.xlim(0.02, 0.03)
        # plt.ylim(-0.0002, 0.0011)

        plt.tight_layout();
        plt.show()
        
        '''

        return [round(rp, 3), round(sdp, 3),
                round((rp - self.risk_free_rate) / sdp, 3), round(rp_min, 3),
                round(sdp_min, 3), round((rp_min - self.risk_free_rate) / sdp_min, 3),
                results, efficient_portfolios, target,
                ind, width,
                max_sharpe, min_vol]
