<<<<<<< HEAD
import pandas as pd 
# from tasks import QThread   
class Excel ():
    
    def Load_Exel(self):
        data = pd.read_excel("Book1.xlsx")
        data=data["Faill Num"]
        data=(list(data))
        print(data)
        return data
              
    def ExcelRead(self,code, Num):
        Data = Excel.Load_Exel()
      
        resultdata = list(Data)
        if len(str(code)) == 1:
                code = "0" + str(code)
                resultdata.append(str(code) + str(Num))
        elif len(str(code)) == 2:
                resultdata.append(str(code) + str(Num))
        else :
                resultdata    

        Data = pd.DataFrame({"code": code ,"Num":Num ,"Faill num": resultdata})
        Data.to_excel("data.xlsx", index=False)
 

 
 

 
 
 
  
########################################################################################      
# class Excel ()  : 
#     def ExcelRead(code, Num):
#         result = []
#         if len(str(code)) == 1:
#             code = "0" + str(code)
#             result.append(str(str(code) + str(Num)))
#             print(result)
#             return result
#         elif len(str(code)) == 2 :
#             result.append(str(code + str(Num)))
#             print(result)
#             return result    
#         else :
#             return result
    
#     resultdata = ExcelRead('4', 114655556)
    
#     data = pd.DataFrame({"Num": resultdata})
#     data.to_excel("data.xlsx", index=False)


       

 
    





=======
################### Abdallah 

#
>>>>>>> fdb23fa6ade844cdcc63d1910ddacc84c561a197
