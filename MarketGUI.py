from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QTableWidgetItem, QTableWidget, QWidget, QGridLayout
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox
from PyQt5.QtGui import QIntValidator
from PyQt5 import uic
from pyqtgraph import PlotWidget, plot, Qt
import pyqtgraph as pg
from pyqtgraph import DateAxisItem
import sys
from linearregression import StockAnalysis


class LinearInputWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Анализ акции")
        self.setGeometry(300, 300, 300, 325)
        self.setFixedSize(300, 325)

        self.input_label_first = QLabel("Введите дни (10-365):", self)
        self.input_label_first.move(50, 50)

        self.input_textbox = QLineEdit(self)
        self.input_textbox.setValidator(QIntValidator(10, 365))
        self.input_textbox.move(50, 80)

        self.input_label_second = QLabel("Введите дни (10-365):", self)
        self.input_label_second.move(50, 110)

        self.input_textbox_2 = QLineEdit(self)
        self.input_textbox_2.setValidator(QIntValidator(10, 365))
        self.input_textbox_2.move(50, 150)

        self.ok_button = QPushButton("ОК", self)
        self.ok_button.move(50, 200)
        self.ok_button.clicked.connect(self.accept)


    def get_input_values(self):
        first_days = self.input_textbox.text()
        second_days = self.input_textbox_2.text()

        if int(first_days) == int(second_days):
            QMessageBox.message(self, "Ошибка!", "Числа не должны быть равны.")
            return None
        elif first_days.isnumeric() and second_days.isnumeric():
            return [int(first_days), int(second_days)]
        else:
            QMessageBox.warning(self, "Ошибка!", "Неправильный ввод. Введите число заново.")
            return None

