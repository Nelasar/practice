from PortfolioImpl import *
import pandas as pd
from technical_analysis import *
from markovitz import *
from yahoostock import *
from sklearn.linear_model import LinearRegression
from vectorized import *
from market import *
from u import *
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QTableWidgetItem, QTableWidget, QWidget, QVBoxLayout, QLabel, QAbstractItemView, QGridLayout
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QIntValidator
from PyQt5 import uic
from pyqtgraph import PlotWidget, plot, Qt
import pyqtgraph as pg
from pyqtgraph import DateAxisItem
import sys
from MarketGUI import BuyWindow, InfoWindow, AnalysisWindow
from linearregression import StockAnalysis

mrkt = Market()
mrkvz = MarkowitzAnalyzer()
portf = PortfolioImpl()

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent=parent)
        self.setupUi(self)
        self.btnMarket.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_1))
        self.btnPortfolio.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_2))

        # ТАБЛИЦА РЫНКА
        header = self.tableMarket.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.tableMarket.setColumnWidth(1, 315)
        self.tableMarket.setColumnWidth(2, 250)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        self.tableMarket.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        # ТАБЛИЦА ПОРТФЕЛЯ
        header = self.tablePortfolio.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.tablePortfolio.setColumnWidth(1, 315)
        self.tablePortfolio.setColumnWidth(2, 250)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        self.tablePortfolio.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.addBtnMarket.setEnabled(False)
        self.removeButton.setEnabled(False)
        self.addBtnPortf.setEnabled(False)

        self.description_window = QWidget()
        self.markovitz_window = QWidget()
        self.information_window = QWidget()
        self.buy_window = QWidget()

        # ЗАПОЛНЕНИЕ ТАБЛИЦЫ РЫНКА
        count = 0
        for asset in mrkt.allAssets():
            print(asset.getTicket(), asset.getName())
            row_pos = self.tableMarket.rowCount()
            asset_info = asset.getInfoValues()
            self.tableMarket.insertRow(row_pos)
            self.tableMarket.setItem(count, 0, QTableWidgetItem(asset_info['ticket']))
            self.tableMarket.setItem(count, 1, QTableWidgetItem(asset_info['name']))
            self.tableMarket.setItem(count, 2, QTableWidgetItem(asset_info['industry']))
            self.tableMarket.setItem(count, 3, QTableWidgetItem(asset_info['price']))
            count += 1

        '''
        # ЗАПОЛНЕНИЕ ТАБЛИЦЫ ПОРТФЕЛЯ
        #count = 0
        for asset in portf.allSecuritiesByKey('Stock'):
            print(asset.getTicket(), asset.getName())
            row_pos = self.tablePortfolio.rowCount()
            asset_info = asset.getInfoValues()
            self.tablePortfolio.insertRow(row_pos)
            self.tablePortfolio.setItem(count, 0, QTableWidgetItem(asset_info['ticket']))
            self.tablePortfolio.setItem(count, 1, QTableWidgetItem(asset_info['name']))
            self.tablePortfolio.setItem(count, 2, QTableWidgetItem(asset_info['industry']))
            self.tablePortfolio.setItem(count, 3, QTableWidgetItem(asset_info['price']))
            self.tablePortfolio.setItem((count, 4, QTableWidgetItem(asset.getQuantity())))
            count += 1
        '''

        # КЛИКИ НА ТАБЛИЦЫ
        self.tableMarket.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableMarket.setSelectionMode(QAbstractItemView.SingleSelection)

        self.tablePortfolio.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tablePortfolio.setSelectionMode(QAbstractItemView.SingleSelection)

        self.tableAnalysis.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableAnalysis.setSelectionMode(QAbstractItemView.SingleSelection)

        # ФУНКЦИИ ПОВЕДЕНИЯ
        # ДВОЙНОЕ НАЖАТИЕ НА РЫНКЕ
        def cell_double_clicked(item):
            security = mrkt.getAsset(self.tableMarket.item(item.row(), 0).text())
            info_window(security)
            # row_data = [self.tableWidget.item(item.row(), col).text() for col in range(self.tableWidget.columnCount())]
            # new_window(row_data)

        # НАЖАТИЕ НА РЫНКЕ
        def cell_clicked(item):
            ticket = str(self.tableMarket.item(item.row(), 0).text())
            if mrkvz.checkTicket(ticket):
                self.addBtnMarket.setEnabled(False)
                self.addBtnPortf.setEnabled(False)
            else:
                self.addBtnMarket.setEnabled(True)
                self.addBtnPortf.setEnabled(True)
            self.coords = item.row()
            self.removeButton.setEnabled(False)

        # ВЫБРАН ЭЛЕМЕНТ ТАБЛИЦЫ МАРКОВИЦА
        def analysis_cell_clicked(item):
            self.addBtnMarket.setEnabled(False)
            self.addBtnPortf.setEnabled(False)
            self.removeButton.setEnabled(True)
            currentRow = self.tableAnalysis.currentRow()
            ticket = str(self.tableAnalysis.item(currentRow, 0).text())
            print(currentRow, ticket)

        # УДАЛИТЬ ИЗ ТАБЛИЦЫ МАРКОВИЦА
        def remove_button_clicked():
            currentRow = self.tableAnalysis.currentRow()
            ticket = str(self.tableAnalysis.item(currentRow, 0).text())
            print(currentRow, ticket)
            self.tableAnalysis.removeRow(currentRow)
            mrkvz.removeAsset(ticket)
            self.removeButton.setEnabled(False)

        # ДОБАВИТЬ В ТАБЛИЦУ МАРКОВИЦА С РЫНКА
        def market_add_button_clicked():
            st = str(self.tableMarket.item(self.coords, 0).text())
            if mrkvz.check(st):
                print("IN!!!")
                return
            else:
                mrkvz.addAsset(mrkt.getAsset(st))
                row_position = self.tableAnalysis.rowCount()
                self.tableAnalysis.insertRow(row_position)
                self.tableAnalysis.setItem(row_position, 0, QTableWidgetItem(st))
                self.addBtnMarket.setEnabled(False)
                print(type(mrkt.getAsset(self.tableMarket.item(self.coords, 0).text())))
                print("ASSETS: ", mrkvz.getAssetsCount())

        # НАЖАТА КНОПКА АНАЛИЗ
        def analysis_button_clicked():
            analysis_data = mrkvz.perform_analysis()
            new_analysis_window(analysis_data)

        # ОТКРЫТИЕ ОКНА АНАЛИЗА
        def new_analysis_window(analysis_data):
            self.markovitz_window = AnalysisWindow(analysis_data)
            self.markovitz_window.show()

        def info_window(security):
            self.information_window = InfoWindow(security)
            self.information_window.show()

        def buy_button_clicked():
            currentRow = self.tableMarket.currentRow()
            ticket = str(self.tableMarket.item(currentRow, 0).text())
            asset = mrkt.getAsset(ticket)

            self.buy_window = BuyWindow()
            self.buy_window.show()
            if self.buy_window.exec_() == QDialog.Accepted:
                input_value = self.buy_window.get_input_value()
                if input_value is not None:
                    portf.addSecurityWithQuantity(asset, input_value)
                    a_info = asset.getInfoValues()
                    portfolio_row = self.tablePortfolio.rowCount()
                    self.tablePortfolio.insertRow(portfolio_row)
                    self.tablePortfolio.setItem(portfolio_row, 0, QTableWidgetItem(a_info['ticket']))
                    self.tablePortfolio.setItem(portfolio_row, 1, QTableWidgetItem(a_info['name']))
                    self.tablePortfolio.setItem(portfolio_row, 2, QTableWidgetItem(a_info['industry']))
                    self.tablePortfolio.setItem(portfolio_row, 3, QTableWidgetItem(a_info['price']))
                    self.tablePortfolio.setItem(portfolio_row, 4, QTableWidgetItem(str(asset.getQuantity())))

        def portfolio_cell_double_clicked(item):
            security = portf.getStock(self.tablePortfolio.item(item.row(), 0).text())
            info_window(security)

        def add_button_clicked_portfolio():
            pass

        def sell_button_clicked():
            pass

        def info_window_portfolio(security):
            pass

        # ПОВЕДЕНИЕ ОБЩИХ ЭЛЕМЕНТОВ
        self.tableAnalysis.itemClicked.connect(analysis_cell_clicked)
        self.removeButton.clicked.connect(remove_button_clicked)

        # ПОВЕДЕНИЕ ТАБЛИЦЫ РЫНКА
        self.tableMarket.itemClicked.connect(cell_clicked)
        self.tableMarket.itemDoubleClicked.connect(cell_double_clicked)
        self.addBtnMarket.clicked.connect(market_add_button_clicked)
        self.analBtnMarket.clicked.connect(analysis_button_clicked)
        self.btnBuy.clicked.connect(buy_button_clicked)

        # ПОВЕДЕНИЕ ТАБЛИЦЫ ПОРТФЕЛЯ
        self.tablePortfolio.itemClicked.connect(cell_clicked)
        self.tablePortfolio.itemDoubleClicked.connect(portfolio_cell_double_clicked)
        self.analBtnPortf.clicked.connect(analysis_button_clicked)
        self.addBtnPortf.clicked.connect(add_button_clicked_portfolio)
        self.sellBtnPortf.clicked.connect(sell_button_clicked)

if __name__ == "__main__":
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
    # ВОТ ЭТОТ КОД МОЛОДЕЦ
    """
    tickets = ["GOOG", "AMD", "^GSPC", "TEVA"]  # start="date", end="date", interval="1mo"
    ticks = yf.download(tickets, start='2020-07-24', end='2023-07-24')
    ticks = ticks[["Adj Close"]]
    """

    app = QtWidgets.QApplication(sys.argv)

    window = Ui_MainWindow()  # uic.loadUi('u.ui')
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
