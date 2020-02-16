import openpyxl
import pandas as pd


dataset = [
    {'name': 'conv1', 'shape': '12'},
    {'name': 'bn', 'shape': ''}
]
str1 = 'conv1.0'
str2 = '12345'
data_list = [{str1,str2}]
dataframe = pd.DataFrame(dataset)
goodsdf = pd.DataFrame(data_list, columns=['name', 'shape',])
writer = pd.ExcelWriter('test.xlsx')
dataframe.to_excel(excel_writer=writer, sheet_name='sheet_moren')

goodsdf.to_excel(excel_writer=writer, sheet_name='sheet_fang')
writer.save()
writer.close()
