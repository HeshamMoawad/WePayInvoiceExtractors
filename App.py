from pages import Page1,Page2
import pandas , openpyxl , time , numpy
from mainclass import WePay
from MyPyQt5 import (
    pyqtSignal ,
    MyQMainWindow ,
    MyThread ,
    QSideMenuEnteredLeaved , 
    QIcon ,
    QSize ,
    QFont ,
    QKeySequence ,
    QShortcut
)



class Window(MyQMainWindow):
    Threads = []

    def SetupUi(self):
        self.ThreadsCount = 0
        self.dataframe = pandas.DataFrame()
        self.dataframeList = []
        self.resize(650,500)
        font = QFont()
        font.setPointSize(12)
        self.setFont(font)
        self.Menu = QSideMenuEnteredLeaved(
            parent = self.mainWidget ,
            ButtonsCount = 2 ,
            PagesCount = 2 ,
            ToggleCount = 0 ,
            ButtonsFixedHight = 50 ,
            ButtonsFrameFixedwidthMini = 50 , 
            ButtonsFrameFixedwidth = 120 ,
            ExitButtonIconPath = "Data\Icons\\reject.png" ,
            MaxButtonIconPath = "Data\Icons\maximize.png",
            Mini_MaxButtonIconPath = "Data\Icons\minimize.png",
            MiniButtonIconPath = "Data\Icons\delete.png",

        )
        self.DashBoardBtn = self.Menu.getButton(0)
        self.DashBoardBtn.setTexts(entred=' DashBoard',leaved='')
        self.DashBoardBtn.setIcon(QIcon('Data\Icons\dashboard.png'))
        self.DashBoardBtn.setIconSize(QSize(30,30))
        self.SettingBtn = self.Menu.getButton(1)
        self.SettingBtn.setIcon(QIcon('Data\Icons\setting.png'))
        self.SettingBtn.setIconSize(QSize(30,30))
        self.SettingBtn.setTexts(entred=' Setting',leaved='')
        font.setPointSize(10)
        self.SettingBtn.setFont(font)
        self.DashBoardBtn.setFont(font)
        self.DashBoard = Page1(self.Menu.getPage(0))
        self.Setting = Page2(self.Menu.getPage(1))
        self.Setting.ExportRangeSignal.connect(self.DashBoard.setExportRange)
        self.Menu.connect_Button_Page(btn = self.DashBoardBtn ,pageIndex = 0)
        self.Menu.connect_Button_Page(btn = self.SettingBtn ,pageIndex = 1)
        self.clear = QShortcut(QKeySequence("ctrl+r"),self)
        self.clear.activated.connect(lambda: self.updateWaitingDF({},clear=True))
        ################### Thread Part ##########################
        self.DashBoard.startbtn.clicked.connect(lambda : self.runThreads(self.Setting.ThreadCountSpinbox.value())) #######
        self.DashBoard.stopbtn.clicked.connect(self.killThread)
        return super().SetupUi()


    def finishedThread(self):
        self.finishedThreads = [thread for thread in self.Threads if not thread.isRunning()]
        if len(self.finishedThreads) == len(self.Threads):
            self.Menu.MainLabel.setText("Ended Succecfully")
            self.msg.showInfo("End Scrape Good Luck Next Time -_*")
            self.DashBoard.comboBox.clear()

    def runThreads(self,count):
        fileDir = self.Setting.lineEditfiledir.text()
        sheetname = 'Sheet1' if self.Setting.lineEdit.text() == '' else self.Setting.lineEdit.text() 
        self.dataframeList = self.splitDataFrame(
                df = self.getExcelData( excelfile = fileDir, sheetname = sheetname) ,
                nArray = count ,
                )
        self.DashBoard.updateWaiting(length = len(pandas.concat(self.dataframeList)))
        for index in range(count):
            self.ThreadsCount = count
            currentvalues = [self.DashBoard.comboBox.itemText(i) for i in range(self.DashBoard.comboBox.count())]
            valuescount = self.DashBoard.comboBox.count()
            self.DashBoard.comboBox.clear()
            self.DashBoard.comboBox.addItems( currentvalues +[f"Task{ valuescount+ 1}"])
            Thread = WorkingThread()
            Thread.index = index
            Thread.setData(self.logicDirMethod(count,index))
            Thread.setMainClass(self)
            Thread.msg.connect(self.msg.showInfo)
            Thread.statues.connect(self.Menu.MainLabel.setText)
            Thread.Lead.connect(self.appendData)
            Thread.finishedSignal.connect(self.finishedThread)
            Thread.DataFrame.connect(self.updateWaitingDF)
            Thread.start(Thread.Priority.InheritPriority)
            self.Threads.append(Thread)

    def killThread(self):
        for thread in self.Threads :
            thread.kill()
        self.Menu.MainLabel.setText("Stopped Succecfully")
        self.msg.showInfo("Stop Scrape Good Luck Next Time -_*")
        self.DashBoard.comboBox.clear()

    def appendData(self,lead):
        if lead[2] == 'True':
            lead[2] = 'يوجد فاتورة'
        elif lead[2] == 'False':
            lead[2] = 'لايوجد فواتير'
        elif lead[2] == 'NoAccount':
            lead[2] = 'لايوجد حساب لهذا العميل'
        self.DashBoard.treeWidget.appendDataAsList(lead)

    def updateWaitingDF(self,signal:dict ,clear:bool=False):
        if clear == False :
            self.dataframeList[signal['index']] = signal["dataframe"]
            self.DashBoard.updateWaiting(length = len(pandas.concat(self.dataframeList)))
        if clear == True :
            self.dataframe = pandas.DataFrame()
            self.DashBoard.updateWaiting(length = 0)
            self.dataframeList = []

    def getExcelData(self,excelfile,sheetname)->pandas.DataFrame:
        wb = openpyxl.load_workbook(excelfile)
        ws = wb[sheetname]
        df = pandas.DataFrame(ws.values)
        df.dropna(inplace=True)
        df = df[1:]
        return df

    def splitDataFrame(self,df:pandas.DataFrame,nArray):
        result = []
        val = int(round(len(df)/nArray,ndigits=0))
        endslice = val
        startslice = 0
        for i in range(nArray) :
            if i == nArray-1 :
                result.append(df[startslice:])
            else:
                result.append(df[startslice:endslice])
            startslice += val
            endslice += val
        return result

    def logicDirMethod(self,count:int,index:int):
        if self.Setting.lineEditfiledir.text() !=  "" :
            dataframe = self.dataframeList[index]
            return dataframe
        elif self.Setting.lineEditfiledir.text() ==  "" :
            if len(self.dataframe) <= 1:
                self.msg.showCritical(f'No Data In Waiting')
                return pandas.DataFrame()
            else :
                df = pandas.concat(self.dataframeList)
                return self.splitDataFrame(df,count)[index]
        self.Setting.lineEditfiledir.clear()



