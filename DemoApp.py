
from PyQt5 import QtCore, QtWidgets , QtGui
from MyPyQt5 import MyQTreeWidget , MyCustomContextMenu,MyMessageBox,MyThread,pyqtSignal
import typing,datetime,openpyxl,pandas,time
from mainclassDemo import WePay
import numpy as np
from ProxyFilterClass import ProxyFilterAPI
import json


class Ui_MainWindow(object):
    def setupUi(self, MainWindow:QtWidgets.QMainWindow):
        self.msg = MyMessageBox()
        MainWindow.resize(600, 457)
        MainWindow.setMaximumHeight(457)
        MainWindow.setMinimumHeight(457)
        MainWindow.setMaximumWidth(600)
        MainWindow.setMinimumWidth(600)
        font = QtGui.QFont()
        font.setPointSize(14)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(339, 80, 251, 41))
        self.pushButton.setFont(font)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 80, 251, 41))
        self.pushButton_2.setFont(font)
        self.toolButton = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton.setGeometry(QtCore.QRect(470, 20, 51, 21))
        self.toolButton.clicked.connect(self.dialog)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(180, 20, 281, 20))
        self.lineEdit.setReadOnly(True)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setFont(font)
        self.label.setGeometry(QtCore.QRect(50, 20, 61, 21))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setPlaceholderText("Defult: Sheet1")
        self.lineEdit_2.setGeometry(QtCore.QRect(230, 50, 231, 20))
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setFont(font)
        self.label_2.setGeometry(QtCore.QRect(45, 50, 111, 31))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        font.setPointSize(10)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(190, 430, 100, 25))
        self.label_4.setText(f"Count : 0")
        self.label_4.setFont(font)
        self.treeWidget = MyQTreeWidget(self.centralwidget,self.label_4)
        self.treeWidget.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.treeWidget.customContextMenuRequested.connect(self.contextMenu)
        self.treeWidget.setGeometry(QtCore.QRect(10, 130, 580, 301))
        self.treeWidget.setColumns(["AreaCode","PhoneNumber","HasInvoice","InvoiceDate",'SubscribtionEnd',"TotalAmount"])
        self.statusLabel = QtWidgets.QLabel(self.centralwidget)
        self.statusLabel.setText("Stopped")
        self.statusLabel.setGeometry(QtCore.QRect(390, 430, 100, 25))
        self.statusLabel.setFont(font)
        self.Thread = Thread()
        self.Thread.setMainClass(self)
        self.Thread.msg.connect(self.msg.showInfo)
        self.Thread.Lead.connect(self.appendData)
        self.Thread.statues.connect(self.statusLabel.setText)
        self.pushButton_2.clicked.connect(self.Thread.start)
        self.pushButton.clicked.connect(lambda : self.Thread.kill(msg="يا عم بطل رخامة بقاا -_-"))


        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Stop"))
        self.pushButton_2.setText(_translate("MainWindow", "Start"))
        self.toolButton.setText(_translate("MainWindow", "..."))
        self.label.setText(_translate("MainWindow", "File"))
        self.label_2.setText(_translate("MainWindow", "Sheet Name"))

    def appendData(self,lead):
        if lead[2] == 'True':
            lead[2] = 'يوجد فاتورة'
        elif lead[2] == 'False':
            lead[2] = 'لايوجد فواتير'
        elif lead[2] == 'NoAccount':
            lead[2] = 'لايوجد حساب لهذا العميل'
        self.treeWidget.appendData(lead)

    def contextMenu(self):
        menu = MyCustomContextMenu([
        "Delete Row" , # 3
        "Export All To Excel", # 4
        "Clear Results", # 10
        ])
        menu.multiConnect(functions=[
            lambda: self.delete() , # 3
            lambda: self.export(f"Hour{datetime.datetime.now().hour}Minute{datetime.datetime.now().minute}") , # 4  {datetime.datetime.now().date()} | 
            lambda: self.treeWidget.clear() , # 10
        ])
        menu.show()


    def delete(self):
        try:
            self.treeWidget.takeTopLevelItem(self.treeWidget.indexOfTopLevelItem(self.treeWidget.currentItem()))
        except:
            self.msg.showWarning(text="No Item Selected please Select one !")


    def export(self,name:typing.Optional[str]):
        if self.treeWidget._ROW_INDEX > 0 :
            self.treeWidget.extract_data_to_DataFrame().to_excel(f"Data/Exports/{name}[{datetime.datetime.now().date()}].xlsx",index=False)
            self.msg.showInfo(text=f"Exported Succecfully to 'Data/Exports/{name}[{datetime.datetime.now().date()}].xlsx'")
        else :
            self.msg.showWarning(text="No Data In App Please Try Again Later")


    def dialog(self):
        file_filter = 'Data File (*.xlsx *.csv);; Excel File (*.xlsx *.xls)'
        dir = QtWidgets.QFileDialog.getOpenFileName(
            caption='Select a data file',
            filter=file_filter,
            )[0]
        self.lineEdit.setText(dir)
    
    def reshapeExelData(self,excelfile,sheetname):
        wb = openpyxl.load_workbook(excelfile)
        ws = wb[sheetname]
        df = pandas.DataFrame(ws.values)
        response = []
        for row in df.index:
            res = (f"{df.iloc[row][0]}",f"{df.iloc[row][1]}")
            response.append(res)
        return response[1:]


class Thread(MyThread):
    Lead = pyqtSignal(list)
    msg = pyqtSignal(str)

    def setMainClass(self, mainClass: Ui_MainWindow):
        self.mainClass = mainClass

    def run(self) -> None:
        if self.mainClass.lineEdit.text() != "":
            self.statues.emit("Starting ...")
            listOfPhones =  self.mainClass.reshapeExelData(
                excelfile = self.mainClass.lineEdit.text() , 
                sheetname = "Sheet1" if self.mainClass.lineEdit_2.text() == "" or self.mainClass.lineEdit_2.text() == " " else self.mainClass.lineEdit_2.text()
            )
            # listOfPhones = list(set(listOfPhones))
            totalNumbers = len(listOfPhones)
            myrange = listOfPhones[::70]
            listOfPhones = np.array_split(listOfPhones,len(myrange))
            print(totalNumbers)
            t1 = time.time()
            try:
                for phones in listOfPhones:
                    print(f'Starting with {phones}') 
                    self.statues.emit("Opening Browser")                   
                    self.we = WePay()
                    self.we.Lead.connect(self.Lead.emit)
                    self.mainClass.lineEdit.clear()
                    self.statues.emit("Start Scraping ... ")
                    self.we.ScrapePhonesList(phones)
                    self.statues.emit("End Scraping ... ")
                    self.we.exit()
                    self.statues.emit("Closing Browser")
                t2 = time.time()
                self.statues.emit("Stopped")        
                print(f"\n {t2-t1} Is Total time for make {totalNumbers} number \n")
                self.msg.emit(f"\n {round(t2-t1,ndigits=4)} Is Total time for make {totalNumbers} number \nنورتنا يا رجولة متجيش تانى بقاا ^_-")
            except Exception as e :
                self.msg.emit(f"Error in {e}\nPlease Contact Hesham To Solve it")



    def kill(self, msg: typing.Optional[bool]):
        try:
            self.we.exit()
        except Exception as e :
            pass
        super().kill("Stopped")
        self.statues.emit("Stopped")        
        self.msg.emit(msg) if msg != None else None
     





if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
