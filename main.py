from PortfolioImpl import *
import pandas as pd
from markovitz import *
from yahoostock import *
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
from PortfolioGUI import SellWindow, PortfolioInfoWindow

pg.setConfigOption("background", "w")
pg.setConfigOption("foreground", "k")

mrkt = Market()
mrkvz = MarkowitzAnalyzer()
portf = PortfolioImpl()

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent=parent)
        self.setupUi(self)
        with open('SpyBot.qss', 'r') as f:
            theme = f.read()

        # Apply the theme to the entire application
        self.setStyleSheet(theme)
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
        self.sell_window = QWidget()
        self.portfolio_info_window = QWidget()

        # ЗАПОЛНЕНИЕ ТАБЛИЦЫ РЫНКА
        count = 0
        for asset in mrkt.allAssets():
            row_pos = self.tableMarket.rowCount()
            asset_info = asset.getInfoValues()
            self.tableMarket.insertRow(row_pos)
            self.tableMarket.setItem(count, 0, QTableWidgetItem(asset_info['ticket']))
            self.tableMarket.setItem(count, 1, QTableWidgetItem(asset_info['name']))
            self.tableMarket.setItem(count, 2, QTableWidgetItem(asset_info['industry']))
            self.tableMarket.setItem(count, 3, QTableWidgetItem(asset_info['price']))
            count += 1

        # КЛИКИ НА ТАБЛИЦЫ
        self.tableMarket.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableMarket.setSelectionMode(QAbstractItemView.SingleSelection)

        self.tablePortfolio.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tablePortfolio.setSelectionMode(QAbstractItemView.SingleSelection)

        self.tableAnalysis.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableAnalysis.setSelectionMode(QAbstractItemView.SingleSelection)

        self.tableAnalysis.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents)

        self.tableAnalysis.resizeColumnsToContents()

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

        # УДАЛИТЬ ИЗ ТАБЛИЦЫ МАРКОВИЦА
        def remove_button_clicked():
            currentRow = self.tableAnalysis.currentRow()
            ticket = str(self.tableAnalysis.item(currentRow, 0).text())
            self.tableAnalysis.removeRow(currentRow)
            mrkvz.removeAsset(ticket)
            self.removeButton.setEnabled(False)

            if mrkvz.getAssetsCount() == 0:
                self.analBtnMarket.setEnabled(False)
                self.analBtnPortf.setEnabled(False)

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

                if mrkvz.getAssetsCount() >= 2:
                    self.analBtnMarket.setEnabled(True)
                    self.analBtnPortf.setEnabled(True)

        def analysis_button_clicked():
            analysis_data = mrkvz.perform_analysis()
            new_analysis_window(analysis_data)

        # ОТКРЫТИЕ ОКНА АНАЛИЗА
        def new_analysis_window(analysis_data):
            self.markovitz_window = AnalysisWindow(analysis_data)
            # Load the theme from the file
            with open('SpyBot.qss', 'r') as f:
                theme = f.read()
            
            # Apply the theme to the new analysis window
            self.markovitz_window.setStyleSheet(theme)
            
            # Show the new analysis window
            self.markovitz_window.show()


        def info_window(security):
            self.information_window = InfoWindow(security)
            self.information_window.show()
        # ПОВЕДЕНИЕ ПОКУПКИ АКЦИИ
        def buy_button_clicked():
            currentRow = self.tableMarket.currentRow()
            ticket = str(self.tableMarket.item(currentRow, 0).text())
            asset = mrkt.getAsset(ticket)

            self.buy_window = BuyWindow()
            self.buy_window.show()

            if self.buy_window.exec_() == QDialog.Accepted:
                input_value = self.buy_window.get_input_value()
                if input_value is not None:
                    if portf.checkTicket(ticket):
                        portf.buySecurity(asset, input_value)
                        for i in range(0, self.tablePortfolio.rowCount()):
                            if ticket == str(self.tablePortfolio.item(i, 0).text()):
                                self.tablePortfolio.setItem(i, 4, QTableWidgetItem(str(asset.getQuantity())))
                    else:
                        portf.buySecurity(asset, input_value)
                        a_info = asset.getInfoValues()
                        portfolio_row = self.tablePortfolio.rowCount()
                        self.tablePortfolio.insertRow(portfolio_row)
                        self.tablePortfolio.setItem(portfolio_row, 0, QTableWidgetItem(a_info['ticket']))
                        self.tablePortfolio.setItem(portfolio_row, 1, QTableWidgetItem(a_info['name']))
                        self.tablePortfolio.setItem(portfolio_row, 2, QTableWidgetItem(a_info['industry']))
                        self.tablePortfolio.setItem(portfolio_row, 3, QTableWidgetItem(a_info['price']))
                        self.tablePortfolio.setItem(portfolio_row, 4, QTableWidgetItem(str(asset.getQuantity())))
        # ДВОЙНОЕ НАЖАТИЕ НА АКЦИЮ В ПОРТФЕЛЕ
        def portfolio_cell_double_clicked(item):
            security = portf.getStock(self.tablePortfolio.item(item.row(), 0).text())
            info_window(security)
        # ДОБАВЛЕНИЕ В АНАЛИЗАТОР МАРКОВИЦА ИЗ ПОРТФЕЛЯ
        def add_button_clicked_portfolio():
            st = str(self.tablePortfolio.item(self.tablePortfolio.currentRow(), 0).text())
            if mrkvz.check(st):
                print("IN!!!")
                return
            else:
                mrkvz.addAsset(portf.getStock(st))
                row_position = self.tableAnalysis.rowCount()
                self.tableAnalysis.insertRow(row_position)
                self.tableAnalysis.setItem(row_position, 0, QTableWidgetItem(st))
                self.addBtnMarket.setEnabled(False)
                print(type(mrkt.getAsset(self.tablePortfolio.item(self.tablePortfolio.currentRow(), 0).text())))
                print("ASSETS: ", mrkvz.getAssetsCount())

                if mrkvz.getAssetsCount() >= 2:
                    self.analBtnMarket.setEnabled(True)
                    self.analBtnPortf.setEnabled(True)
        # КНОПКА ПРОДАЖИ
        def sell_button_clicked():
            currentRow = self.tablePortfolio.currentRow()
            ticket = str(self.tablePortfolio.item(currentRow, 0).text())
            asset = portf.getStock(ticket)

            self.sell_window = SellWindow()
            self.sell_window.show()

            if self.sell_window.exec_() == QDialog.Accepted:
                change = self.sell_window.get_input_value()
                if change is not None:
                    portf.sellSecurity(ticket, change)
                    portfolio_row = self.tablePortfolio.currentRow()
                    if portf.checkTicket(ticket):
                        self.tablePortfolio.setItem(portfolio_row, 4, QTableWidgetItem(str(asset.getQuantity())))
                    else:
                        self.tablePortfolio.removeRow(portfolio_row)

        def portfolio_info_clicked():
            self.portfolio_info_window = PortfolioInfoWindow(portf)
            self.portfolio_info_window.show()

        # ПОВЕДЕНИЕ ОБЩИХ ЭЛЕМЕНТОВ
        self.tableAnalysis.itemClicked.connect(analysis_cell_clicked)
        self.removeButton.clicked.connect(remove_button_clicked)

        # ПОВЕДЕНИЕ ТАБЛИЦЫ РЫНКА
        self.tableMarket.itemClicked.connect(cell_clicked)
        self.tableMarket.itemDoubleClicked.connect(cell_double_clicked)
        self.addBtnMarket.clicked.connect(market_add_button_clicked)
        self.analBtnMarket.clicked.connect(analysis_button_clicked)
        self.btnBuy.clicked.connect(buy_button_clicked)
        self.analBtnMarket.setEnabled(False)

        # ПОВЕДЕНИЕ ТАБЛИЦЫ ПОРТФЕЛЯ
        self.tablePortfolio.itemClicked.connect(cell_clicked)
        self.tablePortfolio.itemDoubleClicked.connect(portfolio_cell_double_clicked)
        self.analBtnPortf.clicked.connect(analysis_button_clicked)
        self.addBtnPortf.clicked.connect(add_button_clicked_portfolio)
        self.sellBtnPortf.clicked.connect(sell_button_clicked)
        self.analBtnPortf.setEnabled(False)
        self.portfolioInfoButton.clicked.connect(portfolio_info_clicked)

if __name__ == "__main__":
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
