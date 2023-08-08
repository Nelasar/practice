import numpy as np

from stock import *
from bond import *
from PortfolioImpl import *
from numpystock import *
from loadfromyahoo import *
import pandas as pd
import yfinance as yf
from technical_analysis import *
from markovitz import *
from yahoostock import *
from sklearn.linear_model import LinearRegression
from vectorized import *
from market import *
from u import *
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import  QTableWidgetItem, QTableWidget, QWidget, QVBoxLayout, QLabel, QAbstractItemView
from PyQt5 import uic
import sys

mrkt = Market()
mrkvz = MarkovitzAnalyzer()

class newWindow(QWidget):
    def __init__(self, row_data):
        super().__init__()
        self.layout = QVBoxLayout()
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(len(row_data))
        self.tableWidget.setRowCount(1)
        for col, data in enumerate(row_data):
            self.tableWidget.setItem(0, col, QTableWidgetItem(data))

        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)
        self.coords = 0


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent=parent)
        self.setupUi(self)
        self.btnMarket.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_1))
        self.btnPortfolio.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_2))
        self.analBtn.clicked.connect(mrkvz.perform_analysis)

        self.tableWidget.setColumnWidth(0, 80)
        self.tableWidget.setColumnWidth(1, 315)
        self.tableWidget.setColumnWidth(2, 250)
        self.tableWidget.setColumnWidth(3, 80)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.sec_count = 0

        self.addBtn.setEnabled(False)
        self.description_window = QWidget()
        self.markovitz_window = QWidget()

        for asset in mrkt.allAssets():
            print(asset.getTicket(), asset.getName())
            rowPos = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPos)
            self.tableWidget.setItem(self.sec_count, 0, QTableWidgetItem(asset.getTicket()))
            self.tableWidget.setItem(self.sec_count, 1, QTableWidgetItem(asset.getName()))
            self.tableWidget.setItem(self.sec_count, 2, QTableWidgetItem("DESCRIPTION"))
            self.tableWidget.setItem(self.sec_count, 3, QTableWidgetItem(str(asset.getPrice())))
            self.sec_count += 1

        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)

        def cell_double_clicked(item):
            row_data = [self.tableWidget.item(item.row(), col).text() for col in range(self.tableWidget.columnCount())]
            new_window(row_data)

        def cell_clicked(item):
            self.addBtn.setEnabled(True)
            self.coords = item.row()

        def button_clicked():
            st = str(self.tableWidget.item(self.coords, 0).text())
            if mrkvz.check(st):
                print("IN!!!")
                #print(mrkvz.check())
                return
            else:
                mrkvz.addAsset(mrkt.getAsset(st))
                print(type(mrkt.getAsset(self.tableWidget.item(self.coords, 0).text())))
                print("ASSETS: ", mrkvz.getAssetsCount())



        def new_window(row_data):
            self.description_window = newWindow(row_data)
            self.description_window.resize(400, 400)
            self.description_window.setWindowTitle("Row Data")
            self.description_window.show()

        self.tableWidget.itemClicked.connect(cell_clicked)
        self.tableWidget.itemDoubleClicked.connect(cell_double_clicked)
        self.addBtn.clicked.connect(button_clicked)

