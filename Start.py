from MyPyQt5 import QSideMenuEnteredLeaved , MyQMainWindow




class Window (MyQMainWindow):

    def SetupUi(self):
        self.resize(600,600)

        self.Menu = QSideMenuEnteredLeaved(
            self.mainWidget,
            ButtonsCount = 1,
            PagesCount = 1 ,
            ButtonsFixedHight = 50 ,  
        )




        return super().SetupUi()        




if __name__ == "__main__":
    w = Window()

    w.show()





