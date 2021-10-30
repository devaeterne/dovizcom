import datetime
import requests
from bs4 import BeautifulSoup
import pyodbc as odbc
import pandas as pd

sql_conn = odbc.connect('Driver={SQL Server};SERVER=;DATABASE=;UID=safak;PWD=;')
# Connection example for Sql Server
# ('Driver={SQL Server};SERVER=10.0.0.1;DATABASE=databasename;UID=user;PWD=password;')
query = "select * from dovizcom"
# table snapshot
df = pd.read_sql(query, sql_conn)
df.head()
print (df)
r = requests.get('https://www.doviz.com/')
r2 = requests.get('https://www.doviz.com/')

source = BeautifulSoup(r.content,"lxml")
source2 = BeautifulSoup(r2.content,"lxml")
USD = source.find("div",attrs={"class","item[:2]"}).text
EUR = source2.find("div",attrs={"class","text-xl"}).text
an = datetime.datetime.now()
tarih = datetime.datetime.strftime(an,'%Y.%m.%d')
print(tarih,'USD :' ,USD.replace(",","."),'EUR :' ,EUR.replace(",","."))

cursor = sql_conn.cursor()
SQLCommand = "update dovizcom(dtarih,nusd, neur) set (?,?,?)"
Values = [tarih,USD.replace(",","."),EUR.replace(",",".")]
cursor.execute(SQLCommand,Values)
sql_conn.commit()