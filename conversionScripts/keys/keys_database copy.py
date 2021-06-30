import pandas as pd
import sqlite3

#create database with key and text

conn = sqlite3.connect('ASBING.db')

c = conn.cursor ()

c.execute ('drop table if exists KEY_TABLE')

conn.commit()

c.execute('''
CREATE TABLE [KEY_TABLE](
	[KEY] [varchar] ,
    [NAME][varchar] ,
    [LANGTEXT] [varchar],
    [SUPERCLASS] [varchar])
''')

conn.commit()

file = pd.read_excel (r"C:\GitHub\TwinGen\DataResources\ASBINGKEYS.xlsx") 

file.to_sql('KEY_TABLE', conn, if_exists = 'append',index= False)



def getParKey(key):
    rev = key[::-1]
        
    for i in rev:
        if i != "0":
            indx = rev.index(i)
            break
                
    char = "0"
    parRev = rev[:indx] + char + rev [indx +1:]
    
    parentKey = parRev[::-1]
    
    c.execute("select KEY, LANGTEXT from KEY_TABLE where KEY = ?", (parentKey,))
    name = c.fetchone()
    if name != None:
        return name
    else:
        return None

def listToString(list):
    text = " "
    return (text.join(list))

#### get keys and text from excel #####

c.execute("select KEY, LANGTEXT from KEY_TABLE")
for i in c.fetchall():
    #print (i)
    
    parKey = getParKey(i[0]) 
    if parKey != None:
        NewName = parKey[1]+" "+str(i[1])
        #print (NewName)
        #print(parKey)
        c.execute("update KEY_TABLE set LANGTEXT = ? where KEY =? ", (NewName, i[0]))
        conn.commit()
        c.execute("update KEY_TABLE set SUPERCLASS = ? where KEY =? ", (parKey[0], i[0]))
        conn.commit()
           
        
        




             
            