from PortfolioImpl import *
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
from PyQt5.QtWidgets import QTableWidgetItem, QTableWidget, QWidget, QVBoxLayout, QLabel, QAbstractItemView, QGridLayout
from PyQt5.QtGui import QColor
from PyQt5 import uic
from pyqtgraph import PlotWidget, plot, Qt
import pyqtgraph as pg
from pyqtgraph import DateAxisItem
import sys

mrkt = Market()
mrkvz = MarkovitzAnalyzer()
portf = PortfolioImpl()

'''
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
'''


class InfoWindow(QWidget):
    def __init__(self, asset):
        super().__init__()
        self.layout = QGridLayout(self)
        self.history = asset.getPriceHistory()

        x = self.history.index
        x = x.to_pydatetime().tolist()
        y = self.history.values.flatten()
        x_float = [date.timestamp() for date in x]

        self.plot_widget = pg.PlotWidget(axisItems={'bottom': DateAxisItem()})
        self.plot_widget.setLabel('bottom', 'X')
        self.plot_widget.setLabel('left', 'Y')
        self.layout.addWidget(self.plot_widget, 0, 0, 1, 1)

        self.line_plot = pg.PlotCurveItem()
        self.line_plot.setData(x=x_float, y=y, pen=(0, 255, 0))
        self.plot_widget.addItem(self.line_plot)

        table = QTableWidget(8, 2)
        table.setHorizontalHeaderLabels(["Параметр", "Значение"])
        self.layout.addWidget(table, 0, 1, 1, 1)

        table.setItem(0, 0, QTableWidgetItem("Ticket"))
        table.setItem(1, 0, QTableWidgetItem("Name"))
        table.setItem(2, 0, QTableWidgetItem("Country"))
        table.setItem(3, 0, QTableWidgetItem("Industry"))
        table.setItem(4, 0, QTableWidgetItem("Price"))
        table.setItem(5, 0, QTableWidgetItem("Beta"))
        table.setItem(6, 0, QTableWidgetItem("Low"))
        table.setItem(7, 0, QTableWidgetItem("High"))
        table.setItem(8, 0, QTableWidgetItem("Open"))

        headers = table.horizontalHeader()
        headers.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)

        values = asset.getInfoValues()

        index = 0
        for key in values.keys():
            table.setItem(index, 1, QTableWidgetItem(values[key]))
            index += 1

        self.text_label = QLabel()
        # self.text_label.setText(values.keys()[0])
        self.layout.addWidget(self.text_label, 1, 0, 1, 2)

        self.setLayout(self.layout)


