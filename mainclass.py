from selenium.webdriver import Chrome
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import  NoSuchElementException
import typing , time , sqlite3 , datetime
import pandas 
import openpyxl
from MyPyQt5 import QObject , pyqtSignal

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


class JavaScriptCodeHandler(object):

    def __init__(self,driver:WebDriver) -> None:
        self.driver = driver
    
    def jscode(self,command):
        return self.driver.execute_script(command)

    def WaitingElement(self,timeout:int,val:str,by:str=By.XPATH)->typing.Optional[WebElement]:
        end_time = time.time() + timeout
        while True:
            if time.time() > end_time :
                print("TimedOut and Breaked")
                break
            try:
                Result = self.driver.find_element(by,val)
                break
            except NoSuchElementException :
                Result = None
        return Result
    
    def WaitingElements(self,timeout:int,val:str,by:str=By.XPATH)->typing.Optional[typing.List[WebElement]]:
        end_time = time.time() + timeout
        while True:
            if time.time() > end_time :
                print("TimedOut and Breaked")
                break
            try:
                Result = self.driver.find_elements(by,val)
                break
            except NoSuchElementException :
                Result = []                
        return Result
            
    def WaitingMethod(self,timeout:int,func):
        end_time = time.time() + timeout
        while True:
            if time.time() > end_time :
                print("TimedOut and Breaked")
                break
            try:
                Result = func()
            except Exception as e :
                pass
        return Result


    def getCustomerInfo(self) -> dict :
        try:
            return self.jscode("return Account.Customer;")
        except Exception as e :
            return False
         

    def getAccountInfo(self) -> dict :
        try:
            return self.jscode("return Account;")
        except Exception as e :
            return False

    def getInvoiceInfo(self) -> list :
        return self.jscode("return Account.Invoices;")
            

    
###########





#########################################################################################

class DataBaseConnection(object):
    def __init__(self) -> None:
        self.con = sqlite3.connect("Data\Database.db")
        self.cur = self.con.cursor()

#--------------------------------------------------------------------

    def exist(self,table,value:dict) ->bool :
        self.cur.execute(f"""SELECT * FROM {table} WHERE {value.keys()[0]} = '{value.values()[0]}'; """)
        return True if self.cur.fetchall() != [] else False
    
    def existCustomer(self,account:str) ->bool:
        self.cur.execute(f"""SELECT * FROM Customers WHERE Account = '{account}'; """)
        return True if self.cur.fetchall() != [] else False
    
    def existInvoiceByAccount(self,account:str) ->bool:
        self.cur.execute(f"""SELECT * FROM Invoices WHERE Account = '{account}'; """)
        return True if self.cur.fetchall() != [] else False
    
    def existInvoiceByID(self,id:str) ->bool:
        self.cur.execute(f"""SELECT * FROM Invoices WHERE ID = '{id}'; """)
        return True if self.cur.fetchall() != [] else False

#--------------------------------------------------------------------

    def addCustomer(self,**kwargs):
        try:
            self.cur.execute(f"""
            INSERT INTO Customers {str(tuple(kwargs.keys())).replace("'","")}
            VALUES {tuple(kwargs.values())}; 
            """)
            self.con.commit()
        except Exception as e:
            print(f"\n{e} \nError in addCustomer \n")

    def addInvoice(self,**kwargs):
        try:
            self.cur.execute(f"""
            INSERT INTO Invoices {str(tuple(kwargs.keys())).replace("'","")}
            VALUES {tuple(kwargs.values())}; 
            """)
            self.con.commit()
        except Exception as e:
            print(f"\n{e} \nError in addInvoice \n")
    
#--------------------------------------------------------------------


    def updateCustomer(self,account:str,**kwargs):
        try:
            self.cur.execute(f""" UPDATE Customers SET {"".join([f" {key}= '{value}'," for key,value in kwargs.items()])[:-1]} WHERE Account = '{account}' ;""")
            self.con.commit()
        except Exception as e:
            print(f"\n{e} \nError in updateCustomer \n")

        
    def reshapeExelData(self,excelfile,sheetname):
        wb = openpyxl.load_workbook(excelfile)
        ws = wb[sheetname]
        df = pandas.DataFrame(ws.values)
        response = []
        for row in df.index:
            res = (f"{df.iloc[row][0]}",f"{df.iloc[row][1]}")
            response.append(res)
        return response[1:]




##############################################################################################

