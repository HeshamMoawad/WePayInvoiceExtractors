from PyQt5.QtCore import  QObject, QThread
from qmodels import (
    QThread ,
    QObject ,
    MyMessageBox ,
    Checking ,
    pyqtSignal ,
    typing
)


class Task(QThread):

    def __init__(self ,parent:'TasksContainer', **kwargs) -> None:
        super().__init__()
        self.setParent(parent)
    
    def parent(self)-> 'TasksContainer' :
        return super().parent()

    def run(self) -> None: ...

    def __str__(self) -> str:
        return f""
        
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
    onSakaniMsg = pyqtSignal(str)

    def __init__(self, parent,**kwargs) -> None:
        super().__init__()
        self.__tasks:typing.Dict[str,typing.List[Task]] = {}
        self.__sakaniInfo = kwargs

    @property
    def tasks(self)->typing.Dict[str,typing.List[Task]]:
        return self.__tasks
    
    def addTask(self , unitcode:str , count:int):
        taskList = []
        for index in range(count):
            task = Task(self,unitcode,index=index,**self.__sakaniInfo)
            taskList.append(task)
            task.start()
        self.__tasks.update(
            {unitcode:taskList}
        )
        self.status.emit("Status : ON ")

    def deleteTask(self,unitcode:str):
        if unitcode in self.__tasks.keys() :
            taskslist = self.__tasks[unitcode]
            for task in taskslist:
                task.delete()
            del self.__tasks[unitcode]
        self.status.emit("Status : OFF ") if not self.isRunning() else None
    
    def deleteAll(self):
        for unit in self.__tasks.keys():
            self.deleteTask(unit)
        self.status.emit("Status : OFF ")

    def isRunning(self):
        return True if len(self.__tasks) > 0 else False
