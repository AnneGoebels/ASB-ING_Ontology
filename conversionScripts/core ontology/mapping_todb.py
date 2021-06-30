import pandas as pd
import sqlite3


#mapping elements from excel
mappings = pd.read_excel(r"C:\GitHub\TwinGen\scripts\ontology\new_mapping.xlsx", sheet_name = "Sheet1", header=0 )

conn = sqlite3.connect ("ASBING.db")

c=conn.cursor()

c.execute ('drop table if exists MAPPING')

conn.commit()

c.execute('''CREATE TABLE MAPPING(
    [QTabelle] [nvarchar](50),
    [QName][nvarchar](50),
    [Objekt_im_Alten_Model][nvarchar](50),
    [Objekt_im_Neuen_Model] [nvarchar](50),
    [ZTabelle] [nvarchar](50),
    [ZName] [nvarchar](50),
    [Mapping_Regel] [nvarchar](50),
    [Ontology_ObjectProperty] [nvarchar](50) NULL,
    [Fixed_KeyValue] [nvarchar](50) NULL,
    [Ontology_Class] [nvarchar] (50) NULL,
    [Bemerkung] [nvarchar]  NULL,
    [Kommentar] [nvarchar]  NULL)
    ''')

mappings.to_sql('MAPPING', conn, if_exists = 'append',index= False)

conn.commit()

