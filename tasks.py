from PyQt5.QtCore import  QObject, QThread
from qmodels import (
    QThread ,
    QObject ,
    Checking ,
    pyqtSignal ,
    typing ,
    SharingDataFrame
)
from WePay import Customer , NotCustomer , BaseWePay


def row(self,row)->dict:
    return {
        'AreaCode' : row[0],
        'PhoneNumber' : row[1]
    }


class Task(QThread):
    onCatchCustomer = pyqtSignal(Customer)
    onCatchNotCustomer = pyqtSignal(NotCustomer)
    
    def __init__(self ,parent:'TasksContainer',sharingdata:SharingDataFrame, **kwargs) -> None:
        super().__init__()
        self.setParent(parent)
        self.sharingdata = sharingdata
        self.wepay = BaseWePay()
        self.checker = Checking()
        self.__stop = False 
    
    def parent(self)-> 'TasksContainer' :
        return super().parent()

    def run(self) -> None: 
        while not self.__stop :
            try :
                while not self.sharingdata.empty :
                    resault = self.wepay.getAccount(**row(self.sharingdata.get_row()))
                    if isinstance(resault,Customer):
                        self.onCatchCustomer.emit(resault)
                    elif isinstance(resault,NotCustomer):
                        self.onCatchNotCustomer.emit(resault)
                    else :
                        print(resault)
            except ConnectionError as ce :
                print(ce)
                if not self.checker.isConnect() :
                    self.__stop = True
            except Exception as e :
                print(e)
                self.__stop = True


    def __str__(self) -> str:
        return f"WePayWorker(isRunning : {self.isRunning()})"
        
    def start(self) -> None:
        if not self.isRunning():
            return super().start(self.Priority.HighPriority)
    
    def stop(self):
        if self.isRunning(self):
            self.terminate()
            self.wait()

    def delete(self):
        self.stop()
        self.deleteLater()

        
class TasksContainer(QObject):
    status = pyqtSignal(str)
    msg = pyqtSignal(str)
    onCatchCustomer = pyqtSignal(Customer)
    onCatchNotCustomer = pyqtSignal(NotCustomer)


    def __init__(self,sharingdata:SharingDataFrame,**kwargs) -> None:
        super().__init__()
        self.__tasks:typing.List[Task]= []
        self.sharingdata = sharingdata

    @property
    def tasks(self)->typing.List[Task]:
        return self.__tasks
    
    def start(self,max:int):
        if self.sharingdata.rowCount() < max :
            max = self.sharingdata.rowCount()
        for _ in range(max):
            print(f"Running {_}")
            task = Task(self , self.sharingdata)
            task.onCatchCustomer.connect(self.onCatchCustomer.emit)
            task.onCatchNotCustomer.connect(self.onCatchNotCustomer.emit)
            self.__tasks.append(task)
            task.start()
        self.status.emit("Status : ON ")
    
    def stop(self):
        for task in self.__tasks :
            task.delete()
            self.__tasks.remove(task)            
        self.status.emit("Status : OFF ")

    def isRunning(self):
        return True if len(self.__tasks) > 0 else False