class LinearInputWindowExtended(LinearInputWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Анализ акции")
        self.setGeometry(300, 300, 500, 200)
        self.setFixedSize(500, 250)

        self.input_label_third = QLabel("Введите дни MSD (10-365):", self)
        self.input_label_third.move(300, 50)

        self.input_textbox_3 = QLineEdit(self)
        self.input_textbox_3.setValidator(QIntValidator(10, 365))
        self.input_textbox_3.move(300, 80)

        self.input_label_fourth = QLabel("Введите дни MSD (10-365):", self)
        self.input_label_fourth.move(300, 110)

        self.input_textbox_4 = QLineEdit(self)
        self.input_textbox_4.setValidator(QIntValidator(10, 365))
        self.input_textbox_4.move(300, 150)

        self.ok_button.move(300, 200)

    def get_input_values(self):
        first_days = self.input_textbox.text()
        second_days = self.input_textbox_2.text()
        third_days = self.input_textbox_3.text()
        fourth_days = self.input_textbox_4.text()

        if int(first_days) == int(second_days):
            QMessageBox.message(self, "Ошибка!", "Числа не должны быть равны.")
            return None
        elif int(third_days) == fourth_days(int):
            QMessageBox.message(self, "Ошибка!", "Числа не должны быть равны.")
            return None
        elif int(first_days) == int(fourth_days):
            QMessageBox.message(self, "Ошибка!", "Числа не должны быть равны.")
            return None
        elif first_days.isnumeric() and second_days.isnumeric() and third_days.isnumeric() and fourth_days.isnumeric():
            return [int(first_days), int(second_days), int(third_days), int(fourth_days)]
        else:
            QMessageBox.warning(self, "Ошибка", "Неправильный ввод. Введите число заново.")
            return None


class InfoWindow(QWidget):
    def __init__(self, asset):
        super().__init__()
        self.setWindowTitle("Информация об акции")
        self.layout = QGridLayout(self)
        self.history = asset.getPriceHistory()

        self.resize(1600, 750)
        self.setFixedSize(1600, 750)

        self.analyzer = StockAnalysis(asset)

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

        self.text_label = QLabel()
        self.text_label.setText('ИСТОРИЯ ЦЕН')
        self.layout.addWidget(self.text_label, 1, 0, 1, 2)

        self.table = QTableWidget(9, 2)
        self.table.resize(650, 800)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setHorizontalHeaderLabels(["Параметр", "Значение"])
        self.layout.addWidget(self.table, 0, 1, 1, 1)

        self.table.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents)

        self.table.resizeColumnsToContents()

        # IF ASSET.GETTYPE == 'Stock' ELIF ASSET.GETTYPE == 'Bond'
        values = asset.getInfoValues()

        print(values)

        index = 0
        for key in values.keys():
            self.table.setItem(index, 0, QTableWidgetItem(str(key)))
            index += 1

        """
        self.table.setItem(0, 0, QTableWidgetItem("Ticket"))
        self.table.setItem(1, 0, QTableWidgetItem("Name"))
        self.table.setItem(2, 0, QTableWidgetItem("Country"))
        self.table.setItem(3, 0, QTableWidgetItem("Industry"))
        self.table.setItem(4, 0, QTableWidgetItem("Price"))
        self.table.setItem(5, 0, QTableWidgetItem("Beta"))
        self.table.setItem(6, 0, QTableWidgetItem("Low"))
        self.table.setItem(7, 0, QTableWidgetItem("High"))
        self.table.setItem(8, 0, QTableWidgetItem("Open"))
        """
        headers = self.table.horizontalHeader()
        headers.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)

        index = 0
        for key in values.keys():
            self.table.setItem(index, 1, QTableWidgetItem(str(values[key])))
            index += 1


        self.text_label = QLabel()
        self.layout.addWidget(self.text_label, 1, 0, 1, 2)

        self.button_layout = QGridLayout()
        self.button_layout.setSpacing(10)

        self.button1 = QPushButton("SMA")
        self.button2 = QPushButton("MSD")
        self.button3 = QPushButton("RSI")
        self.button4 = QPushButton("PREDICTION")

        self.button1.clicked.connect(self.showGraphSMA)
        self.button2.clicked.connect(self.showGraphMSD)
        self.button3.clicked.connect(self.showGraphRSI)
        self.button4.clicked.connect(self.showGraphPrediction)

        self.button_layout.addWidget(self.button1, 0, 0)
        self.button_layout.addWidget(self.button2, 0, 1)
        self.button_layout.addWidget(self.button3, 1, 0)
        self.button_layout.addWidget(self.button4, 1, 1)
        self.layout.addLayout(self.button_layout, 2, 2, 1, 2)

        self.input_combo = QComboBox()
        self.input_combo.addItems(["День", "Месяц", "Год"])
        self.input_combo.currentIndexChanged.connect(self.updateGraph)

        self.layout.addWidget(self.input_combo, 2, 0, 1, 1)

        self.graph_window = pg.GraphicsLayoutWidget()
        self.layout.addWidget(self.graph_window, 0, 2, 2, 1)

        self.setLayout(self.layout)

        self.input_window = QWidget()

    def updateGraph(self):
        index = self.input_combo.currentIndex()
        if index == 0:
            # Show prices by day
            x = self.history.index
            x = x.to_pydatetime().tolist()
            self.y = self.history.values.flatten()
            self.x_float = [date.timestamp() for date in x]

            self.line_plot.setData(x=self.x_float, y=self.y, pen=(0, 255, 0))
        elif index == 1:
            # Show prices by month
            x_month = self.history.resample('M').mean()
            x = x_month.index
            x = x.to_pydatetime().tolist()
            self.y = x_month.values.flatten()
            x_float = [date.timestamp() for date in x]
            self.line_plot.setData(x=x_float, y=self.y, pen=(0, 255, 0))
        elif index == 2:
            # Show prices by year
            x_year = self.history.resample('Y').mean()
            x = x_year.index
            x = x.to_pydatetime().tolist()
            self.y = x_year.values.flatten()
            x_float = [date.timestamp() for date in x]
            self.line_plot.setData(x=x_float, y=self.y, pen=(0, 255, 0))

    def showGraphSMA(self):
        self.graph_window.clear()

        self.input_window = LinearInputWindow()
        self.input_window.show()

        if self.input_window.exec_() == QDialog.Accepted:
            input_values = self.input_window.get_input_values()
            if input_values is not None:
                sma = self.analyzer.sma(input_values[0], input_values[1])
                x = sma.index
                x = x.to_pydatetime().tolist()

                indexies = sma.columns

                y = sma[indexies[1]].values.flatten()
                x_float = [date.timestamp() for date in x]

                plot = self.graph_window.addPlot(axisItems={'bottom': DateAxisItem()})
                plot.addLegend()
                plot.setLabel('bottom', 'X')
                plot.setLabel('left', 'Y')
                plot.plot(x=x_float, y=y, pen=(0, 0, 255), name=indexies[1])

                x = sma.index
                x = x.to_pydatetime().tolist()
                y = sma[indexies[2]].values.flatten()
                x_float = [date.timestamp() for date in x]
                plot.plot(x=x_float, y=y, pen=(255, 0, 0), name=indexies[2])

                plot.addLegend()

    def showGraphMSD(self):
        self.graph_window.clear()

        self.input_window = LinearInputWindow()
        self.input_window.show()

        if self.input_window.exec_() == QDialog.Accepted:
            input_values = self.input_window.get_input_values()
            if input_values is not None:
                msd = self.analyzer.msd(input_values[0], input_values[1])
                print(input_values[0])
                print(input_values[1])
                x = msd.index
                x = x.to_pydatetime().tolist()

                indexies = msd.columns

                y = msd[indexies[2]].values.flatten()
                x_float = [date.timestamp() for date in x]

                plot = self.graph_window.addPlot(axisItems={'bottom': DateAxisItem()})
                plot.addLegend()
                plot.setLabel('bottom', 'X')
                plot.setLabel('left', 'Y')
                plot.plot(x=x_float, y=y, pen=(0, 0, 255), name=indexies[2])

                x = msd.index
                x = x.to_pydatetime().tolist()
                y = msd[indexies[3]].values.flatten()
                x_float = [date.timestamp() for date in x]
                plot.plot(x=x_float, y=y, pen=(255, 0, 0), name=indexies[3])

                plot.addLegend()

    def showGraphRSI(self):
        self.graph_window.clear()

        rsi = self.analyzer.RSI()
        x = rsi.index
        x = x.to_pydatetime().tolist()

        indexies = rsi.columns

        y = rsi[indexies[1]].values.flatten()
        x_float = [date.timestamp() for date in x]

        plot = self.graph_window.addPlot(axisItems={'bottom': DateAxisItem()})
        plot.addLegend()
        plot.setLabel('bottom', 'X')
        plot.setLabel('left', 'Y')
        plot.plot(x=x_float, y=y, pen=(0, 0, 255), name=indexies[1])

    def showGraphPrediction(self):
        self.graph_window.clear()

        self.input_window = LinearInputWindowExtended()
        self.input_window.show()

        if self.input_window.exec_() == QDialog.Accepted:
            input_values = self.input_window.get_input_values()
            if input_values is not None:
                linear_trading = self.analyzer.lin_reg_trading(input_values[0], input_values[1],
                                                               input_values[2], input_values[3])
                plot = self.graph_window.addPlot(axisItems={'bottom': DateAxisItem()})
                plot.addLegend()
                plot.setLabel('bottom', 'X')
                plot.setLabel('left', 'Y')

                x = linear_trading.index
                x = x.to_pydatetime().tolist()

                y = linear_trading['prediction'].values.flatten()
                x_float = [date.timestamp() for date in x]

                # HERE
                plot = self.graph_window.addPlot(axisItems={'bottom': DateAxisItem()})
                plot.setLabel('bottom', 'X')
                plot.setLabel('left', 'Y')
                plot.plot(x=x_float, y=y, pen=(0, 0, 255), name='Prediction')

                plot.addLegend()

                x = linear_trading.index
                x = x.to_pydatetime().tolist()
                y = linear_trading['strategy'].cumsum() * 100
                x_float = [date.timestamp() for date in x]
                plot.plot(x=x_float, y=y, pen=(255, 0, 0), name='Strategy')


