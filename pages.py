from PyQt5 import QtCore, QtWidgets
import pyperclip , typing 
from datetime import datetime
from styles import Styles
from MyPyQt5 import (
    QObject ,
    pyqtSignal ,
    AnimatedToggle ,
    MyQTreeWidget ,
    MyCustomContextMenu ,
    MyMessageBox ,
    )



class Page1(QObject):
    msg = MyMessageBox()
    def __init__(self, parent:QObject) -> None:
        super().__init__()
        
        self.ExportRange =  {'AreaCode':0,'PhoneNumber':1,'HasInvoice':2,'InvoiceDate':3 ,'SubscribtionEnd':4,'TotalAmount':5,'Time Scraping':6}
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(parent)
        self.firstFrame = QtWidgets.QFrame(parent)
        self.firstFrame.setStyleSheet(Styles.Frame.Normal)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.firstFrame)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(30)
        self.exportFrame = QtWidgets.QFrame(self.firstFrame)
        self.exportFrame.setStyleSheet(Styles.Frame.Normal)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.exportFrame)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QtWidgets.QLabel(self.exportFrame)
        self.label_3.setText('Export Sheet Name')
        self.horizontalLayout_4.addWidget(self.label_3, 0, QtCore.Qt.AlignHCenter)
        self.lineEdit = QtWidgets.QLineEdit(self.exportFrame)
        self.lineEdit.setPlaceholderText('Export Sheet Name')
        self.horizontalLayout_4.addWidget(self.lineEdit)
        self.horizontalLayout_4.setStretch(0, 1)
        self.horizontalLayout_4.setStretch(1, 2)
        self.horizontalLayout_5.addWidget(self.exportFrame)
        self.taskFrame = QtWidgets.QFrame(self.firstFrame)
        self.taskFrame.setStyleSheet(Styles.Frame.Normal)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.taskFrame)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QtWidgets.QLabel(self.taskFrame)
        self.label_2.setText('Tasks')
        self.horizontalLayout_3.addWidget(self.label_2, 0, QtCore.Qt.AlignHCenter)
        self.comboBox = QtWidgets.QComboBox(self.taskFrame)
        self.comboBox.setStyleSheet(Styles.ComboBox.Normal)
        self.comboBox.currentIndexChanged.connect(self.combochanged)
        self.horizontalLayout_3.addWidget(self.comboBox)
        self.horizontalLayout_5.addWidget(self.taskFrame)
        self.horizontalLayout_5.setStretch(0, 3)
        self.horizontalLayout_5.setStretch(1, 2)
        self.verticalLayout_2.addWidget(self.firstFrame)
        self.buttonsFrame = QtWidgets.QFrame(parent)
        self.buttonsFrame.setStyleSheet(Styles.Frame.Normal)
        self.ThreadHbox = QtWidgets.QHBoxLayout(self.buttonsFrame)
        self.startbtn = QtWidgets.QToolButton(self.buttonsFrame)
        self.startbtn.setText("Start")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.startbtn.setSizePolicy(sizePolicy)
        self.ThreadHbox.addWidget(self.startbtn)
        self.label = QtWidgets.QLabel(self.buttonsFrame)
        self.label.setText("    Current Task\n         ")
        self.ThreadHbox.addWidget(self.label)
        self.stopbtn = QtWidgets.QToolButton(self.buttonsFrame)
        self.stopbtn.setText("Stop")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.stopbtn.setSizePolicy(sizePolicy)
        self.ThreadHbox.addWidget(self.stopbtn)
        self.ThreadHbox.setStretch(0, 5)
        self.ThreadHbox.setStretch(1, 3)
        self.ThreadHbox.setStretch(2, 5)
        self.verticalLayout_2.addWidget(self.buttonsFrame)
        self.treeFrame = QtWidgets.QFrame(parent)
        self.treeFrame.setStyleSheet(Styles.Frame.Normal)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.treeFrame)
        self.frame = QtWidgets.QFrame(self.treeFrame)
        self.frame.setStyleSheet(Styles.Frame.Normal)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.counterlabel = QtWidgets.QLabel(self.frame)
        self.counterlabel.setText("Count : 0")
        self.treeWidget = MyQTreeWidget(self.treeFrame,counterLabel = self.counterlabel)
        self.treeWidget.setColumns(["AreaCode","PhoneNumber","HasInvoice","InvoiceDate",'SubscribtionEnd',"TotalAmount","Time Scraping"])
        self.treeWidget.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.treeWidget.customContextMenuRequested.connect(self.menu)
        self.treeWidget.setStyleSheet(Styles.TreeWidget.Normal)
        self.verticalLayout.addWidget(self.treeWidget)
        self.horizontalLayout.addWidget(self.counterlabel, 0, QtCore.Qt.AlignHCenter)
        self.waitinglabel = QtWidgets.QLabel(self.frame)
        self.waitinglabel.setText("Waiting : 0")
        self.waitinglabel.setStyleSheet("color:white;")
        self.horizontalLayout.addWidget(self.waitinglabel, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout.addWidget(self.frame)
        self.verticalLayout_2.addWidget(self.treeFrame)
        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 1)
        self.verticalLayout_2.setStretch(2, 6)
        self.waitingCount = 0

    def updateWaitingText(self,length:int = None):#wait:bool=False ,
        if length != None:
            self.waitingCount = length
            self.waitinglabel.setText(f"Waiting : {length}")
        # if wait == True :
        #     self.waitingCount -= 1
        #     self.waitinglabel.setText(f"Waiting : {self.waitingCount}")


    def combochanged(self):
        self.label.setText(f"    Current Task\n        {self.comboBox.currentText()} ")

    def menu (self):
        menu = MyCustomContextMenu(
            Actions_arg=[
                "Copy AreaCode", 
                "Copy Number", 
                "Delete Row", 
                "Export To Excel", 
                "Clear Data" ,
            ])
        menu.multiConnect(functions=[
            lambda: self.copy(0) ,
            lambda: self.copy(1) ,
            lambda: self.delete() ,
            lambda : self.export(self.lineEdit.text(),self.ExportRange),
            lambda : self.treeWidget.clear()
        ])
        menu.show()


    def copy(self , index:int):
        try :
            pyperclip.copy(self.treeWidget.currentItem().text(index))
        except :
            self.msg.showWarning(text="No Item Selected please Select one !")

    def delete(self):
        try:
            self.treeWidget.takeTopLevelItem(self.treeWidget.indexOfTopLevelItem(self.treeWidget.currentItem()))
        except:
            self.msg.showWarning(text="No Item Selected please Select one !")

    def export(self,name:typing.Optional[str],values:dict):
        if name == '' or name == ' ':
            name = f"Hour{datetime.now().hour}Minute{datetime.now().minute}"
        if self.treeWidget._ROW_INDEX > 0 :
            self.treeWidget.getCustomDataFrame(values).to_excel(f"Data/Exports/{name}[{datetime.now().date()}].xlsx",index=False)
            self.msg.showInfo(text=f"Exported Succecfully to 'Data/Exports/{name}[{datetime.now().date()}].xlsx'")
        else :
            self.msg.showWarning(text="No Data In App Please Try Again Later")
    
    def setExportRange(self,values:dict):
        self.ExportRange = values



