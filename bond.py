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
# from linearregression import StockAnalysis


class InfoWindow(QWidget):
    def __init__(self, asset):
        super().__init__()
        self.layout = QGridLayout(self)
        self.resize(800, 500)
        self.history = asset.getPriceHistory()

        x = self.history.index
        x = x.to_pydatetime().tolist()
        self.y = self.history.values.flatten()
        self.x_float = [date.timestamp() for date in x]

        self.plot_widget = pg.PlotWidget(axisItems={'bottom': DateAxisItem()})
        self.plot_widget.setLabel('bottom', 'X')
        self.plot_widget.setLabel('left', 'Y')
        self.layout.addWidget(self.plot_widget, 0, 0, 1, 1)

        self.line_plot = pg.PlotCurveItem()
        self.line_plot.setData(x=self.x_float, y=self.y, pen=(0, 255, 0))
        self.plot_widget.addItem(self.line_plot)

        self.table = QTableWidget(9, 2)
        self.table.setHorizontalHeaderLabels(["Параметр", "Значение"])
        self.layout.addWidget(self.table, 0, 1, 1, 1)

        self.table.setItem(0, 0, QTableWidgetItem("Ticket"))
        self.table.setItem(1, 0, QTableWidgetItem("Name"))
        self.table.setItem(2, 0, QTableWidgetItem("Country"))
        self.table.setItem(3, 0, QTableWidgetItem("Industry"))
        self.table.setItem(4, 0, QTableWidgetItem("Price"))
        self.table.setItem(5, 0, QTableWidgetItem("Beta"))
        self.table.setItem(6, 0, QTableWidgetItem("Low"))
        self.table.setItem(7, 0, QTableWidgetItem("High"))
        self.table.setItem(8, 0, QTableWidgetItem("Open"))

        headers = self.table.horizontalHeader()
        headers.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)

        values = asset.getInfoValues()

        index = 0
        for key in values.keys():
            self.table.setItem(index, 1, QTableWidgetItem(values[key]))
            index += 1

        self.text_label = QLabel()
        self.layout.addWidget(self.text_label, 1, 0, 1, 2)

        self.button_layout = QGridLayout()
        self.button_layout.setSpacing(10)

        self.button1 = QPushButton("Button 1")
        self.button2 = QPushButton("Button 2")
        self.button3 = QPushButton("Button 3")
        self.button4 = QPushButton("Button 4")

        self.button1.clicked.connect(self.showGraph1)
        self.button2.clicked.connect(self.showGraph2)
        self.button3.clicked.connect(self.showGraph3)
        self.button4.clicked.connect(self.showGraph4)

        self.button_layout.addWidget(self.button1, 0, 0)
        self.button_layout.addWidget(self.button2, 0, 1)
        self.button_layout.addWidget(self.button3, 1, 0)
        self.button_layout.addWidget(self.button4, 1, 1)
        self.layout.addLayout(self.button_layout, 2, 0, 1, 2)

        self.graph_window = pg.GraphicsLayoutWidget()
        self.layout.addWidget(self.graph_window, 0, 2, 2, 1)

        self.setLayout(self.layout)

    def showGraph1(self):
        self.graph_window.clear()
        plot = self.graph_window.addPlot()
        plot.plot(x=self.x_float, y=self.y, pen=(255, 0, 0))

    def showGraph2(self):
        self.graph_window.clear()
        plot = self.graph_window.addPlot()
        plot.setLabel('bottom', 'X')
        plot.setLabel('left', 'Y')
        plot.plot(x=self.x_float, y=self.y ** 2, pen=(0, 0, 255))

    def showGraph3(self):
        self.graph_window.clear()
        plot = self.graph_window.addPlot()
        plot.setLabel('bottom', 'X')
        plot.setLabel('left', 'Y')
        plot.plot(x=self.x_float, y=self.y ** 3, pen=(0, 255, 0))

    def showGraph4(self):
        self.graph_window.clear()
        plot = self.graph_window.addPlot()
        plot.setLabel('bottom', 'X')
        plot.setLabel('left', 'Y')
        plot.plot(x=self.x_float, y=-self.y, pen=(255, 0, 255))


if __name__ == '__main__':
    asset = yfStock('GOOG')
    app = QApplication([])
    info_window = InfoWindow(asset)
    info_window.show()
    sys.exit(app.exec_())