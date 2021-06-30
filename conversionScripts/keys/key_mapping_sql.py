import pandas as pd
import sqlite3

#create database with key and text

conn = sqlite3.connect('ASBING.db')

c = conn.cursor ()

##keymapping table 

c.execute ('drop table if exists SCHLUESSEL_MAPPING_TABLE')

conn.commit()

c.execute('''
CREATE TABLE [SCHLUESSEL_MAPPING_TABLE](
	[Alter_Schluessel] [int] NOT NULL,
    [Alte_Nummer] [int] NOT NULL,
    [Alter_Text] [varchar] NOT NULL,
    [Bewertung] [float] NOT NULL,
    [Neuer_Text] [varchar] NOT NULL,
    [Neue_Position] [float] NOT NULL,
    [Kategorie] [varchar] NOT NULL,
    [Neue_Id] [varchar] NOT NULL)
''')

conn.commit()

#keys excel file

file = pd.read_excel (r"C:\TwinGen\SIB\SIB-BW2_Automatisiertes_Schluesselmapping_v0.03.xlsx") 

file.to_sql('SCHLUESSEL_MAPPING_TABLE', conn, if_exists = 'append',index= False)