class Page2(QObject):
    msg = MyMessageBox()
    ExportRangeSignal = pyqtSignal(dict)
    def __init__(self, parent:QObject) -> None:
        super().__init__()
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(parent)
        self.settinggroupbox = QtWidgets.QGroupBox(parent)
        self.settinggroupbox.setTitle("Setting")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.settinggroupbox)
        self.frame_11 = QtWidgets.QFrame(self.settinggroupbox)
        self.frame_11.setStyleSheet(Styles.Frame.Normal)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.frame_11)
        self.filedirlabel = QtWidgets.QLabel(self.frame_11)
        self.filedirlabel.setText("File Directory")
        self.horizontalLayout_9.addWidget(self.filedirlabel, 0, QtCore.Qt.AlignHCenter)
        self.lineEditfiledir = QtWidgets.QLineEdit(self.frame_11)
        self.lineEditfiledir.setReadOnly(True)
        self.horizontalLayout_9.addWidget(self.lineEditfiledir)
        self.filedirbtn = QtWidgets.QToolButton(self.frame_11)
        self.filedirbtn.clicked.connect(self.getFileDir)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.filedirbtn.setSizePolicy(sizePolicy)
        self.horizontalLayout_9.addWidget(self.filedirbtn)
        self.horizontalLayout_9.setStretch(0, 1)
        self.horizontalLayout_9.setStretch(1, 4)
        self.horizontalLayout_9.setStretch(2, 1)
        self.verticalLayout_4.addWidget(self.frame_11)
        self.frame_13 = QtWidgets.QFrame(self.settinggroupbox)
        self.frame_13.setStyleSheet(Styles.Frame.Normal)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.frame_13)
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.frame_12 = QtWidgets.QFrame(self.frame_13)
        self.frame_12.setStyleSheet(Styles.Frame.Normal)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.frame_12)
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.sheetnamelabel = QtWidgets.QLabel(self.frame_12)
        self.sheetnamelabel.setText("Sheet Name")
        self.horizontalLayout_10.addWidget(self.sheetnamelabel, 0, QtCore.Qt.AlignHCenter)
        self.lineEdit = QtWidgets.QLineEdit(self.frame_12)
        self.lineEdit.setPlaceholderText("Defualt : Sheet1")
        self.horizontalLayout_10.addWidget(self.lineEdit)