if __name__ == "__main__":
    #stock1 = Stock("test stock1", 1234.34, 20)
    #stock2 = Stock("test stock2", 12334.34, 30)
    #stock3 = Stock("test stock3", 4343.33, 40)

    # UNCOMMENT!!!!
    #npstock1 = NPStock("npstock1", 434.43, 20)
    #npstock2 = NPStock("npstock2", 10234.3434, 34)
    #npstock3 = NPStock("npstock3", 5000, 434, 40)
    #npstock4 = NPStock("npstock4", 2700.459, 200)

    #bond1 = Bond("test bond1", 243.434, 15)
    #bond2 = Bond("test bond2", 434.434, 30)
    #bond3 = Bond("test bond3", 342.45, 45)

    """
    Тут создаются тестовые штуки классов для портфелей и ЦБ
    С этим кодом можешь как-то играть для гуи, разбирать его 
    
    print(stock1.getName(), stock1.getPrice(), stock1.getPriceHistory())
    print(stock2.getName(), stock2.getPrice(), stock2.getPriceHistory())
    print(stock3.getName(), stock3.getPrice(), stock3.getPriceHistory())

    print(bond1.getName(), bond1.getPrice(), bond1.getPriceHistory())
    print(bond2.getName(), bond2.getPrice(), bond2.getPriceHistory())
    print(bond3.getName(), bond3.getPrice(), bond3.getPriceHistory())

    test_portfolio = portfolio_initialization()

    test_portfolio.addSecurity(stock1)
    test_portfolio.addSecurity(stock2)
    test_portfolio.addSecurity(stock3)

    test_portfolio.addSecurity(bond1)
    test_portfolio.addSecurity(bond2)
    test_portfolio.addSecurity(bond3)

    test_portfolio.printSecurities()

    #print(npstock1.getNP())
    #print(npstock2.getNP())
    #print(npstock3.getNP())

    #printGraphHistory(npstock1)
    #printGraphHistory(npstock2)
    #printGraphHistory(npstock3)

    print(df)
    #df[["SMA 15", "SMA 60", "close"]].loc["2010"].plot(figsize=(15, 8))
    #print(df["SMA 15"])
    """
    """
    df = df[["close", 'SMA 15', 'SMA 60']].loc['2010']

    plt.figure(figsize=(10, 6))

    plt.plot(df['close'], label='values')
    plt.plot(df['SMA 15'], label='SPA 15')
    plt.plot(df['SMA 60'], label='SPA 60')

    plt.xlabel('Date')
    plt.ylabel('Values')
    plt.title('Generated Values over Time')
    plt.legend()
    plt.show()
    """
    """
    
    SMA(npstock1)
    MSD(npstock1)

    print(simple_analysis(npstock1))
    """
    """
    table.plot(figsize=(10, 5))
    plt.grid(True, linestyle='--')
    plt.legend(labelspacing=0.8)
    plt.tight_layout()
    plt.show()
    """

    """ НА ЭТОТ КОД ЗАБЕЙ ХУЙ
    
    # максимальный коэф шарпа
    max_sharpe = max_sharp_ratio(mean_returns, cov_matrix, risk_free_rate)
    # минимальный риск
    min_vol = min_variance(mean_returns, cov_matrix)

    sdp, rp = portfolio_annualised_performance(max_sharpe['x'], mean_returns, cov_matrix)
    max_sharpe_allocation = pd.DataFrame(max_sharpe.x, index=table.columns, columns=['allocation'])
    max_sharpe_allocation.allocation = [round(i * 100, 2) for i in max_sharpe_allocation.allocation]
    max_sharpe_allocation = max_sharpe_allocation.T

    sdp_min, rp_min = portfolio_annualised_performance(min_vol['x'], mean_returns, cov_matrix)
    min_vol_allocation = pd.DataFrame(min_vol.x, index=table.columns, columns=['allocation'])
    min_vol_allocation.allocation = [round(i * 100, 2) for i in min_vol_allocation.allocation]
    min_vol_allocation = min_vol_allocation.T

    target = np.linspace(rp_min, 0.017, 20)
    efficient_portfolios = efficient_frontier(mean_returns, cov_matrix, target)

    results, _ = random_portfolios(num_portfolios, mean_returns, cov_matrix, risk_free_rate)

    print("-" * 80)
    print("Распределение долей акций в портфеле с максимальным коэффициентом Шарпа:n")
    print("Годовая доходность:", round(rp, 3))
    print("Годовой риск:", round(sdp, 3))
    print("Коэффициент Шарпа", round((rp - risk_free_rate) / sdp, 3))
    print("\n")
    print(max_sharpe_allocation)
    print("-" * 80)
    print("Распределение долей акций в портфеле с наименьшим показателем риска:\n")
    print("Годовая доходность:", round(rp_min, 3))
    print("Годовой риск:", round(sdp_min, 3))
    print("Коэффициент Шарпа:", round((rp_min - risk_free_rate) / sdp_min, 3))
    print("\n")
    print(min_vol_allocation)

    plt.figure(figsize=(10, 7))
    plt.scatter(results[0, :], results[1, :], c=results[2, :], cmap='YlGnBu', marker='o', s=10, alpha=0.3)
    plt.colorbar(label='Коэффициент Шарпа')
    plt.scatter(sdp, rp, marker='*', color='r', s=500, label='Максимальный коэф-т Шарпа')
    plt.scatter(sdp_min, rp_min, marker='*', color='g', s=500, label='Минимальный риск')

    plt.plot([p['fun'] for p in efficient_portfolios], target, 'k-x', label='граница эффективности')
    plt.title('Оптимизация портфеля на основе построения эффективной границы')
    plt.xlabel('Риск(стандартное отклонение)')
    plt.ylabel('Доходность')
    plt.grid(True, linestyle='--')
    plt.legend(labelspacing=0.8)

    plt.tight_layout();
    plt.show()


    ind = np.arange(n_assets)
    width = 0.35

    plt.figure(figsize=(8, 6))
    plt.bar(ind, max_sharpe['x'], width, color='r', alpha=0.75)
    plt.bar(ind + width, min_vol['x'], width, color='b', alpha=0.75)

    plt.xticks(ind, stocks)
    plt.ylabel('Распределение акций в портфеле')
    plt.title('Сравнение сотавов портфелей')
    plt.legend(('Максимальный коэф-т Шарпа', 'Минимальный Риск'))
    plt.grid(visible=True, linestyle='--')

    plt.tight_layout()
    plt.show()
    """

    # ЗДЕСЬ ТЕСТЫ ПО ТА, МОЖЕШЬ НА ЭТОТ КОД ХУЙ ЗАБИТЬ И ЗАКОММЕНТИТЬ ПОКА
    """
    stocks = [npstock1, npstock2, npstock3, npstock4]
    names = [stock.getName() for stock in stocks]

    print(names)

    price = pd.DataFrame()
    for stock in stocks:
        price[stock.getName()] = stock.getHistory()

    print(price)
    print(price.shape)

    returns = price.pct_change()
    mean_returns = returns.mean()
    cov_matrix = returns.cov()

    max_sharpe = max_sharp_ratio(mean_returns, cov_matrix, risk_free_rate)
    min_vol = min_variance(mean_returns, cov_matrix)

    sdp, rp = portfolio_annualised_performance(max_sharpe['x'], mean_returns, cov_matrix)
    max_sharpe_allocation = pd.DataFrame(max_sharpe.x.copy(), index=price.columns, columns=['allocation'])
    max_sharpe_allocation.allocation = [round(i * 100, 2) for i in max_sharpe_allocation.allocation]
    max_sharpe_allocation = max_sharpe_allocation.T

    sdp_min, rp_min = portfolio_annualised_performance(min_vol['x'], mean_returns, cov_matrix)
    min_vol_allocation = pd.DataFrame(min_vol.x.copy(), index=price.columns, columns=['allocation'])
    min_vol_allocation.allocation = [round(i * 100, 2) for i in min_vol_allocation.allocation]
    min_vol_allocation = min_vol_allocation.T

    target = np.linspace(rp_min, 0.00081, 20)
    efficient_portfolios = efficient_frontier(mean_returns, cov_matrix, target)

    results, _ = random_portfolios(num_portfolios, mean_returns, cov_matrix, risk_free_rate)

    print("-" * 80)
    print("Распределение долей акций в портфеле с максимальным коэффициентом Шарпа:\n")
    print("Годовая доходность:", round(rp, 3))
    print("Годовой риск:", round(sdp, 3))
    print("Коэффициент Шарпа:", round((rp - risk_free_rate) / sdp, 3))
    print(max_sharpe_allocation)
    print("-" * 80)
    print("Распределение долей акций в портфеле с наименьшим показателем риска:\n")
    print("Годовая доходность:", round(rp_min, 3))
    print("Годовой риск:", round(sdp_min, 3))
    print("Коэффициент Шарпа:", round((rp_min - risk_free_rate) / sdp_min, 3))
    print(min_vol_allocation)

    plt.figure(figsize=(10, 7))
    plt.scatter(results[0, :], results[1, :], c=results[2, :], cmap='YlGnBu', marker='o', s=10, alpha=0.3)
    plt.colorbar(label='Коэффициент Шарпа:')
    plt.scatter(sdp, rp, marker='*', color='r', s=500, label='Максимальный коэф-т Шарпа')
    plt.scatter(sdp_min, rp_min, marker='*', color='g', s=500, label='Минимальный риск')

    plt.plot([p['fun'] for p in efficient_portfolios], target, 'k-x', label='граница эффективности')
    plt.title('Оптимизация портфеля на основе построения эффективной границы')
    plt.xlabel('Риск(стандартное отклонение)')
    plt.ylabel('Доходность')
    plt.grid(True, linestyle='--')
    plt.legend(labelspacing=0.8)

    plt.xlim(0.02, 0.028)
    plt.ylim(0.0001, 0.0009)

    plt.tight_layout();
    plt.show()

    ind = np.arange(price.columns.size)
    width = 0.35

    plt.figure(figsize=(8, 6))
    plt.bar(ind, max_sharpe['x'], width, color='r', alpha=0.75)
    plt.bar(ind + width, min_vol['x'], width, color='b', alpha=0.75)

    plt.xticks(ind, names)
    plt.ylabel('Распределение акций в портфеле')
    plt.title('Cравнение сотавов портфелей')
    plt.legend(('Максимальный коэф-т Шарпа', 'Минимальный Риск'))
    plt.grid(visible=True, linestyle='--')

    plt.tight_layout()
    plt.show()
    """

    #yfstock = yfStock("GOOG", "Google")
    #print(yfstock.getPriceHistory())
    #print(yfstock.getPrice())

    # ВОТ ЭТОТ КОД МОЛОДЕЦ
    """
    tickets = ["GOOG", "AMD", "^GSPC", "TEVA"]  # start="date", end="date", interval="1mo"
    ticks = yf.download(tickets, start='2020-07-24', end='2023-07-24')
    ticks = ticks[["Adj Close"]]

    #print(ticks)
    #print(ticks.shape)
    #print(ticks.head())

    also_ticks = yf.download(tickets)
    also_ticks = also_ticks[["Adj Close"]]
    also_ticks = also_ticks.dropna()#(inplace=True)

    #print(also_ticks)
    #print(also_ticks.shape)
    #print(also_ticks.head())

    num_portfolios = 10000
    risk_free_rate = 0.00   # ЭТО ЮЗЕР ДОЛЖЕН РЕГУЛИРОВАТЬ САМ
    num_periods_annually = 252

    returns = also_ticks.pct_change()
    mean_returns = returns.mean()
    cov_matrix = returns.cov()

    #print(mean_returns)
    #print(cov_matrix)

    max_sharpe = max_sharp_ratio(mean_returns, cov_matrix, risk_free_rate)
    min_vol = min_variance(mean_returns, cov_matrix)

    # print(max_sharpe)
    # print(min_vol)

    sdp, rp = portfolio_annualised_performance(max_sharpe['x'], mean_returns, cov_matrix)
    # print(sdp)
    # print(rp)

    max_sharpe_allocation = pd.DataFrame(max_sharpe.x.copy(), index=also_ticks.columns, columns=['allocation'])
    max_sharpe_allocation.allocation = [round(i * 100, 2) for i in max_sharpe_allocation.allocation]
    max_sharpe_allocation = max_sharpe_allocation.T

    sdp_min, rp_min = portfolio_annualised_performance(min_vol['x'], mean_returns, cov_matrix)
    # print(sdp_min)
    # print(rp_min)
    min_vol_allocation = pd.DataFrame(min_vol.x.copy(), index=also_ticks.columns, columns=['allocation'])
    # print(min_vol_allocation)
    min_vol_allocation.allocation = [round(i * 100, 2) for i in min_vol_allocation.allocation]
    min_vol_allocation = min_vol_allocation.T
    # print(min_vol_allocation)

    target = np.linspace(rp_min, 0.00081, 20)
    efficient_portfolios = efficient_frontier(mean_returns, cov_matrix, target)

    results, _ = random_portfolios(num_portfolios, mean_returns, cov_matrix, risk_free_rate, tickets)

    print(results)

    print("-" * 80)
    print("Распределение долей акций в портфеле с максимальным коэффициентом Шарпа:\n")
    print("Годовая доходность:", round(rp, 3))
    print("Годовой риск:", round(sdp, 3))
    print("Коэффициент Шарпа:", round((rp - risk_free_rate) / sdp, 3))
    print(max_sharpe_allocation)
    print("-" * 80)
    print("Распределение долей акций в портфеле с наименьшим показателем риска:\n")
    print("Годовая доходность:", round(rp_min, 3))
    print("Годовой риск:", round(sdp_min, 3))
    print("Коэффициент Шарпа:", round((rp_min - risk_free_rate) / sdp_min, 3))
    print(min_vol_allocation)

    plt.figure(figsize=(10, 7))
    plt.scatter(results[0, :], results[1, :], c=results[2, :], cmap='YlGnBu', marker='o', s=10, alpha=0.3)
    plt.colorbar(label='Коэффициент Шарпа:')
    plt.scatter(sdp, rp, marker='*', color='r', s=500, label='Максимальный коэф-т Шарпа')
    plt.scatter(sdp_min, rp_min, marker='*', color='g', s=500, label='Минимальный риск')

    plt.plot([p['fun'] for p in efficient_portfolios], target, 'k-x', label='граница эффективности')
    plt.title('Оптимизация портфеля на основе построения эффективной границы')
    plt.xlabel('Риск(стандартное отклонение)')
    plt.ylabel('Доходность')
    plt.grid(True, linestyle='--')
    plt.legend(labelspacing=0.8)

    plt.tight_layout();
    plt.show()

    ind = np.arange(also_ticks.columns.size)
    width = 0.35

    plt.figure(figsize=(8, 6))
    plt.bar(ind, max_sharpe['x'], width, color='r', alpha=0.75)
    plt.bar(ind + width, min_vol['x'], width, color='b', alpha=0.75)

    plt.xticks(ind, tickets)
    plt.ylabel('Распределение акций в портфеле')
    plt.title('Cравнение сотавов портфелей')
    plt.legend(('Максимальный коэф-т Шарпа', 'Минимальный Риск'))
    plt.grid(visible=True, linestyle='--')

    plt.tight_layout()
    plt.show()

    max_sharpe = max_sharp_ratio(mean_returns, cov_matrix, risk_free_rate)
    sdp, rp = portfolio_annualised_performance(max_sharpe['x'], mean_returns, cov_matrix)
    max_sharpe_allocation = pd.DataFrame(max_sharpe.x.copy(), index=also_ticks.columns, columns=['allocation'])
    max_sharpe_allocation.allocation = [round(i * 100, 2) for i in max_sharpe_allocation.allocation]
    max_sharpe_allocation = max_sharpe_allocation.T

    min_vol = min_variance(mean_returns, cov_matrix)
    sdp_min, rp_min = portfolio_annualised_performance(min_vol['x'], mean_returns, cov_matrix)
    min_vol_allocation = pd.DataFrame(min_vol.x.copy(), index=also_ticks.columns, columns=['allocation'])
    min_vol_allocation.allocation = [round(i * 100, 2) for i in min_vol_allocation.allocation]
    min_vol_allocation = min_vol_allocation.T

    an_vol = np.std(returns) * np.sqrt(num_periods_annually)
    an_rt = mean_returns * num_periods_annually

    target = np.linspace(rp_min, 0.00081, 20)
    efficient_portfolios = efficient_frontier(mean_returns, cov_matrix, target)

    print("-" * 80)
    print("Распределение долей акций в портфеле с максимальным коэффициентом Шарпа\n")
    print("Годовая доходность:", round(rp, 2))
    print("Годовой риск:", round(sdp, 2))
    print("Коэффициент Шарпа:", round((rp - risk_free_rate) / sdp, 3))
    print(max_sharpe_allocation)
    print("-" * 80)
    print("Распределение долей акций в портфеле с наименьшим показателем риска:\n")
    print("Годовая доходность:", round(rp_min, 2))
    print("Годовой риск:", round(sdp_min, 2))
    print("Коэффициент Шарпа:", round((rp_min - risk_free_rate) / sdp_min, 3))
    print(min_vol_allocation)
    print("-" * 80)

    print("Показатели доходности и риска каждой отдельной акции:\n")
    for i, txt in enumerate(also_ticks.columns):
        print(txt, ":", "годовая доходность:", round(an_rt[i], 2), ", годовой риск:", round(an_vol[i], 2))
    print("-" * 80)

    plt.subplots(figsize=(10, 7))

    for i, txt in enumerate(also_ticks.columns):
        plt.annotate(txt, (an_vol[i], an_rt[i]), xytext=(10, 0), textcoords='offset points')

    # coolwarm RdBu YlGnBu
    plt.scatter(results[0, :], results[1, :], c=results[2, :], cmap=cm.YlGnBu, marker='o', s=10, alpha=0.3)
    plt.colorbar(label='Коэффициент Шарпа')

    plt.scatter(sdp, rp, marker='s', color='r', s=150, label='Максимальный коэф-т Шарпа')
    plt.scatter(sdp_min, rp_min, marker='s', color='g', s=150, label='Минимальный риск')

    plt.scatter(an_vol, an_rt, marker='o', s=200, c='blue', edgecolors='black')

    plt.plot([p['fun'] for p in efficient_portfolios], target, 'k-x', linewidth=2, label='граница эффективности')
    plt.title('Оптимизация портфеля и показатели отдельный акций')
    plt.xlabel('Риск (стандартное отклонение)')
    plt.ylabel('Доходность')
    plt.legend(labelspacing=0.8)
    plt.grid(True, linestyle='--')

    #plt.xlim(0.02, 0.03)
    #plt.ylim(-0.0002, 0.0011)

    plt.tight_layout();
    plt.show()
    """

    #mrkt.printMarket()

    #portfolio = PortfolioImpl()

    #for asset in mrkt.allAssets():
    #    portfolio.addSecurity(asset)

    # WORKS
    #portfolio.printSecurities()

    # ('GOOG', 'MSFT', 'PYPL', 'QCOM', 'U')

    #portfolio.getStock('GOOG').setQuantity(23)
    #portfolio.getStock('MSFT').setQuantity(54)
    #portfolio.getStock('PYPL').setQuantity(60)
    #portfolio.getStock('QCOM').setQuantity(11)
    #portfolio.getStock('U').setQuantity(37)

    #print(portfolio.weighting())

    #mrkt.printMarket()

    print(mrkvz.getAssetsCount())
    # mrkvz.addAsset(mrkt.getAsset('GOOG'))
    print(mrkvz.getAssetsCount())
    # mrkvz.addAsset(mrkt.getAsset('PYPL'))
    print(mrkvz.getAssetsCount())
    # mrkvz.addAsset(mrkt.getAsset('MSFT'))
    print(mrkvz.getAssetsCount())
    #mrkvz.perform_analysis()

    app = QtWidgets.QApplication(sys.argv)

    window = Ui_MainWindow()#uic.loadUi('u.ui')
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
