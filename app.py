from flask.templating import render_template_string
import sqlite3
import pandas as pd
from pandas.core import indexing
from pandas.io import sql
from sqlalchemy import create_engine, engine
from flask import Flask,render_template,request,redirect, url_for
import os
from werkzeug.utils import secure_filename



app=Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = b'_4#y2L"F4Q8z\n\xec]/'

engine = create_engine("sqlite:///data.db", echo=False)

@app.route("/", methods=["GET","POST"])
def func():
    if request.method=="POST":
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        xls = pd.ExcelFile(file)
        print(xls.sheet_names)
        for sheet_name in xls.sheet_names:
            print(sheet_name)
            sql_tables = sheet_name
            df = pd.read_excel(file,sheet_name=sheet_name, index_col=None)
            df.to_sql(sql_tables, con=engine, if_exists="append", index=False)   
            
        return redirect('/')
    return render_template("index.html")


filePath = "Info.xlsx"
conn = sqlite3.connect('data.db')
writer = pd.ExcelWriter(filePath, engine='xlsxwriter')

df= pd.read_sql("SELECT name FROM sqlite_master WHERE type='table'", conn)

print(df['name'])

for table_name in df['name']:
    sheet_name = table_name

    SQL = "select * from " + sheet_name

    dft = pd.read_sql(SQL, conn)

    print(dft)

    dft.to_excel(writer, sheet_name=sheet_name, index=False)
writer.save()   




    
if __name__ == "__main__":
    app.run(debug=True)

    

