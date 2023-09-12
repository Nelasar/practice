from PortfolioImpl import *
from markovitz import *
from market import *
from u import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QWidget, QAbstractItemView
from PyQt5.QtWidgets import QDialog
import pyqtgraph as pg
import sys
from MarketGUI import BuyWindow, InfoWindow, AnalysisWindow, SetupAnalyzerWindow
from PortfolioGUI import SellWindow, PortfolioInfoWindow
import yfinance as yf


pg.setConfigOption("background", "w")
pg.setConfigOption("foreground", "k")

mrkt = Market()
mrkvz = MarkowitzAnalyzer(5000, 10.0)
portf = PortfolioImpl()

mrkt.addAsset(bond1)
mrkt.addAsset(bond2)
mrkt.addAsset(bond3)
mrkt.addAsset(bond4)
mrkt.addAsset(bond5)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent=parent)
        self.setupUi(self)
        self.setWindowTitle('BAUMANInvestPro')
        self.resize(1200, 750)
        with open('SpyBot.qss', 'r') as f:
            theme = f.read()

        self.setStyleSheet(theme)
        self.btnMarket.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_1))
        self.btnPortfolio.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_2))

        # ТАБЛИЦА РЫНКА
        header = self.tableMarket.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.tableMarket.setColumnWidth(1, 315)
        self.tableMarket.setColumnWidth(2, 250)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        self.tableMarket.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        # ТАБЛИЦА ПОРТФЕЛЯ
        header = self.tablePortfolio.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.tablePortfolio.setColumnWidth(1, 315)
        self.tablePortfolio.setColumnWidth(2, 250)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
        self.tablePortfolio.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.addBtnMarket.setEnabled(False)
        self.removeButton.setEnabled(False)
        self.addBtnPortf.setEnabled(False)
        self.clearButton.setEnabled(False)

        self.description_window = QWidget()
        self.markovitz_window = QWidget()
        self.information_window = QWidget()
        self.buy_window = QWidget()
        self.sell_window = QWidget()
        self.portfolio_info_window = QWidget()
        self.setup_analyzer_window = QWidget()

        # ЗАПОЛНЕНИЕ ТАБЛИЦЫ РЫНКА
        count = 0
        for asset in mrkt.allAssets():
            row_pos = self.tableMarket.rowCount()
            asset_info = asset.getInfoValues()
            asset_type = asset.getType()
            self.tableMarket.insertRow(row_pos)
            self.tableMarket.setItem(count, 0, QTableWidgetItem(asset_info['Ticket']))
            self.tableMarket.setItem(count, 1, QTableWidgetItem(asset_info['Name']))
            self.tableMarket.setItem(count, 2, QTableWidgetItem(asset_info['Industry']))
            self.tableMarket.setItem(count, 3, QTableWidgetItem(asset_info['Price']))
            self.tableMarket.setItem(count, 4, QTableWidgetItem(asset_type))
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
                self.clearButton.setEnabled(False)

        def clear_button_clicked():
            while(self.tableAnalysis.rowCount() > 0):
                self.tableAnalysis.removeRow(0)
            mrkvz.clearAnalyzer()
            self.clearButton.setEnabled(False)
            self.analBtnPortf.setEnabled(False)
            self.analBtnMarket.setEnabled(False)

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
                if mrkvz.getAssetsCount() >= 1:
                    self.clearButton.setEnabled(True)

        def analysis_button_clicked():
            analysis_data = mrkvz.perform_analysis()
            new_analysis_window(analysis_data)

        # ОТКРЫТИЕ ОКНА АНАЛИЗА
        def new_analysis_window(analysis_data):
            self.markovitz_window = AnalysisWindow(analysis_data)
            # Load the theme from the file
            with open('SpyBot.qss', 'r') as f:
                theme = f.read()

            self.markovitz_window.setStyleSheet(theme)
            self.markovitz_window.show()

        def setup_button_clicked():
            self.setup_analyzer_window = SetupAnalyzerWindow()
            self.setup_analyzer_window.show()

            if self.setup_analyzer_window.exec_() == QDialog.Accepted:
                input_values = self.setup_analyzer_window.get_input_values()
                mrkvz.set_options(input_values[0], input_values[1])

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
                        self.tablePortfolio.setItem(portfolio_row, 0, QTableWidgetItem(a_info['Ticket']))
                        self.tablePortfolio.setItem(portfolio_row, 1, QTableWidgetItem(a_info['Name']))
                        self.tablePortfolio.setItem(portfolio_row, 2, QTableWidgetItem(a_info['Industry']))
                        self.tablePortfolio.setItem(portfolio_row, 3, QTableWidgetItem(a_info['Price']))
                        self.tablePortfolio.setItem(portfolio_row, 4, QTableWidgetItem(str(asset.getQuantity())))
                        self.tablePortfolio.setItem(portfolio_row, 5, QTableWidgetItem(str(asset.getType())))
        # ДВОЙНОЕ НАЖАТИЕ НА АКЦИЮ В ПОРТФЕЛЕ
        def portfolio_cell_double_clicked(item):
            security = portf.getStock(self.tablePortfolio.item(item.row(), 0).text(),
                                      self.tablePortfolio.item(item.row(), 5).text())
            info_window(security)
        # ДОБАВЛЕНИЕ В АНАЛИЗАТОР МАРКОВИЦА ИЗ ПОРТФЕЛЯ
        def add_button_clicked_portfolio():
            st = str(self.tablePortfolio.item(self.tablePortfolio.currentRow(), 0).text())
            type = str(self.tablePortfolio.item(self.tablePortfolio.currentRow(), 5). text())
            if mrkvz.check(st):
                print("IN!!!")
                return
            else:
                mrkvz.addAsset(portf.getStock(st, type))
                row_position = self.tableAnalysis.rowCount()
                self.tableAnalysis.insertRow(row_position)
                self.tableAnalysis.setItem(row_position, 0, QTableWidgetItem(st))
                self.addBtnMarket.setEnabled(False)
                print("ASSETS: ", mrkvz.getAssetsCount())

                if mrkvz.getAssetsCount() >= 2:
                    self.analBtnMarket.setEnabled(True)
                    self.analBtnPortf.setEnabled(True)
                    self.clearButton.setEnabled(True)
        # КНОПКА ПРОДАЖИ
        def sell_button_clicked():
            currentRow = self.tablePortfolio.currentRow()
            ticket = str(self.tablePortfolio.item(currentRow, 0).text())
            type = str(self.tablePortfolio.item(currentRow, 5).text())
            asset = portf.getStock(ticket, type)

            self.sell_window = SellWindow()
            self.sell_window.show()

            if self.sell_window.exec_() == QDialog.Accepted:
                change = self.sell_window.get_input_value()
                if change is not None:
                    portf.sellSecurity(ticket, type, change)
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
        self.clearButton.clicked.connect(clear_button_clicked)
        self.setupAnalyzerBtn.clicked.connect(setup_button_clicked)

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
    app = QtWidgets.QApplication(sys.argv)
    window = Ui_MainWindow()  # uic.loadUi('u.ui')
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())