class AnalysisWindow(QWidget):
    def __init__(self,  analysis_data, parent=None):
        super().__init__(parent)
        layout = QGridLayout(self)
        self.setWindowTitle('Результаты анализа')
        self.resize(1000, 800)
        self.setFixedSize(1000, 800)

        x = analysis_data['results'][0, :].tolist()
        y = analysis_data['results'][1, :].tolist()
        z = [p['fun'] for p in analysis_data['efficient_portfolios']]
        v = analysis_data['target'].tolist()
        ind = analysis_data['index'].tolist()  # analysis_data['index']
        width = analysis_data['width']  # analysis_data['width']
        ind2 = (analysis_data['index'] + width)
        max_sharpe = analysis_data['max_sharpe']['x'].tolist()
        min_vol = analysis_data['min_vol']['x'].tolist()
        items = analysis_data['asset_count']
        print(type(items))
        tickets = analysis_data['tickets']
        allocation = analysis_data['min_vol_alloc']
        print(type(allocation))
        allocation = allocation.iloc[0]

        allocation_sharpe = analysis_data['max_sharpe_alloc']
        allocation_sharpe = allocation_sharpe.iloc[0]

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
        self.bar_view.addLegend()
        self.bar_graph = pg.BarGraphItem(x=ind, height=max_sharpe, width=width, brush=(255, 0, 0), name='Max Sharpe')
        self.bar_graph2 = pg.BarGraphItem(x=ind2, height=min_vol, width=width, brush=(0, 255, 0), name='Min Volatility')
        self.bar_view.addItem(self.bar_graph)
        self.bar_view.addItem(self.bar_graph2)
        layout.addWidget(self.bar_view, 0, 1, 1, 1)

        table = QTableWidget(6, 2)
        table.setHorizontalHeaderLabels(["Параметр", "Значение"])
        layout.addWidget(table, 1, 0, 1, 2)
        table.resize(650, 800)
        table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        table.setItem(0, 0, QTableWidgetItem("Годовая доходность(макс. Шарп)"))
        table.setItem(1, 0, QTableWidgetItem("Годовой риск(макс Шарп)"))
        table.setItem(2, 0, QTableWidgetItem("Коэффициент Шарпа"))
        table.setItem(3, 0, QTableWidgetItem("Годовая доходность(мин. риск)"))
        table.setItem(4, 0, QTableWidgetItem("Годовой риск(мин. риск)"))
        table.setItem(5, 0, QTableWidgetItem("Коэффициент Шарпа(мин. риск)"))

        allocation_table = QTableWidget(2, items)
        allocation_table.setHorizontalHeaderLabels(tickets)
        allocation_table.setVerticalHeaderLabels(['Min Volatility', 'Max Sharpe'])

        layout.addWidget(allocation_table, 1, 1, 1, 1)

        headers = table.horizontalHeader()
        headers.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)

        table.setItem(0, 1, QTableWidgetItem(str(analysis_data['year_profit_max_sharpe'])))
        table.setItem(1, 1, QTableWidgetItem(str(analysis_data['year_risk_max_sharpe'])))
        table.setItem(2, 1, QTableWidgetItem(str(analysis_data['sharpe_max_sharpe'])))
        table.setItem(3, 1, QTableWidgetItem(str(analysis_data['year_profit_min_vol'])))
        table.setItem(4, 1, QTableWidgetItem(str(analysis_data['year_risk_min_vol'])))
        table.setItem(5, 1, QTableWidgetItem(str(analysis_data['sharpe_min_vol'])))

        for i in range(0, items):
            allocation_table.setItem(0, i, QTableWidgetItem(str(allocation[i])))
            allocation_table.setItem(1, i, QTableWidgetItem(str(allocation_sharpe[i])))


class BuyWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Новое окно")
        self.setGeometry(300, 300, 300, 200)
        self.setFixedSize(300, 200)

        self.input_label = QLabel("Введите количество (0-10000):", self)
        self.input_label.move(50, 50)

        self.input_textbox = QLineEdit(self)
        self.input_textbox.setValidator(QIntValidator(0, 10000))
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