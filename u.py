# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'u.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1069, 712)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.btnMarket = QtWidgets.QPushButton(self.centralwidget)
        self.btnMarket.setGeometry(QtCore.QRect(10, 10, 141, 51))
        self.btnMarket.setObjectName("btnMarket")
        self.btnPortfolio = QtWidgets.QPushButton(self.centralwidget)
        self.btnPortfolio.setGeometry(QtCore.QRect(190, 10, 131, 51))
        self.btnPortfolio.setObjectName("btnPortfolio")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 80, 941, 541))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.stackedWidget = QtWidgets.QStackedWidget(self.verticalLayoutWidget)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page_1 = QtWidgets.QWidget()
        self.page_1.setObjectName("page_1")
        self.tableMarket = QtWidgets.QTableWidget(self.page_1)
        self.tableMarket.setGeometry(QtCore.QRect(0, 40, 731, 501))
        self.tableMarket.setObjectName("tableMarket")
        self.tableMarket.setColumnCount(4)
        self.tableMarket.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableMarket.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableMarket.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableMarket.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableMarket.setHorizontalHeaderItem(3, item)
        self.tableMarket.horizontalHeader().setCascadingSectionResizes(True)
        self.labelMarket = QtWidgets.QLabel(self.page_1)
        self.labelMarket.setGeometry(QtCore.QRect(360, 0, 331, 41))
        self.labelMarket.setAlignment(QtCore.Qt.AlignCenter)
        self.labelMarket.setObjectName("labelMarket")
        self.btnBuy = QtWidgets.QPushButton(self.page_1)
        self.btnBuy.setGeometry(QtCore.QRect(750, 410, 171, 91))
        self.btnBuy.setObjectName("btnBuy")
        self.addBtnMarket = QtWidgets.QPushButton(self.page_1)
        self.addBtnMarket.setGeometry(QtCore.QRect(760, 310, 71, 41))
        self.addBtnMarket.setObjectName("addBtnMarket")
        self.labelMarkovitzMarket = QtWidgets.QLabel(self.page_1)
        self.labelMarkovitzMarket.setGeometry(QtCore.QRect(750, 30, 181, 31))
        self.labelMarkovitzMarket.setObjectName("labelMarkovitzMarket")
        self.analBtnMarket = QtWidgets.QPushButton(self.page_1)
        self.analBtnMarket.setGeometry(QtCore.QRect(760, 360, 151, 41))
        self.analBtnMarket.setObjectName("analBtnMarket")
        self.rmvBtnMarket = QtWidgets.QPushButton(self.page_1)
        self.rmvBtnMarket.setGeometry(QtCore.QRect(840, 310, 71, 41))
        self.rmvBtnMarket.setObjectName("rmvBtnMarket")
        self.tableAnalMarket = QtWidgets.QTableWidget(self.page_1)
        self.tableAnalMarket.setGeometry(QtCore.QRect(780, 70, 121, 221))
        self.tableAnalMarket.setObjectName("tableAnalMarket")
        self.tableAnalMarket.setColumnCount(1)
        self.tableAnalMarket.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableAnalMarket.setHorizontalHeaderItem(0, item)
        self.searchLinePortfMarket = QtWidgets.QLineEdit(self.page_1)
        self.searchLinePortfMarket.setGeometry(QtCore.QRect(0, 10, 241, 21))
        self.searchLinePortfMarket.setObjectName("searchLinePortfMarket")
        self.searchBtnPortfMarket = QtWidgets.QPushButton(self.page_1)
        self.searchBtnPortfMarket.setGeometry(QtCore.QRect(250, 10, 93, 28))
        self.searchBtnPortfMarket.setObjectName("searchBtnPortfMarket")
        self.stackedWidget.addWidget(self.page_1)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.tablePortfolio = QtWidgets.QTableWidget(self.page_2)
        self.tablePortfolio.setGeometry(QtCore.QRect(0, 40, 731, 501))
        self.tablePortfolio.setObjectName("tablePortfolio")
        self.tablePortfolio.setColumnCount(4)
        self.tablePortfolio.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tablePortfolio.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tablePortfolio.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tablePortfolio.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tablePortfolio.setHorizontalHeaderItem(3, item)
        self.addBtnPortf = QtWidgets.QPushButton(self.page_2)
        self.addBtnPortf.setGeometry(QtCore.QRect(760, 310, 71, 41))
        self.addBtnPortf.setObjectName("addBtnPortf")
        self.analBtnPortf = QtWidgets.QPushButton(self.page_2)
        self.analBtnPortf.setGeometry(QtCore.QRect(760, 360, 151, 41))
        self.analBtnPortf.setObjectName("analBtnPortf")
        self.sellBtnPortf = QtWidgets.QPushButton(self.page_2)
        self.sellBtnPortf.setGeometry(QtCore.QRect(750, 410, 171, 91))
        self.sellBtnPortf.setObjectName("sellBtnPortf")
        self.tableAnalPortf = QtWidgets.QTableWidget(self.page_2)
        self.tableAnalPortf.setGeometry(QtCore.QRect(780, 70, 121, 221))
        self.tableAnalPortf.setObjectName("tableAnalPortf")
        self.tableAnalPortf.setColumnCount(1)
        self.tableAnalPortf.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableAnalPortf.setHorizontalHeaderItem(0, item)
        self.rmvBtnPortf = QtWidgets.QPushButton(self.page_2)
        self.rmvBtnPortf.setGeometry(QtCore.QRect(840, 310, 71, 41))
        self.rmvBtnPortf.setObjectName("rmvBtnPortf")
        self.searchLinePortf = QtWidgets.QLineEdit(self.page_2)
        self.searchLinePortf.setGeometry(QtCore.QRect(0, 10, 241, 21))
        self.searchLinePortf.setObjectName("searchLinePortf")
        self.searchBtnPortf = QtWidgets.QPushButton(self.page_2)
        self.searchBtnPortf.setGeometry(QtCore.QRect(250, 10, 93, 28))
        self.searchBtnPortf.setObjectName("searchBtnPortf")
        self.labelPortf = QtWidgets.QLabel(self.page_2)
        self.labelPortf.setGeometry(QtCore.QRect(360, 0, 331, 31))
        self.labelPortf.setAlignment(QtCore.Qt.AlignCenter)
        self.labelPortf.setObjectName("labelPortf")
        self.labelMarkovitz_2 = QtWidgets.QLabel(self.page_2)
        self.labelMarkovitz_2.setGeometry(QtCore.QRect(750, 30, 181, 31))
        self.labelMarkovitz_2.setObjectName("labelMarkovitz_2")
        self.stackedWidget.addWidget(self.page_2)
        self.verticalLayout.addWidget(self.stackedWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1069, 26))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btnMarket.setText(_translate("MainWindow", "РЫНОК"))
        self.btnPortfolio.setText(_translate("MainWindow", "ПОРТФЕЛЬ"))
        item = self.tableMarket.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "ТИКЕР"))
        item = self.tableMarket.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "НАЗВАНИЕ"))
        item = self.tableMarket.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "ОТРАСЛЬ"))
        item = self.tableMarket.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "ЦЕНА"))
        self.labelMarket.setText(_translate("MainWindow", "РЫНОК"))
        self.btnBuy.setText(_translate("MainWindow", "КУПИТЬ"))
        self.addBtnMarket.setText(_translate("MainWindow", "ДОБАВИТЬ"))
        self.labelMarkovitzMarket.setText(_translate("MainWindow", "МАРКОВИЦ"))
        self.analBtnMarket.setText(_translate("MainWindow", "АНАЛ"))
        self.rmvBtnMarket.setText(_translate("MainWindow", "УБРАТЬ"))
        item = self.tableAnalMarket.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "ТИКЕР"))
        self.searchBtnPortfMarket.setText(_translate("MainWindow", "ПОИСК"))
        item = self.tablePortfolio.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "ТИКЕР"))
        item = self.tablePortfolio.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "НАЗВАНИЕ"))
        item = self.tablePortfolio.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "ОТРАСЛЬ"))
        item = self.tablePortfolio.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "ЦЕНА"))
        self.addBtnPortf.setText(_translate("MainWindow", "ДОБАВИТЬ"))
        self.analBtnPortf.setText(_translate("MainWindow", "АНАЛ"))
        self.sellBtnPortf.setText(_translate("MainWindow", "ПРОДАТЬ"))
        item = self.tableAnalPortf.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "ТИКЕР"))
        self.rmvBtnPortf.setText(_translate("MainWindow", "УБРАТЬ"))
        self.searchBtnPortf.setText(_translate("MainWindow", "ПОИСК"))
        self.labelPortf.setText(_translate("MainWindow", "ПОРТФЕЛЬ"))
        self.labelMarkovitz_2.setText(_translate("MainWindow", "МАРКОВИЦ"))
        self.menu.setTitle(_translate("MainWindow", "sdf"))
