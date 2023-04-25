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

    def __init__(self) -> None:
        super().__init__()
        
        

    def convertDataframeToPhonesList(self,df:pandas.DataFrame)->list:
        response = []
        for row in range(0,len(df)):
            res = (f"{df.iloc[row][0]}",f"{df.iloc[row][1]}")
            if f"{df.iloc[row]}" != 'None' :
                response.append(res)
        return response