class WorkingThread(MyThread):
    Lead = pyqtSignal(list)
    DataFrame = pyqtSignal(dict)
    finishedSignal = pyqtSignal()
    errors = []
    index = 0

    def setMainClass(self,mainclass:Window):
        self.MainClass = mainclass

    def setData(self,df:pandas.DataFrame):
        self.df = df

    def run(self) -> None:
        self.statues.emit("Starting")
        # try:
        self.WePay = WePay()
        self.WePay.Lead.connect(self.Lead.emit)
        self.WePay.msg.connect(self.msg.emit)
        phonelist = self.WePay.convertDataframeToPhonesList(self.df)
        myrange = phonelist[::70]
        listOfPhones = numpy.array_split(phonelist,len(myrange))
        for lista in listOfPhones :
            self.WePay.start()
            for AreaCode , PhoneNumber in lista :
                try:
                    print(AreaCode,PhoneNumber)
                    self.statues.emit(f"Searching for +2{AreaCode}{PhoneNumber}")
                    self.WePay.ScrapePhone(areacode = AreaCode , phone = PhoneNumber)
                    self.df = self.df[1:]
                    self.DataFrame.emit({'index':self.index , "dataframe":self.df})
                except Exception as e :
                    self.msg.emit(f"Error in Task{self.index} : {e}\nPlease Contact Hesham")
                    self.errors.append(e)
            self.WePay.exit()
        # except Exception as e :
        #     self.msg.emit(f"Error in Task{self.index} : {e}\nPlease Contact Hesham")
        self.finishedSignal.emit()


    def kill(self, msg: str = None):
        try:
            self.WePay.exit()
        except Exception as e :
            pass
        return super().kill(msg)




w = Window()
w.show()