class WePay(QObject):
    Lead = pyqtSignal(list)
    msg = pyqtSignal(str)
    stop = pyqtSignal(bool)

    BACKTOMAINSCREEN = """document.querySelector("a[id='InquiryForAnotherAccount']").click()"""

    def __init__(self) -> None:
        super().__init__()
    
    def start(self):
        option = Options()
        option.add_experimental_option("excludeSwitches", ["enable-logging"])
        option.add_argument('--disable-logging')
        self.driver = Chrome(ChromeDriverManager().install(),options=option)
        self.driver.maximize_window()
        self.driver.get("https://billing.te.eg/ar-EG")
        self.jscode = JavaScriptCodeHandler(self.driver)
        self.SearchButton = self.jscode.WaitingElement(timeout=10,val="//button[@data-role='Inquiry']")
        self.AreaCode = self.jscode.WaitingElement(timeout = 10,val = "//input[@id='TxtAreaCode']")
        self.PhoneNumber = self.jscode.WaitingElement(timeout= 10 ,val = "//input[@id='TxtPhoneNumber']",)
        self.Data = DataBaseConnection()
        print("\n Opened Browser Succecfully  \n")
        self.driver.minimize_window()
        

    def writeAreaCode(self,code:str,phonenumber:str)-> None:
        try:
            self.AreaCode.clear()
            self.AreaCode.send_keys(code)
        except Exception as e :
            # self.driver.refresh()
            self.AreaCode = self.jscode.WaitingElement(
                timeout = 2,
                val = "//input[@id='TxtAreaCode']",
            )
            self.writePhoneNumber(phone=phonenumber,code=code)
            self.AreaCode.clear()
            self.AreaCode.send_keys(code)


    def writePhoneNumber(self,phone:str,code:str)->None:
        try:
            self.PhoneNumber.clear()
            self.PhoneNumber.send_keys(phone)
        except Exception as e :
            # self.driver.refresh()
            self.PhoneNumber = self.jscode.WaitingElement(
                timeout= 2 ,
                val = "//input[@id='TxtPhoneNumber']",
            )
            # self.writeAreaCode(code,phone)
            self.PhoneNumber.clear()
            self.PhoneNumber.send_keys(phone)


    def clickSearchButton(self)->None:
        try:
            self.SearchButton.click()
        except Exception as e :
            self.SearchButton = self.jscode.WaitingElement(timeout=1,val="//button[@data-role='Inquiry']")
            self.SearchButton.click()
    
    def backToInquiry(self):
        self.jscode.jscode("""document.querySelector("div[data-role='BackToInquiryIco']").click();""")


    def checkExistAccount(self)->bool:
        try:
            AccountInfo = self.jscode.WaitingElement(
                timeout = 5 ,
                val = "//div[@data-role='CustomerInfo']")
            return True
        except Exception as e :
            okbtn = self.jscode.WaitingElement(
                timeout = 1 ,
                val= '//button[@class="swal2-confirm swal2-styled"]',
            )
            okbtn.click()
            print(f"\nClicked OK\n")
            return False


    def filterCustomerData(self,Account:dict,Customer:dict)-> dict:
        CustomerResult = {}
        if Customer != False :
            CustomerResult["Account"] = Customer['Account']
            CustomerResult['AreaCode'] = Customer['AreaCode']
            CustomerResult['PhoneNumber'] = Customer['PhoneNumber']
            CustomerResult['AssociatedTelephonesFormatted'] = Customer['AssociatedTelephonesFormatted']
            CustomerResult['HasPreviousUnPaidInvoice'] = Account['HasPreviousUnPaidInvoice']
            CustomerResult['InvoicesCount'] = len(Account["Invoices"])
            CustomerResult['DepositValue'] = Customer['DepositValue']
            CustomerResult['IsBusiness'] = Customer['IsBusiness']
            CustomerResult['DateScraping'] = f"{datetime.datetime.now().date()} | {datetime.datetime.now().hour}:{datetime.datetime.now().minute}"
            return CustomerResult
        else :
            return False


    def filterInvoiceData(self,Invoice:dict)-> dict:
        InvoiceResult = {}
        InvoiceResult['ID'] = Invoice['ID']
        InvoiceResult['Account'] = Invoice['AccountNo']
        InvoiceResult['PhoneNumber'] = Invoice['PhoneNumber']
        InvoiceResult['StartDay'] = Invoice['ConsumptionStart']["Day"]
        InvoiceResult['StartMonth'] = Invoice['ConsumptionStart']["Month"]
        InvoiceResult['StartYear'] = Invoice['ConsumptionStart']["Year"]
        InvoiceResult['EndDay'] = Invoice['ConsumptionEnd']["Day"]
        InvoiceResult['EndMonth'] = Invoice['ConsumptionEnd']["Month"]
        InvoiceResult['EndYear'] = Invoice['ConsumptionEnd']["Year"]
        InvoiceResult['TimeOfInvoice'] = int(Invoice['ConsumptionEnd']["Month"]-Invoice['ConsumptionStart']["Month"])+1
        InvoiceResult['BillDateClient'] = f"{Invoice['BillDateClient']['Day']}-{Invoice['BillDateClient']['Month']}-{Invoice['BillDateClient']['Year']}"
        InvoiceResult['TotalAmount'] = Invoice['TotalAmount']
        InvoiceResult['SubscribtionEnd'] = f"{Invoice['SubscribtionEnd']['Day']}-{Invoice['SubscribtionEnd']['Month']}-{Invoice['SubscribtionEnd']['Year']}"
        return InvoiceResult

    def ScrapePhonesList(self,phoneslist:list):
        for areacode , phone in phoneslist :
            Leadform = []
            print(phone,areacode)
            if len(areacode) == 1:
                areacode = f"0{areacode}" 
            try:
                self.writeAreaCode(areacode,phone)
                self.writePhoneNumber(phone,areacode)
                self.clickSearchButton()
            except Exception as e :
                self.driver.refresh()
                self.writeAreaCode(areacode,phone)
                self.writePhoneNumber(phone,areacode)
                self.clickSearchButton()

            if self.checkExistAccount():
                Customer = self.filterCustomerData(
                    Account = self.jscode.getAccountInfo() ,
                    Customer = self.jscode.getCustomerInfo() ,
                    )
                if Customer != False :

                    if  phone in Customer['AssociatedTelephonesFormatted'] :
                        Leadform.append(areacode)
                        Leadform.append(phone)                    
                        if not self.Data.existCustomer(Customer['Account']):
                            try:
                                self.Data.addCustomer(**Customer)
                            except Exception as e :
                                pass
                        else :
                            try:
                                self.Data.updateCustomer(Customer['Account'],**Customer)
                            except Exception as e :
                                pass
                        InvoicesList = self.jscode.getInvoiceInfo()
                        for Invoice in InvoicesList:
                            Invoice = self.filterInvoiceData(Invoice)
                            if not self.Data.existInvoiceByID(Invoice['ID']):
                                try:
                                    self.Data.addInvoice(**Invoice)
                                except Exception as e :
                                    pass
                            else:
                                pass
                        if  Customer['HasPreviousUnPaidInvoice'] :
                            Leadform.append(str(Customer['HasPreviousUnPaidInvoice']))
                            Leadform.append(str(Invoice['BillDateClient']))
                            Leadform.append(str(Invoice['SubscribtionEnd']))
                            Leadform.append(str(Invoice['TotalAmount']))
                        else : 
                            Leadform = [areacode,phone,str(Customer['HasPreviousUnPaidInvoice']),"","",""]
                        self.Lead.emit(Leadform)
                else:
                    self.Lead.emit([areacode,phone,"NoAccount","NoAccount","NoAccount","NoAccount"])
                self.backToInquiry()
            else :
                self.Lead.emit([areacode,phone,"NoAccount","NoAccount","NoAccount","NoAccount"])
    
    def ScrapePhone(self,areacode:str,phone:str):
        Leadform = []
        # print(phone,areacode)
        t1 = time.time()
        if len(areacode) == 1:
            areacode = f"0{areacode}" 
        try:
            self.writeAreaCode(areacode,phone)
            self.writePhoneNumber(phone,areacode)
            self.clickSearchButton()
        except Exception as e :
            self.driver.refresh()
            self.writeAreaCode(areacode,phone)
            self.writePhoneNumber(phone,areacode)
            self.clickSearchButton()

        if self.checkExistAccount():
            Customer = self.filterCustomerData(
                Account = self.jscode.getAccountInfo() ,
                Customer = self.jscode.getCustomerInfo() ,
                )
            if Customer != False :

                if  phone in Customer['AssociatedTelephonesFormatted'] :
                    Leadform.append(areacode)
                    Leadform.append(phone)                    
                    if not self.Data.existCustomer(Customer['Account']):
                        try:
                            self.Data.addCustomer(**Customer)
                        except Exception as e :
                            pass
                    else :
                        try:
                            self.Data.updateCustomer(Customer['Account'],**Customer)
                        except Exception as e :
                            pass
                    InvoicesList = self.jscode.getInvoiceInfo()
                    for Invoice in InvoicesList:
                        Invoice = self.filterInvoiceData(Invoice)
                        if not self.Data.existInvoiceByID(Invoice['ID']):
                            try:
                                self.Data.addInvoice(**Invoice)
                            except Exception as e :
                                pass
                        else:
                            pass
                    if  Customer['HasPreviousUnPaidInvoice'] :
                        Leadform.append(str(Customer['HasPreviousUnPaidInvoice']))
                        Leadform.append(str(Invoice['BillDateClient']))
                        Leadform.append(str(Invoice['SubscribtionEnd']))
                        Leadform.append(str(Invoice['TotalAmount']))
                    else : 
                        Leadform = [areacode,phone,str(Customer['HasPreviousUnPaidInvoice']),"","",""]
                    t2 = time.time()
                    Leadform.append(f"{round(t2-t1,ndigits=2)}") ###############
                    self.Lead.emit(Leadform)
            else:
                t2 = time.time()
                self.Lead.emit([areacode,phone,"NoAccount","NoAccount","NoAccount","NoAccount",f"{round(t2-t1,ndigits=2)}"])
            self.backToInquiry()
        else :
            t2 = time.time()
            self.Lead.emit([areacode,phone,"NoAccount","NoAccount","NoAccount","NoAccount",f"{round(t2-t1,ndigits=2)}"])
    def exit(self):
        self.driver.close()


    def convertDataframeToPhonesList(self,df:pandas.DataFrame)->list:
        response = []
        for row in range(0,len(df)):
            res = (f"{df.iloc[row][0]}",f"{df.iloc[row][1]}")
            if f"{df.iloc[row]}" != 'None' :
                response.append(res)
        return response


