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
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QIntValidator
from PyQt5 import uic
from pyqtgraph import PlotWidget, plot, Qt
import pyqtgraph as pg
from pyqtgraph import DateAxisItem
import sys


class InfoPortfolioWindow(QWidget):
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
        self.layout.addWidget(self.text_label, 1, 0, 1, 2)

        self.setLayout(self.layout)


class AnalysisPortfolioWindow(QWidget):
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

        headers = table.horizontalHeader()
        headers.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)

        for i in range(0, 6):
            table.setItem(i, 1, QTableWidgetItem(str(anal_data[i])))


class SellWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Новое окно")
        self.setGeometry(300, 300, 300, 200)

        self.input_label = QLabel("Введите количество (0-10000):", self)
        self.input_label.move(50, 50)

        self.input_textbox = QLineEdit(self)
        self.input_textbox.setValidator(QIntValidator(0, 10000))  # Исправленная строка
        self.input_textbox.move(50, 80)

        self.ok_button = QPushButton("ОК", self)
        self.ok_button.move(50, 120)
        self.ok_button.clicked.connect(self.accept)

    def get_input_value(self):
        input_value = self.input_textbox.text()
        if input_value.isnumeric():
            return int(input_value)
        else:
            QMessageBox.warning(self, "Ошибка", "Неправильный ввод. Введите число заново.")
            return None