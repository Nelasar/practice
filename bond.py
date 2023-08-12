import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, \
    QGridLayout, QTableWidget, QTableWidgetItem, QPushButton
import pyqtgraph as pg
from PyQt5 import QtWidgets


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 700, 500)
        layout = QVBoxLayout()
        button = QPushButton("Open New Window")
        button.clicked.connect(self.open_new_window)
        layout.addWidget(button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.new_window = None

    def open_new_window(self):
        self.new_window = NewWindow()
        self.new_window.show()


class NewWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QGridLayout(self)
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setLabel('bottom', 'X')
        self.plot_widget.setLabel('left', 'Y')
        layout.addWidget(self.plot_widget, 0, 0, 1, 1)

        self.scatter_plot = pg.ScatterPlotItem()
        self.scatter_plot.setData([1, 3, 2, 4, 6, 8], [3, 6, 2, 8, 4, 7],
                                  pen=None, symbol='o', symbolSize=5, symbolBrush=(255, 0, 0))
        self.plot_widget.addItem(self.scatter_plot)

        self.line_plot = pg.PlotDataItem()
        self.line_plot.setData([1, 2, 3, 4, 5, 6], [2, 4, 6, 8, 10, 12], pen=(0, 255, 0))
        self.plot_widget.addItem(self.line_plot)

        self.bar_view = pg.PlotWidget()
        self.bar_graph = pg.BarGraphItem(x=[1, 3, 2, 4, 6, 8], height=[3, 6, 2, 8, 4, 7], width=0.6, brush=(255, 0, 0))
        self.bar_view.addItem(self.bar_graph)
        layout.addWidget(self.bar_view, 0, 1, 1, 1)

        table = QTableWidget(6, 2)
        table.setHorizontalHeaderLabels(["Column 1", "Column 2"])
        layout.addWidget(table, 1, 0, 1, 2)

        for row in range(6):
            for col in range(2):
                item = QTableWidgetItem(f"({row}, {col})")
                table.setItem(row, col, item)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())