############################
        self.ThreadCountFrame = QtWidgets.QFrame(self.frame_13)
        self.ThreadCountFrame.setStyleSheet(Styles.Frame.Normal)
        self.ThreadCountLabel = QtWidgets.QLabel(self.ThreadCountFrame)
        self.ThreadCountLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ThreadCountLabel.setText("Thread Count ")
        self.ThreadHbox = QtWidgets.QHBoxLayout(self.ThreadCountFrame)
        self.ThreadHbox.setContentsMargins(0, 0, 0, 0)
        self.ThreadHbox.addWidget(self.ThreadCountLabel)#, 0, QtCore.Qt.AlignHCenter
        self.ThreadCountSpinbox = QtWidgets.QSpinBox(self.ThreadCountLabel)
        self.ThreadCountSpinbox.setMinimum(1)
        self.ThreadCountSpinbox.setMaximum(30)
        self.ThreadCountSpinbox.setValue(1)
        self.ThreadCountSpinbox.setStyleSheet(Styles.SpinBox.Normal)
        self.ThreadHbox.addWidget(self.ThreadCountSpinbox)
        self.ThreadHbox.setStretch(0, 3)
        self.ThreadHbox.setStretch(1, 2)
        self.horizontalLayout_11.addWidget(self.ThreadCountFrame)

