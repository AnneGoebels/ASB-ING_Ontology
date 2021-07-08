import sqlite3
import pandas as pd

datamappings = pd.read_excel(r"C:\GitHub\TwinGen\DataResources\DatatypeMapping.xlsx", sheet_name = "Tabelle1", header=0 )

conn = sqlite3.connect ("ASBING.db")

c=conn.cursor()

c.execute ('drop table if exists DATAMAPPING')

conn.commit()

c.execute('''CREATE TABLE DATAMAPPING(
    [ASB] [nvarchar](50),
    [XSD][nvarchar](50),
    [SUBCLASS][nvarchar](50))
    ''')

datamappings.to_sql('DATAMAPPING', conn, if_exists = 'append',index= False)

conn.commit()

