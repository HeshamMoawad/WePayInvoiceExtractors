from selenium.webdriver import Chrome
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import  NoSuchElementException
#import random
import typing , time , sqlite3 , datetime #, os
import pandas as pd
import openpyxl
from MyPyQt5 import QObject , pyqtSignal



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
                #QThread.msleep(100)
                #time.sleep(0.1)
                pass
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
                #QThread.msleep(100)
                #time.sleep(0.1)
                
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
        return self.jscode("return Account.Customer;")

    def getAccountInfo(self) -> dict :
        return self.jscode("return Account;")

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
        df = pd.DataFrame(ws.values)
        response = []
        for row in df.index:
            res = (f"{df.iloc[row][0]}",f"{df.iloc[row][1]}")
            #print(res)
            response.append(res)
        return response[1:]










##############################################################################################

class WePay(QObject):
    Lead = pyqtSignal(list)

    BACKTOMAINSCREEN = """document.querySelector("a[id='InquiryForAnotherAccount']").click()"""

    def __init__(self) -> None:
        super().__init__()
        option = Options()
        #option.headless = True if  headless == True else False
        option.add_experimental_option("excludeSwitches", ["enable-logging"])
        option.add_argument('--disable-logging')
        #option.add_argument('--force-dark-mode') if darkMode == True else None
        #option.add_argument(f"user-data-dir={os.getcwd()}\\Profiles\\{userProfile}")
        self.driver = Chrome(ChromeDriverManager().install(),options=option)
        #self.js = JavaScriptCodeHandler(self.driver)
        self.driver.maximize_window()
        self.driver.get("https://billing.te.eg/ar-EG")
        # self.leadCount = 0
        self.jscode = JavaScriptCodeHandler(self.driver)
        self.SearchButton = self.jscode.WaitingElement(timeout=10,val="//button[@data-role='Inquiry']")
        self.AreaCode = self.jscode.WaitingElement(timeout = 10,val = "//input[@id='TxtAreaCode']")
        self.PhoneNumber = self.jscode.WaitingElement(timeout= 10 ,val = "//input[@id='TxtPhoneNumber']",)
        #self.BackButton = self.jscode.WaitingElement(timeout = 20,val="//a[@id='InquiryForAnotherAccount']")
        self.Data = DataBaseConnection()
        print("\n Opened Browser Succecfully  \n")
        

    def writeAreaCode(self,code:str)-> None:
        try:
            self.AreaCode.clear()
            self.AreaCode.send_keys(code)
        except Exception as e :
            #print(f"\n{e}\n")
            self.AreaCode = self.jscode.WaitingElement(
                timeout = 3,
                val = "//input[@id='TxtAreaCode']",
            )
            self.AreaCode.clear()
            self.AreaCode.send_keys(code)


    def writePhoneNumber(self,phone:str)->None:
        try:
            self.PhoneNumber.clear()
            self.PhoneNumber.send_keys(phone)
        except Exception as e :
            #print(f"\n{e}\n")
            self.PhoneNumber = self.jscode.WaitingElement(
                timeout= 3 ,
                val = "//input[@id='TxtPhoneNumber']",
            )
            self.PhoneNumber.clear()
            self.PhoneNumber.send_keys(phone)


    def clickSearchButton(self)->None:
        try:
            self.SearchButton.click()
        except Exception as e :
            #print(f"\n{e}\n")
            self.SearchButton = self.jscode.WaitingElement(timeout=5,val="//button[@data-role='Inquiry']")
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
            return False


    def filterCustomerData(self,Account:dict,Customer:dict)-> dict:
        CustomerResult = {}
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
            self.writeAreaCode(areacode)
            self.writePhoneNumber(phone)
            self.clickSearchButton()
            if self.checkExistAccount():
                Customer = self.filterCustomerData(
                    Account = self.jscode.getAccountInfo() ,
                    Customer = self.jscode.getCustomerInfo() ,
                    )
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
    def exit(self):
        self.driver.close()




