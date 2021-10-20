# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 720)
        MainWindow.setAutoFillBackground(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(20, 80, 640, 360))
        self.groupBox.setObjectName("groupBox")
        self.screen = QtWidgets.QLabel(self.groupBox)
        self.screen.setGeometry(QtCore.QRect(0, 0, 640, 360))
        self.screen.setAutoFillBackground(True)
        self.screen.setFrameShape(QtWidgets.QFrame.Box)
        self.screen.setAlignment(QtCore.Qt.AlignCenter)
        self.screen.setObjectName("screen")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(30, 559, 1001, 101))
        self.groupBox_2.setObjectName("groupBox_2")
        self.ledTrigger = QtWidgets.QLabel(self.groupBox_2)
        self.ledTrigger.setGeometry(QtCore.QRect(10, 20, 60, 60))
        self.ledTrigger.setAutoFillBackground(True)
        self.ledTrigger.setFrameShape(QtWidgets.QFrame.Box)
        self.ledTrigger.setAlignment(QtCore.Qt.AlignCenter)
        self.ledTrigger.setWordWrap(True)
        self.ledTrigger.setObjectName("ledTrigger")
        self.id = QtWidgets.QLabel(self.groupBox_2)
        self.id.setGeometry(QtCore.QRect(120, 30, 111, 41))
        self.id.setAutoFillBackground(True)
        self.id.setFrameShape(QtWidgets.QFrame.Box)
        self.id.setAlignment(QtCore.Qt.AlignCenter)
        self.id.setObjectName("id")
        self.account = QtWidgets.QLabel(self.groupBox_2)
        self.account.setGeometry(QtCore.QRect(660, 30, 121, 41))
        self.account.setAutoFillBackground(True)
        self.account.setFrameShape(QtWidgets.QFrame.Box)
        self.account.setAlignment(QtCore.Qt.AlignCenter)
        self.account.setObjectName("account")
        self.line = QtWidgets.QFrame(self.groupBox_2)
        self.line.setGeometry(QtCore.QRect(620, 20, 3, 61))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.MoneyLeft = QtWidgets.QLCDNumber(self.groupBox_2)
        self.MoneyLeft.setGeometry(QtCore.QRect(800, 30, 191, 41))
        self.MoneyLeft.setObjectName("MoneyLeft")
        self.InputID = QtWidgets.QLineEdit(self.groupBox_2)
        self.InputID.setGeometry(QtCore.QRect(250, 30, 251, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.InputID.setFont(font)
        self.InputID.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.InputID.setAutoFillBackground(True)
        self.InputID.setClearButtonEnabled(False)
        self.InputID.setObjectName("InputID")
        self.confirmButton = QtWidgets.QPushButton(self.groupBox_2)
        self.confirmButton.setGeometry(QtCore.QRect(514, 30, 71, 41))
        self.confirmButton.setObjectName("confirmButton")
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(670, 0, 351, 71))
        self.groupBox_3.setObjectName("groupBox_3")
        self.label_2 = QtWidgets.QLabel(self.groupBox_3)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 71, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox_3)
        self.label_3.setGeometry(QtCore.QRect(180, 10, 71, 16))
        self.label_3.setObjectName("label_3")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.groupBox_3)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 30, 331, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.SlotCount = QtWidgets.QLCDNumber(self.horizontalLayoutWidget)
        self.SlotCount.setObjectName("SlotCount")
        self.horizontalLayout_2.addWidget(self.SlotCount)
        self.TotalSlot = QtWidgets.QLCDNumber(self.horizontalLayoutWidget)
        self.TotalSlot.setObjectName("TotalSlot")
        self.horizontalLayout_2.addWidget(self.TotalSlot)
        self.groupBox_4 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_4.setGeometry(QtCore.QRect(670, 460, 361, 81))
        self.groupBox_4.setObjectName("groupBox_4")
        self.extractedInfo = QtWidgets.QLabel(self.groupBox_4)
        self.extractedInfo.setGeometry(QtCore.QRect(10, 20, 251, 51))
        self.extractedInfo.setAutoFillBackground(True)
        self.extractedInfo.setFrameShape(QtWidgets.QFrame.Box)
        self.extractedInfo.setAlignment(QtCore.Qt.AlignCenter)
        self.extractedInfo.setObjectName("extractedInfo")
        self.VerifyBox = QtWidgets.QLabel(self.groupBox_4)
        self.VerifyBox.setGeometry(QtCore.QRect(270, 20, 81, 51))
        self.VerifyBox.setAutoFillBackground(True)
        self.VerifyBox.setFrameShape(QtWidgets.QFrame.Box)
        self.VerifyBox.setAlignment(QtCore.Qt.AlignCenter)
        self.VerifyBox.setObjectName("VerifyBox")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(1050, 40, 221, 621))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setMouseTracking(True)
        self.tableWidget.setAutoFillBackground(True)
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setGridStyle(QtCore.Qt.SolidLine)
        self.tableWidget.setRowCount(20)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(12, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(60)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(10)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(True)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(True)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setDefaultSectionSize(30)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(1070, 10, 181, 21))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(50, 10, 571, 51))
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(670, 80, 361, 361))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.ViewLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.ViewLayout.setContentsMargins(0, 0, 0, 0)
        self.ViewLayout.setObjectName("ViewLayout")
        self.ViewPlateIn = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.ViewPlateIn.setAutoFillBackground(True)
        self.ViewPlateIn.setFrameShape(QtWidgets.QFrame.Box)
        self.ViewPlateIn.setAlignment(QtCore.Qt.AlignCenter)
        self.ViewPlateIn.setObjectName("ViewPlateIn")
        self.ViewLayout.addWidget(self.ViewPlateIn)
        self.ViewPlateOut = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.ViewPlateOut.setAutoFillBackground(True)
        self.ViewPlateOut.setFrameShape(QtWidgets.QFrame.Box)
        self.ViewPlateOut.setAlignment(QtCore.Qt.AlignCenter)
        self.ViewPlateOut.setObjectName("ViewPlateOut")
        self.ViewLayout.addWidget(self.ViewPlateOut)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(40, 450, 591, 91))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.ControlLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.ControlLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.ControlLayout.setContentsMargins(0, 0, 0, 0)
        self.ControlLayout.setObjectName("ControlLayout")
        self.startButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.startButton.sizePolicy().hasHeightForWidth())
        self.startButton.setSizePolicy(sizePolicy)
        self.startButton.setObjectName("startButton")
        self.ControlLayout.addWidget(self.startButton)
        self.stopButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stopButton.sizePolicy().hasHeightForWidth())
        self.stopButton.setSizePolicy(sizePolicy)
        self.stopButton.setObjectName("stopButton")
        self.ControlLayout.addWidget(self.stopButton)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "CameraView"))
        self.screen.setText(_translate("MainWindow", "CameraView"))
        self.groupBox_2.setTitle(_translate("MainWindow", "ControlPanel"))
        self.ledTrigger.setText(_translate("MainWindow", "Trigger"))
        self.id.setText(_translate("MainWindow", "ID scan from ID card"))
        self.account.setText(_translate("MainWindow", "Money left in account"))
        self.confirmButton.setText(_translate("MainWindow", "Cofirm"))
        self.groupBox_3.setTitle(_translate("MainWindow", "GroupBox"))
        self.label_2.setText(_translate("MainWindow", "Count"))
        self.label_3.setText(_translate("MainWindow", "Max"))
        self.groupBox_4.setTitle(_translate("MainWindow", "Plate number"))
        self.extractedInfo.setText(_translate("MainWindow", "Plate number"))
        self.VerifyBox.setText(_translate("MainWindow", "Verify"))
        self.tableWidget.setSortingEnabled(True)
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "1"))
        item = self.tableWidget.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "2"))
        item = self.tableWidget.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "3"))
        item = self.tableWidget.verticalHeaderItem(3)
        item.setText(_translate("MainWindow", "4"))
        item = self.tableWidget.verticalHeaderItem(4)
        item.setText(_translate("MainWindow", "5"))
        item = self.tableWidget.verticalHeaderItem(5)
        item.setText(_translate("MainWindow", "6"))
        item = self.tableWidget.verticalHeaderItem(6)
        item.setText(_translate("MainWindow", "7"))
        item = self.tableWidget.verticalHeaderItem(7)
        item.setText(_translate("MainWindow", "8"))
        item = self.tableWidget.verticalHeaderItem(8)
        item.setText(_translate("MainWindow", "9"))
        item = self.tableWidget.verticalHeaderItem(9)
        item.setText(_translate("MainWindow", "10"))
        item = self.tableWidget.verticalHeaderItem(10)
        item.setText(_translate("MainWindow", "11"))
        item = self.tableWidget.verticalHeaderItem(11)
        item.setText(_translate("MainWindow", "12"))
        item = self.tableWidget.verticalHeaderItem(12)
        item.setText(_translate("MainWindow", "13"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Item"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Value"))
        self.label_4.setText(_translate("MainWindow", "PLC tracking value"))
        self.label_5.setText(_translate("MainWindow", "License Plate recognition for smart parking station"))
        self.ViewPlateIn.setText(_translate("MainWindow", "CameraViewIn"))
        self.ViewPlateOut.setText(_translate("MainWindow", "CameraViewOut"))
        self.startButton.setText(_translate("MainWindow", "Start"))
        self.stopButton.setText(_translate("MainWindow", "Stop"))