#
#
# BONDS/STOCKS TABLES
#
#

"""
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QVBoxLayout
from functools import partial

def create_menu(menu, tables):
    securities = ['Stocks', 'Bonds', 'Metals']
    for i, security in enumerate(securities):
        show_table_func = partial(show_table, i, tables)
        action = menu.addAction(security)
        action.setIconVisibleInMenu(False)
        action.triggered.connect(show_table_func)

def show_table(security_index, tables):
    for i, table in enumerate(tables):
        table.setVisible(i == security_index)

class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.tables = []
        menu = QtWidgets.QMenu(self)
        create_menu(menu, self.tables)

        button = QtWidgets.QPushButton()
        button.setMenu(menu)

        self.layout = QVBoxLayout()
        self.layout.addWidget(button)

        self.create_table("Stocks")
        self.create_table("Bonds")
        self.create_table("Metals")

        self.setLayout(self.layout)
        self.resize(640, 480)

    def create_table(self, security):
        table = QTableWidget()
        table.setColumnCount(1)
        table.setHorizontalHeaderLabels([security])
        for i in range(5):
            item = QTableWidgetItem(f"{security} Item {i + 1}")
            table.setItem(i, 0, item)
        table.setVisible(security == "Stocks")
        self.tables.append(table)
        self.layout.addWidget(table)

if __name__ == "__main__":
    # app = QtWidgets.QApplication(sys.argv)
    # w = Widget()
    # w.show()
    # sys.exit(app.exec_())
    pass

    # ticket = yf.Ticker('^TNX')

"""
