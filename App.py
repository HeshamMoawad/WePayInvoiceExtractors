from pages import Page1,Page2
import pandas , openpyxl , time , numpy
from mainclass import WePay
import os 
from styles import Styles
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

####################################################

# MIT License

# Copyright (c) 2023 HeshamMoawad

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Contact Me 
# GitHub : github.com/HeshamMoawad
# Gmail : HeshamMoawad120120@gmail.com
# Whatsapp : +201111141853

####################################################


class Window(MyQMainWindow):
    Threads = []

    def __init__(self,name:str) -> None:
        self.Name = name
        super().__init__()

    def SetupUi(self):
        self.ThreadsCount = 0
        self.dataframe = pandas.DataFrame()
        self.dataframeList = []
        self.resize(650,500)
        font = QFont()
        font.setPointSize(12)
        self.setFont(font)
        self.setStyleSheet(Styles().main)
        self.setFrameLess()
        self.Menu = QSideMenuEnteredLeaved(
            Title = f"Welcome {self.Name if self.Name != 'K7Hesham' else 'Admin'}" ,
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
        # self.mainWidget.setStyleSheet(Styles().main)
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


        # self.Menu.MainLabel.setText("hhhhhhhh")

        ################### ShortCut ##########################
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
            print(f"Main DF -> {self.dataframe}\n\nDF List -> {self.dataframeList}")
            self.DashBoard.comboBox.clear()
            lambda: self.updateWaitingDF({},clear=True)



    def prepareDF(self,count:int):
        fileDir = self.Setting.lineEditfiledir.text()
        sheetname = 'Sheet1' if self.Setting.lineEdit.text() == '' else self.Setting.lineEdit.text() 

        if fileDir != "":
            if os.path.isfile(fileDir):
                self.dataframeList = self.splitDataFrame(
                        df = self.getExcelData( excelfile = fileDir, sheetname = sheetname) ,
                        nArray = count ,
                            )
                self.dataframe = pandas.concat(self.dataframeList)
                return True
            elif not os.path.isfile(fileDir):
                self.msg.showInfo('No Such File Or Directory')
                return False
        else:
            if len(self.dataframe) >= 1 :
                return True
            else:
                self.msg.showInfo("No Data In Waiting")
                return False




    def runThreads(self,count:int):
        if self.prepareDF(count):
            self.DashBoard.updateWaitingText(length = len(self.dataframe))
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
            self.dataframe = pandas.concat(self.dataframeList)
            self.DashBoard.updateWaitingText(length = len(self.dataframe))
        if clear == True :
            self.dataframe = pandas.DataFrame()
            self.DashBoard.updateWaitingText(length = 0)
            self.dataframeList.clear()


    def getExcelData(self,excelfile,sheetname)->pandas.DataFrame:
        wb = openpyxl.load_workbook(excelfile)
        ws = wb[sheetname]
        df = pandas.DataFrame(ws.values)
        df.dropna(inplace=True)
        df[df.columns[0]].apply(int)
        df[df.columns[1]].apply(int)
        df[df.columns[0]].apply(str)
        df[df.columns[1]].apply(str)
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
        try:
            self.WePay = WePay()
            self.WePay.Lead.connect(self.Lead.emit)
            self.WePay.msg.connect(self.msg.emit)
            listOfPhones = self.splitPhones(
                List = self.WePay.convertDataframeToPhonesList(self.df)
            )
            self.errorNumbers = []
            for lista in listOfPhones :
                self.scrape(lista)
            errlength = len(self.errorNumbers)
            print(self.errorNumbers)
            if errlength == 0 :
                pass
            elif errlength <= 70 :
                self.scrape(self.errorNumbers)
            elif errlength > 70 :
                listOfPhones = self.splitPhones(self.errorNumbers)
                for List in listOfPhones:
                    self.scrape(List)
        except Exception as e :
            self.msg.emit(f"Error in Task{self.index} : {e}\nPlease Contact Hesham")
        self.finishedSignal.emit()


    def splitPhones(self,List):
        myrange = List[::70]
        return numpy.array_split(List,len(myrange))


    def scrape(self,List):
        self.WePay.start()
        for AreaCode , PhoneNumber in List :
            try:
                print(AreaCode,PhoneNumber)
                self.statues.emit(f"Searching for +2{AreaCode}{PhoneNumber}")
                self.WePay.ScrapePhone(areacode = AreaCode , phone = PhoneNumber)
                self.df = self.df[1:]
                self.DataFrame.emit({'index':self.index , "dataframe":self.df})
            except Exception as e :
                self.errorNumbers.append((AreaCode,PhoneNumber))
                self.errors.append(e)
        self.WePay.exit()


    def kill(self, msg: str = None):
        try:
            self.WePay.exit()
        except Exception as e :
            pass
        return super().kill(msg)
