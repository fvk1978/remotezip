#!/usr/bin/env python

from zip import ZipFile
from qt_gui import Ui_MainWindow
from PyQt4 import QtCore, QtGui
import os, sys


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    # Maintain the list of browser windows so that they do not get garbage
    # collected.
    _window_list = []

    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        MainWindow._window_list.append(self)

        self.setupUi(self)
        
        self.URLlineEdit.setText('')
        
        # default output dir
        self.lineEdit.setText('./')

        # Qt Designer (at least to v4.2.1) can't handle arbitrary widgets in a
        # QToolBar - even though uic can, and they are in the original .ui
        # file.  Therefore we manually add the problematic widgets.
        """
        self.lblAddress = QtGui.QLabel("Address", self.tbAddress)
        self.tbAddress.insertWidget(self.actionGo, self.lblAddress)
        self.addressEdit = QtGui.QLineEdit(self.tbAddress)
        self.tbAddress.insertWidget(self.actionGo, self.addressEdit)

        self.connect(self.addressEdit, QtCore.SIGNAL("returnPressed()"),
                     self.actionGo, QtCore.SLOT("trigger()"))
        self.connect(self.actionBack, QtCore.SIGNAL("triggered()"),
                     self.WebBrowser, QtCore.SLOT("GoBack()"))
        self.connect(self.actionForward, QtCore.SIGNAL("triggered()"),
                     self.WebBrowser, QtCore.SLOT("GoForward()"))
        self.connect(self.actionStop, QtCore.SIGNAL("triggered()"),
                     self.WebBrowser, QtCore.SLOT("Stop()"))
        self.connect(self.actionRefresh, QtCore.SIGNAL("triggered()"),
                     self.WebBrowser, QtCore.SLOT("Refresh()"))
        self.connect(self.actionHome, QtCore.SIGNAL("triggered()"),
                     self.WebBrowser, QtCore.SLOT("GoHome()"))
        self.connect(self.actionSearch, QtCore.SIGNAL("triggered()"),
                     self.WebBrowser, QtCore.SLOT("GoSearch()"))

        self.pb = QtGui.QProgressBar(self.statusBar())
        self.pb.setTextVisible(False)
        self.pb.hide()
        self.statusBar().addPermanentWidget(self.pb)
        """

        self.connect(self.pushButton_2, QtCore.SIGNAL("clicked()"), self.browse)
        self.connect(self.StartpushButton, QtCore.SIGNAL("clicked()"), self.get_file_list)
        self.connect(self.pushButton, QtCore.SIGNAL("clicked()"), self.get_files)
    
    def closeEvent(self, e):
        MainWindow._window_list.remove(self)
        e.accept()

    def browse(self):
        directory = QtGui.QFileDialog.getExistingDirectory(self, self.tr("Output directory"),
                                                           QtCore.QDir.currentPath())
        if directory:
            self.lineEdit.setText(directory)

    def get_file_list(self):
        url = str(self.URLlineEdit.text())
        if url == '':
            QtGui.QMessageBox.warning(self, self.tr("Get remote zip content"),
                   self.tr("Specify URL please"),
                   QtGui.QMessageBox.AcceptRole, QtGui.QMessageBox.Escape);
            return
        
        self.StartpushButton.setDisabled(True)
        
        self.z = ZipFile(url)
        #print z.file_list()
        model = QtGui.QStandardItemModel(0, 4, self)
        model.setHeaderData(0, QtCore.Qt.Horizontal, QtCore.QVariant("File name"))
        model.setHeaderData(1, QtCore.Qt.Horizontal, QtCore.QVariant("Compressed size"))
        model.setHeaderData(2, QtCore.Qt.Horizontal, QtCore.QVariant("Uncompressed size"))
        model.setHeaderData(3, QtCore.Qt.Horizontal, QtCore.QVariant("File date"))
        
        from datetime import date, time
        for filename in self.z.TOC:
            #print type(z.TOC[filename][1])
            compressed_size = self.z.TOC[filename][7]
            uncompressed_size = self.z.TOC[filename][8]
            d = self.z.TOC[filename][9]
            t = self.z.TOC[filename][10]
            
            model = self.add_file_item(model, filename, compressed_size, uncompressed_size,
                    QtCore.QDateTime(QtCore.QDate(d[0],d[1],d[2]), QtCore.QTime(t[0],t[1],t[2])))
            
            self.treeView.setModel(model)
        
        self.StartpushButton.setEnabled(True)

    def add_file_item(self, model, filename, compressed_size, uncompressed_size, date):
        model.insertRow(0)
        model.setData(model.index(0, 0), QtCore.QVariant(filename))
        model.setData(model.index(0, 1), QtCore.QVariant(compressed_size))
        model.setData(model.index(0, 2), QtCore.QVariant(uncompressed_size))
        model.setData(model.index(0, 3), QtCore.QVariant(date))
        
        return model
    
    def get_files(self):
        files = []
        for index in self.treeView.selectedIndexes():
            if index.column() == 0:
                data = str(index.data().toString())
                files.append(data)

        if files == []:
            QtGui.QMessageBox.warning(self, self.tr("Get remote zip content"),
                   self.tr("Select file(s) please"),
                   QtGui.QMessageBox.AcceptRole, QtGui.QMessageBox.Escape);
            return
        
        self.pushButton.setDisabled(True)

        self.progressBar.setMaximum(len(files))
        self.progressBar.setValue(0)
        
        directory = str(self.lineEdit.text())
        for file in files:
            fd, fn = os.path.split(file)
            self.statusBar().showMessage("downloding file " + fn)
            self.z.get(file, directory)
            self.progressBar.setValue(self.progressBar.value() + 1)

        self.statusBar().showMessage("Done")
        self.pushButton.setEnabled(True)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())
