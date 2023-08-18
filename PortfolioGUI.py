from PyQt5.QtWidgets import QTableWidgetItem, QTableWidget, QWidget, QGridLayout
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import  QFont
from PyQt5.QtGui import QIntValidator
from PyQt5 import uic
from pyqtgraph import PlotWidget, plot, Qt
import pyqtgraph as pg
from pyqtgraph import DateAxisItem
import sys


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


class PortfolioInfoWindow(QWidget):
    def __init__(self, portfolio):
        super().__init__()
        self.layout = QGridLayout(self)
        self.resize(800, 700)

        self.weightings = portfolio.weighting()
        print(self.weightings)

        x = list(self.weightings.keys())
        y = list(self.weightings.values())

        xval = list(range(1, len(x) + 1))
        print(xval)

        ticks = []
        for i, item in enumerate(x):
            ticks.append((xval[i], item))
        ticks = [ticks]

        self.bar_view = pg.PlotWidget()
        self.bar_graph = pg.BarGraphItem(x=xval, height=y, width=0.35, brush=(255, 0, 0))
        self.bar_view.addItem(self.bar_graph)
        self.layout.addWidget(self.bar_view, 0, 1, 1, 1)
        ax = self.bar_view.getAxis('bottom')
        ax.setTicks(ticks)

        index_count = len(x)

        self.table_widget = QTableWidget()
        self.table_widget.setRowCount(1)
        self.table_widget.setColumnCount(index_count)
        self.layout.addWidget(self.table_widget, 1, 0, 1, 2)

        self.labels = x
        self.table_widget.setHorizontalHeaderLabels(self.labels)

        for i in range(len(y)):
            item = QTableWidgetItem(str(y[i]))
            self.table_widget.setItem(0, i, item)

        self.label_total = QLabel("ОБЩАЯ ЦЕННОСТЬ РАВНА")
        self.label_total.setFont(QFont('Arial', 32))
        self.layout.addWidget(self.label_total, 2, 0, 1, 2)

        total_value = str(portfolio.price())
        self.label_total_value = QLabel(total_value)
        self.label_total_value.setFont(QFont('Arial', 32))
        self.layout.addWidget(self.label_total_value, 3, 0, 1, 2)

        self.setLayout(self.layout)