############################
        self.horizontalLayout_10.setStretch(0, 1)
        self.horizontalLayout_10.setStretch(1, 2)
        self.horizontalLayout_11.addWidget(self.frame_12)
        self.verticalLayout_4.addWidget(self.frame_13)
        self.verticalLayout_5.addWidget(self.settinggroupbox)
        self.exportgroupbox = QtWidgets.QGroupBox(parent)
        self.exportgroupbox.setTitle("Export Options")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.exportgroupbox)
        self.frame_8 = QtWidgets.QFrame(self.exportgroupbox)
        self.frame_8.setStyleSheet(Styles.Frame.Normal)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_8)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame = QtWidgets.QFrame(self.frame_8)
        self.frame.setStyleSheet(Styles.Frame.Normal)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.AreaCodelabel = QtWidgets.QLabel(self.frame)
        self.AreaCodelabel.setText("AreaCode")
        self.horizontalLayout.addWidget(self.AreaCodelabel, 0, QtCore.Qt.AlignHCenter)
        self.AreaCodetoggle = AnimatedToggle(self.frame)
        self.AreaCodetoggle.stateChanged.connect(self.exportrange)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        self.AreaCodetoggle.setSizePolicy(sizePolicy)
        self.horizontalLayout.addWidget(self.AreaCodetoggle)
        self.horizontalLayout.setStretch(0,2)
        self.horizontalLayout.setStretch(1,1)
        self.verticalLayout.addWidget(self.frame)
        self.frame_2 = QtWidgets.QFrame(self.frame_8)
        self.frame_2.setStyleSheet(Styles.Frame.Normal)
        self.ThreadHbox = QtWidgets.QHBoxLayout(self.frame_2)
        self.PhoneNumberlabel = QtWidgets.QLabel(self.frame_2)
        self.PhoneNumberlabel.setText("PhoneNumber")
        self.ThreadHbox.addWidget(self.PhoneNumberlabel, 0, QtCore.Qt.AlignHCenter)
        self.PhoneNumbertoggle = AnimatedToggle(self.frame_2)
        self.PhoneNumbertoggle.stateChanged.connect(self.exportrange)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        self.PhoneNumbertoggle.setSizePolicy(sizePolicy)
        self.ThreadHbox.addWidget(self.PhoneNumbertoggle)
        self.ThreadHbox.setStretch(0,2)
        self.ThreadHbox.setStretch(1,1)
        self.verticalLayout.addWidget(self.frame_2)
        self.frame_3 = QtWidgets.QFrame(self.frame_8)
        self.frame_3.setStyleSheet(Styles.Frame.Normal)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_3)
        self.HasInvoicelabel = QtWidgets.QLabel(self.frame_3)
        self.HasInvoicelabel.setText("HasInvoice")
        self.horizontalLayout_3.addWidget(self.HasInvoicelabel, 0, QtCore.Qt.AlignHCenter)
        self.HasInvoicetoggle = AnimatedToggle(self.frame_3)
        self.HasInvoicetoggle.stateChanged.connect(self.exportrange)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        self.HasInvoicetoggle.setSizePolicy(sizePolicy)
        self.horizontalLayout_3.addWidget(self.HasInvoicetoggle)
        self.horizontalLayout_3.setStretch(0,2)
        self.horizontalLayout_3.setStretch(1,1)
        self.verticalLayout.addWidget(self.frame_3)
        self.horizontalLayout_8.addWidget(self.frame_8)
        self.frame_9 = QtWidgets.QFrame(self.exportgroupbox)
        self.frame_9.setStyleSheet(Styles.Frame.Normal)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_9)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame_7 = QtWidgets.QFrame(self.frame_9)
        self.frame_7.setStyleSheet(Styles.Frame.Normal)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.frame_7)
        self.InvoiceDatelabel = QtWidgets.QLabel(self.frame_7)
        self.InvoiceDatelabel.setText('InvoiceDate')
        self.horizontalLayout_7.addWidget(self.InvoiceDatelabel, 0, QtCore.Qt.AlignHCenter)
        self.InvoiceDatetoggle = AnimatedToggle(self.frame_7)
        self.InvoiceDatetoggle.stateChanged.connect(self.exportrange)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        self.InvoiceDatetoggle.setSizePolicy(sizePolicy)
        self.horizontalLayout_7.addWidget(self.InvoiceDatetoggle)
        self.horizontalLayout_7.setStretch(0,2)
        self.horizontalLayout_7.setStretch(1,1)
        self.verticalLayout_2.addWidget(self.frame_7)
        self.frame_4 = QtWidgets.QFrame(self.frame_9)
        self.frame_4.setStyleSheet(Styles.Frame.Normal)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_4)
        self.SubscribtionEndlabel = QtWidgets.QLabel(self.frame_4)
        self.SubscribtionEndlabel.setText("SubscribtionEnd")
        self.horizontalLayout_4.addWidget(self.SubscribtionEndlabel, 0, QtCore.Qt.AlignHCenter)
        self.SubscribtionEndtoggle = AnimatedToggle(self.frame_4)
        self.SubscribtionEndtoggle.stateChanged.connect(self.exportrange)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        self.SubscribtionEndtoggle.setSizePolicy(sizePolicy)
        self.horizontalLayout_4.addWidget(self.SubscribtionEndtoggle)
        self.horizontalLayout_4.setStretch(0,2)
        self.horizontalLayout_4.setStretch(1,1)
        self.verticalLayout_2.addWidget(self.frame_4)
        self.frame_5 = QtWidgets.QFrame(self.frame_9)
        self.frame_5.setStyleSheet(Styles.Frame.Normal)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.frame_5)
        self.TotalAmountlabel = QtWidgets.QLabel(self.frame_5)
        self.TotalAmountlabel.setText("TotalAmount")
        self.horizontalLayout_5.addWidget(self.TotalAmountlabel, 0, QtCore.Qt.AlignHCenter)
        self.TotalAmounttoggle = AnimatedToggle(self.frame_5)
        self.TotalAmounttoggle.stateChanged.connect(self.exportrange)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        self.TotalAmounttoggle.setSizePolicy(sizePolicy)
        self.horizontalLayout_5.addWidget(self.TotalAmounttoggle)
        self.horizontalLayout_5.setStretch(0,2)
        self.horizontalLayout_5.setStretch(1,1)
        self.verticalLayout_2.addWidget(self.frame_5)
        self.horizontalLayout_8.addWidget(self.frame_9)
        self.frame_10 = QtWidgets.QFrame(self.exportgroupbox)
        self.frame_10.setStyleSheet(Styles.Frame.Normal)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_10)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.frame_6 = QtWidgets.QFrame(self.frame_10)
        self.frame_6.setStyleSheet(Styles.Frame.Normal)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.frame_6)
        self.timescrapelabel = QtWidgets.QLabel(self.frame_6)
        self.timescrapelabel.setText("Time Scraping")
        self.horizontalLayout_6.addWidget(self.timescrapelabel, 0, QtCore.Qt.AlignHCenter)
        self.timescrapetoggle = AnimatedToggle(self.frame_6)
        self.timescrapetoggle.stateChanged.connect(self.exportrange)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        self.timescrapetoggle.setSizePolicy(sizePolicy)
        self.horizontalLayout_6.addWidget(self.timescrapetoggle)
        self.horizontalLayout_6.setStretch(0, 2)
        self.horizontalLayout_6.setStretch(1, 1)
        self.verticalLayout_3.addWidget(self.frame_6)
        self.Mylabel = QtWidgets.QLabel(self.frame_10)
        self.Mylabel.setText("Producer :\nHeshamMoawad")
        self.verticalLayout_3.addWidget(self.Mylabel, 0, QtCore.Qt.AlignHCenter)
        self.horizontalLayout_8.addWidget(self.frame_10)
        self.verticalLayout_5.addWidget(self.exportgroupbox)
        self.verticalLayout_5.setStretch(0, 1)
        self.verticalLayout_5.setStretch(1, 2)
        self.AreaCodetoggle.setChecked(True)
        self.PhoneNumbertoggle.setChecked(True)
        self.HasInvoicetoggle.setChecked(True)
        self.InvoiceDatetoggle.setChecked(True)
        self.SubscribtionEndtoggle.setChecked(True)
        self.TotalAmounttoggle.setChecked(True)
        self.timescrapetoggle.setChecked(True)

        
    def exportrange(self):
        result = {}
        result['AreaCode'] = 0 if self.AreaCodetoggle.isChecked() else None
        result['PhoneNumber'] = 1  if self.PhoneNumbertoggle.isChecked() else None
        result['HasInvoice'] = 2 if self.HasInvoicetoggle .isChecked() else None
        result['InvoiceDate'] = 4  if self.InvoiceDatetoggle.isChecked() else None
        result['SubscribtionEnd'] = 5  if self.SubscribtionEndtoggle.isChecked() else None
        result['TotalAmount'] = 5  if self.TotalAmounttoggle.isChecked() else None
        result['Time Scraping'] = 5  if self.timescrapetoggle.isChecked() else None
        self.ExportRangeSignal.emit(result)

    def getFileDir(self):
        file_filter = 'Data File (*.xlsx *.csv);; Excel File (*.xlsx *.xls)'
        dir = QtWidgets.QFileDialog.getOpenFileName(
            caption='Select a data file',
            filter=file_filter,
            )[0]
        self.lineEditfiledir .clear()
        self.lineEditfiledir.setText(dir)