class AnalysisWindow(QWidget):
    def __init__(self,  anal_data, parent=None):
        super().__init__(parent)
        layout = QGridLayout(self)
        x = anal_data[6][0, :].tolist()
        y = anal_data[6][1, :].tolist()
        z = [p['fun'] for p in anal_data[7]]
        v = anal_data[8].tolist()
        ind = anal_data[9].tolist()
        width = anal_data[10]
        ind2 = (anal_data[9] + width)
        max_sharpe = anal_data[11]['x'].tolist()
        min_vol = anal_data[12]['x'].tolist()

        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setLabel('bottom', 'X')
        self.plot_widget.setLabel('left', 'Y')
        layout.addWidget(self.plot_widget, 0, 0, 1, 1)

        self.scatter_plot = pg.ScatterPlotItem()
        self.scatter_plot.setData(x, y,
                                  pen=None, symbol='o', symbolSize=5, symbolBrush=(255, 0, 0))
        self.plot_widget.addItem(self.scatter_plot)

        self.line_plot = pg.PlotDataItem()
        self.line_plot.setData(z, v, pen=(0, 255, 0))
        self.plot_widget.addItem(self.line_plot)

        self.bar_view = pg.PlotWidget()
        self.bar_graph = pg.BarGraphItem(x=ind, height=max_sharpe, width=width, brush=(255, 0, 0))
        self.bar_graph2 = pg.BarGraphItem(x=ind2, height=min_vol, width=width, brush=(0, 255, 0))
        self.bar_view.addItem(self.bar_graph)
        self.bar_view.addItem(self.bar_graph2)
        layout.addWidget(self.bar_view, 0, 1, 1, 1)

        table = QTableWidget(6, 2)
        table.setHorizontalHeaderLabels(["Параметр", "Значение"])
        layout.addWidget(table, 1, 0, 1, 2)
        table.setItem(0, 0, QTableWidgetItem("Годовая доходность(макс. Шарп)"))
        table.setItem(1, 0, QTableWidgetItem("Годовой риск(макс Шарп)"))
        table.setItem(2, 0, QTableWidgetItem("Коэффициент Шарпа"))
        table.setItem(3, 0, QTableWidgetItem("Годовая доходность(мин. риск)"))
        table.setItem(4, 0, QTableWidgetItem("Годовой риск(мин. риск)"))
        table.setItem(5, 0, QTableWidgetItem("Коэффициент Шарпа(мин. риск)"))

        for i in range(0, 6):
            table.setItem(i, 1, QTableWidgetItem(str(anal_data[i])))


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent=parent)
        self.setupUi(self)
        self.btnMarket.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_1))
        self.btnPortfolio.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_2))
        self.rmvBtnMarket.clicked.connect

        header = self.tableMarket.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.tableMarket.setColumnWidth(1, 315)
        self.tableMarket.setColumnWidth(2, 250)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        self.tableMarket.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.addBtnMarket.setEnabled(False)
        self.rmvBtnMarket.setEnabled(False)
        self.description_window = QWidget()
        self.markovitz_window = QWidget()
        self.information_window = QWidget()

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

        self.tableMarket.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableMarket.setSelectionMode(QAbstractItemView.SingleSelection)

        self.tableAnalMarket.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableAnalMarket.setSelectionMode(QAbstractItemView.SingleSelection)

        def cell_double_clicked(item):
            security = mrkt.getAsset(self.tableMarket.item(item.row(), 0).text())
            info_window(security)
            #row_data = [self.tableWidget.item(item.row(), col).text() for col in range(self.tableWidget.columnCount())]
            #new_window(row_data)

        def cell_clicked(item):
            ticket = str(self.tableMarket.item(item.row(), 0).text())
            if mrkvz.checkTicket(ticket):
                self.addBtnMarket.setEnabled(False)
            else:
                self.addBtnMarket.setEnabled(True)
            self.coords = item.row()
            self.rmvBtnMarket.setEnabled(False)

        def anal_cell_clicked(item):
            self.addBtnMarket.setEnabled(False)
            self.rmvBtnMarket.setEnabled(True)
            currentRow = self.tableAnalMarket.currentRow()
            ticket = str(self.tableAnalMarket.item(currentRow, 0).text())
            print(currentRow, ticket)

        def market_rmv_button_clicked():
            currentRow = self.tableAnalMarket.currentRow()
            ticket = str(self.tableAnalMarket.item(currentRow, 0).text())
            print(currentRow, ticket)
            self.tableAnalMarket.removeRow(currentRow)
            mrkvz.removeAsset(ticket)
            self.rmvBtnMarket.setEnabled(False)

        def market_add_button_clicked():
            st = str(self.tableMarket.item(self.coords, 0).text())
            if mrkvz.check(st):
                print("IN!!!")
                return
            else:
                mrkvz.addAsset(mrkt.getAsset(st))
                row_position = self.tableAnalMarket.rowCount()
                self.tableAnalMarket.insertRow(row_position)
                self.tableAnalMarket.setItem(row_position, 0, QTableWidgetItem(st))
                self.addBtnMarket.setEnabled(False)
                print(type(mrkt.getAsset(self.tableMarket.item(self.coords, 0).text())))
                print("ASSETS: ", mrkvz.getAssetsCount())

        def analysis_button_clicked():
            analysis_data = mrkvz.perform_analysis()
            new_analysis_window(analysis_data)

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
            # print(ticket)
            # print(mrkt.getAsset(ticket))
            # print(asset.getTicket())
            portf.addSecurity(asset)
            portf.printSecurities()


        self.tableMarket.itemClicked.connect(cell_clicked)
        self.tableMarket.itemDoubleClicked.connect(cell_double_clicked)
        self.tableAnalMarket.itemClicked.connect(anal_cell_clicked)
        self.addBtnMarket.clicked.connect(market_add_button_clicked)
        self.analBtnMarket.clicked.connect(analysis_button_clicked)
        self.rmvBtnMarket.clicked.connect(market_rmv_button_clicked)
        self.btnBuy.clicked.connect(buy_button_clicked)

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
