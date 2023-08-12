from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout, QWidget
from PyQt5.QtCore import Qt
import pyqtgraph as pg
from datetime import datetime
import pandas as pd

class DateAxisItem(pg.AxisItem):
    def tickStrings(self, values, scale, spacing):
        return [datetime.fromtimestamp(value).strftime('%Y-%m-%d') for value in values]

class infoWindow(QWidget):
    def __init__(self, asset, parent=None):
        super().init(parent)
        layout = QGridLayout(self)
        self.history = asset.getPriceHistory()
        self.plot_widget = pg.PlotWidget(axisItems={'bottom': DateAxisItem()})
        self.plot_widget.showGrid(x=True, y=True)
        self.plot_widget.setLabel('bottom', 'X')
        self.plot_widget.setLabel('left', 'Y')

        self.plot_widget.plot(x=self.history.index, y=self.history.values.flatten())

        layout.addWidget(self.plot_widget, 0, 0, 1, 1)
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")

        button = QPushButton("Open infoWindow", self)
        button.setGeometry(100, 100, 150, 50)
        button.clicked.connect(self.open_info_window)

    def open_info_window(self):
        asset = pd.DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9]], columns=['A', 'B', 'C'],
                             index=pd.date_range(start='20220101', periods=3))
        self.info_window = infoWindow(asset)
        self.info_window.show()

if __name__ == '__main__':
    app = QApplication([])
    mainWin = MainWindow()
    mainWin.show()
    app.exec_()
