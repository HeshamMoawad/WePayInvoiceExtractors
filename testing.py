    # def export(self,name:typing.Optional[str],values:dict):
    #     if name == '' or name == ' ':
    #         name = f"Hour{datetime.now().hour}Minute{datetime.now().minute}"
    #     if self.treeWidget._ROW_INDEX > 0 :
    #         self.treeWidget.getCustomDataFrame(values).to_excel(f"Data/Exports/{name}[{datetime.now().date()}].xlsx",index=False)
    #         self.msg.showInfo(text=f"Exported Succecfully to 'Data/Exports/{name}[{datetime.now().date()}].xlsx'")
    #     else :
    #         self.msg.showWarning(text="No Data In App Please Try Again Later")






# # import pandas module
# import pandas as pd

# # create student dataframe with 3 columns
# # and 4 rows
# data = pd.DataFrame({'id': [1, 2, 3, 4],
# 					'name': ['sai', 'navya', 'reema', 'thanuja'],
# 					'age': [21, 22, 21, 22]})


# # drop first row
# frow = data.iloc[0]
# hh = data.iloc[1:, :]

# print(hh)
# print(frow)




import re
# as per recommendation from @freylis, compile once only # '<.*?>'
CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});') 

def cleanhtml(raw_html):
  cleantext = re.sub(CLEANR, '', raw_html)
  return cleantext

print(cleanhtml("""<p><strong>This telephone does not exist.Please check <a href="https://my.te.eg/anonymous/select"/>here</a></strong></p>"""))


