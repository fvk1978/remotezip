# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './resources/remote_zip.ui'
#
# Created: Sun Feb 10 13:03:58 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(QtCore.QSize(QtCore.QRect(0,0,760,580).size()).expandedTo(MainWindow.minimumSizeHint()))
        MainWindow.setWindowIcon(QtGui.QIcon("./resources/download.png"))

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridlayout = QtGui.QGridLayout(self.centralwidget)
        self.gridlayout.setObjectName("gridlayout")

        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")

        self.hboxlayout = QtGui.QHBoxLayout(self.groupBox)
        self.hboxlayout.setObjectName("hboxlayout")

        self.URLlineEdit = QtGui.QLineEdit(self.groupBox)
        self.URLlineEdit.setObjectName("URLlineEdit")
        self.hboxlayout.addWidget(self.URLlineEdit)

        self.StartpushButton = QtGui.QPushButton(self.groupBox)
        self.StartpushButton.setIcon(QtGui.QIcon("./resources/connect.png"))
        self.StartpushButton.setObjectName("StartpushButton")
        self.hboxlayout.addWidget(self.StartpushButton)
        self.gridlayout.addWidget(self.groupBox,0,0,1,1)

        self.groupBox_2 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName("groupBox_2")

        self.gridlayout1 = QtGui.QGridLayout(self.groupBox_2)
        self.gridlayout1.setObjectName("gridlayout1")

        self.proxyModel = QtGui.QSortFilterProxyModel()
        self.proxyModel.setDynamicSortFilter(True)
        
        self.treeView = QtGui.QTreeView(self.groupBox_2)
        self.treeView.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.treeView.setObjectName("treeView")
        self.treeView.setRootIsDecorated(False)
        self.treeView.setAlternatingRowColors(True)
        self.treeView.setModel(self.proxyModel)
        self.treeView.setSortingEnabled(True)
        self.gridlayout1.addWidget(self.treeView,0,0,1,1)
        self.treeView.sortByColumn(0, QtCore.Qt.AscendingOrder)

        self.pushButton = QtGui.QPushButton(self.groupBox_2)
        self.pushButton.setIcon(QtGui.QIcon("./resources/download.png"))
        self.pushButton.setObjectName("pushButton")
        self.gridlayout1.addWidget(self.pushButton,1,0,1,1)
        self.gridlayout.addWidget(self.groupBox_2,1,0,1,1)

        self.groupBox_3 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName("groupBox_3")

        self.hboxlayout1 = QtGui.QHBoxLayout(self.groupBox_3)
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.lineEdit = QtGui.QLineEdit(self.groupBox_3)
        self.lineEdit.setObjectName("lineEdit")
        self.hboxlayout1.addWidget(self.lineEdit)

        self.progressBar = QtGui.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value",QtCore.QVariant(0))
        self.progressBar.setObjectName("progressBar")
        self.gridlayout.addWidget(self.progressBar,3,0,1,1)

        self.pushButton_2 = QtGui.QPushButton(self.groupBox_3)
        self.pushButton_2.setIcon(QtGui.QIcon("./resources/dir.png"))
        self.pushButton_2.setObjectName("pushButton_2")
        self.hboxlayout1.addWidget(self.pushButton_2)
        self.gridlayout.addWidget(self.groupBox_3,2,0,1,1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0,0,760,26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def sortChanged(self):
        self.proxyModel.setSortCaseSensitivity(caseSensitivity)
        
    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Get files from remote zip archive", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("MainWindow", "Zip file URL", None, QtGui.QApplication.UnicodeUTF8))
        self.StartpushButton.setText(QtGui.QApplication.translate("MainWindow", "Connect", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("MainWindow", "File list", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("MainWindow", "Download selected files", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("MainWindow", "Output directory", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("MainWindow", "Change directory", None, QtGui.QApplication.UnicodeUTF8))


