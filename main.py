# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
from PyQt5 import QtCore, QtWidgets
import sys , typing

APP = QtWidgets.QApplication(sys.argv)


from qmodels import (
    SharingDataFrame , 
    MyMessageBox , 
    MyTableModel ,
    GifWidget ,
    Checking ,
)
from tasks import TasksContainer
from readers import (
     COLUMNS ,
     TABEL_MODEL_COLUMNS ,
     ExcelReader ,
)


class Ui_MainWindow(QtWidgets.QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        # Define Attributes
        self.message = MyMessageBox()
        self.sharingdata = SharingDataFrame(COLUMNS,self)
        self.taskscontainer  = TasksContainer(self.sharingdata)
        self.tableModel = MyTableModel(TABEL_MODEL_COLUMNS)
        self.loadingWidget = GifWidget(self,'')
        self.internet = Checking()



    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(681, 519)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.topFrame = QtWidgets.QFrame(self.widget)
        self.topFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.topFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.topFrame.setObjectName("topFrame")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.topFrame)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.loadsheetBtn = QtWidgets.QToolButton(self.topFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.loadsheetBtn.sizePolicy().hasHeightForWidth())
        self.loadsheetBtn.setSizePolicy(sizePolicy)
        self.loadsheetBtn.setObjectName("loadsheetBtn")
        self.horizontalLayout_4.addWidget(self.loadsheetBtn)
        self.filenameFrame = QtWidgets.QFrame(self.topFrame)
        self.filenameFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.filenameFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.filenameFrame.setObjectName("filenameFrame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.filenameFrame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.filenameLabel = QtWidgets.QLabel(self.filenameFrame)
        self.filenameLabel.setObjectName("filenameLabel")
        self.horizontalLayout_2.addWidget(self.filenameLabel, 0, QtCore.Qt.AlignHCenter)
        self.filenameValue = QtWidgets.QLabel(self.filenameFrame)
        self.filenameValue.setObjectName("filenameValue")
        self.horizontalLayout_2.addWidget(self.filenameValue, 0, QtCore.Qt.AlignHCenter)
        self.horizontalLayout_4.addWidget(self.filenameFrame)
        self.watingFrame = QtWidgets.QFrame(self.topFrame)
        self.watingFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.watingFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.watingFrame.setObjectName("watingFrame")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.watingFrame)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.waitingLabel = QtWidgets.QLabel(self.watingFrame)
        self.waitingLabel.setObjectName("waitingLabel")
        self.horizontalLayout_3.addWidget(self.waitingLabel, 0, QtCore.Qt.AlignRight)
        self.waitingValue = QtWidgets.QLabel(self.watingFrame)
        self.waitingValue.setObjectName("waitingValue")
        self.horizontalLayout_3.addWidget(self.waitingValue, 0, QtCore.Qt.AlignLeft)
        self.horizontalLayout_4.addWidget(self.watingFrame)
        self.horizontalLayout_4.setStretch(0, 1)
        self.horizontalLayout_4.setStretch(1, 1)
        self.horizontalLayout_4.setStretch(2, 1)
        self.verticalLayout_2.addWidget(self.topFrame)
        self.midFrame = QtWidgets.QFrame(self.widget)
        self.midFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.midFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.midFrame.setObjectName("midFrame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.midFrame)
        self.horizontalLayout.setSpacing(25)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.startBtn = QtWidgets.QToolButton(self.midFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.startBtn.sizePolicy().hasHeightForWidth())
        self.startBtn.setSizePolicy(sizePolicy)
        self.startBtn.setObjectName("startBtn")
        self.horizontalLayout.addWidget(self.startBtn)
        self.stopBtn = QtWidgets.QToolButton(self.midFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stopBtn.sizePolicy().hasHeightForWidth())
        self.stopBtn.setSizePolicy(sizePolicy)
        self.stopBtn.setObjectName("stopBtn")
        self.horizontalLayout.addWidget(self.stopBtn)
        self.verticalLayout_2.addWidget(self.midFrame)
        self.botFrame = QtWidgets.QFrame(self.widget)
        self.botFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.botFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.botFrame.setObjectName("botFrame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.botFrame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableView = QtWidgets.QTableView(self.botFrame)
        self.tableView.setObjectName("tableView")
        # Connect tabel view with Model
        self.tableView.setModel(self.tableModel)
        self.verticalLayout.addWidget(self.tableView)
        self.exportFrame = QtWidgets.QFrame(self.botFrame)
        self.exportFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.exportFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.exportFrame.setObjectName("exportFrame")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.exportFrame)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.counterFrame = QtWidgets.QFrame(self.exportFrame)
        self.counterFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.counterFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.counterFrame.setObjectName("counterFrame")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.counterFrame)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.counterLabel = QtWidgets.QLabel(self.counterFrame)
        self.counterLabel.setObjectName("counterLabel")
        self.horizontalLayout_5.addWidget(self.counterLabel, 0, QtCore.Qt.AlignRight)
        self.CounterValue = QtWidgets.QLabel(self.counterFrame)
        self.CounterValue.setObjectName("CounterValue")
        self.horizontalLayout_5.addWidget(self.CounterValue, 0, QtCore.Qt.AlignLeft)
        self.horizontalLayout_6.addWidget(self.counterFrame)
        self.statusFrame = QtWidgets.QFrame(self.exportFrame)
        self.statusFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.statusFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.statusFrame.setObjectName("statusFrame")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.statusFrame)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.statusLabel = QtWidgets.QLabel(self.statusFrame)
        self.statusLabel.setObjectName("statusLabel")
        self.horizontalLayout_5.addWidget(self.statusLabel, 0, QtCore.Qt.AlignRight)
        self.statusValue = QtWidgets.QLabel(self.statusFrame)
        self.statusValue.setObjectName("statusValue")
        self.horizontalLayout_5.addWidget(self.statusValue, 0, QtCore.Qt.AlignLeft)
        self.horizontalLayout_6.addWidget(self.statusFrame)
        self.exportBtn = QtWidgets.QPushButton(self.exportFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exportBtn.sizePolicy().hasHeightForWidth())
        self.exportBtn.setSizePolicy(sizePolicy)
        self.exportBtn.setObjectName("exportBtn")
        self.horizontalLayout_6.addWidget(self.exportBtn)
        self.verticalLayout.addWidget(self.exportFrame)
        self.verticalLayout_2.addWidget(self.botFrame)
        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 2)
        self.verticalLayout_2.setStretch(2, 8)
        self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)
        # set window title 
        self.setWindowTitle("الفواتير")

        # rename Labels 
        self.filenameLabel.setText("File Name :")
        self.filenameValue.setText("test.xlsx")

        self.waitingLabel.setText("Waiting :")
        self.waitingValue.setText("")

        self.counterLabel.setText("Count :")
        self.CounterValue.setText("")

        self.statusLabel.setText("Status : ")

        # rename btns 
        self.exportBtn.setText("Export")
        
        self.startBtn.setText("Start")
        self.stopBtn.setText("Stop")

        self.loadsheetBtn.setText("Load Excel")

        self.statusValue.setText("OFF")
        # connect load excel signal 
        self.loadsheetBtn.clicked.connect(self.getFileDir)

        # Run ui constants
        self.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(self)


    # show function that override original method and run app methods
    def show(self) -> None:
        # if self.internet.isConnect():
            self.setupUi()
            super().show()
            sys.exit(APP.exec_())
        # else :
        #     self.message.showCritical('Please Check internet Connection','Error')


    # method to get excel path ==================================================================
    def getFileDir(self):
        file_filter = 'Data File (*.xlsx );; Excel File (*.xlsx )'
        dir = QtWidgets.QFileDialog.getOpenFileName(
            caption='Select a data file',
            filter=file_filter,
            )[0]
        self.filenameValue.setText(dir.split("/")[-1])


if __name__ == "__main__":
    ui = Ui_MainWindow()
    ui.show()
    
