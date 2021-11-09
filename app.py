import sqlite3
import pandas as pd
from pandas.io import sql
from sqlalchemy import create_engine

file = 'Info.xlsx'
output = 'output.xlsx'
 
engine = create_engine('sqlite://', echo = False)
# df = pd.read_excel(file, sheet_name='Лист1')

xls = pd.ExcelFile(file)
print(xls.sheet_names)

for sheet_name in xls.sheet_names:
    print(sheet_name)
    sql_tables = 'tbl' + sheet_name
    print('Table -' + sql_tables)
    df = pd.read_excel(file, sheet_name=sheet_name, index_col=None)
    print(df)

    conn = sqlite3.connect('Info.db')

    df.to_sql(sql_tables, conn, if_exists='append', index= False)

    conn.close()

    

