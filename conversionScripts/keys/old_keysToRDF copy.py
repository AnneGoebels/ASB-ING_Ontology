import sqlite3
from urllib.parse import quote_plus
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import OWL, RDF, RDFS, XSD
from rdflib.plugins.sparql import prepareQuery


def to_camel_case(text):
    s = text.replace("-", " ").replace("_", " ").replace("*"," ").replace("."," ").replace("/","_").replace(",","_").replace("(", "_").replace(")", "_")
    s = s.split()
    if len(text) == 0:
        return text
    return s[0] + ''.join(i.capitalize() for i in s[1:])

conn = sqlite3.connect (r"C:\GitHub\TwinGen\ASBING.db")
c=conn.cursor()

graph =Graph()
#ANS = Namespace("http://asbingowl.org/def/2016/asbingowl#")
#AONS = Namespace("http://asbingowl.org/def/2013/asbingowl/keys#")
#ANSK = Namespace("http://asbingowl.org/def/2016/asbingowl/keys#")

 #w3id version
ANS = Namespace("https://w3id.org/asbingowl/2016/core#")
AONS = Namespace("https://w3id.org/asbingowl/2013/keys#")
ANSK = Namespace("https://w3id.org/asbingowl/2016/keys#")


graph.bind("owl", OWL)
graph.bind("asb",  ANS)
graph.bind("asbkey13",  AONS)
graph.bind("asbkey",  ANSK)

all_key_res = URIRef (ANSK + "GesamteSchluessel")
#graph.add((all_key_res,RDF.type, OWL.Class))
#graph.add((all_key_res,RDFS.comment,Literal("abstrakte Klasse fuer neue und alte Schluesseltabellen")))

schlussel_res = URIRef (AONS + "Schluesseltabellen")
graph.add((schlussel_res,RDF.type, OWL.Class))
graph.add((schlussel_res,RDFS.comment,Literal("Abstract superclass of all old keys")))
graph.add((schlussel_res, RDFS.subClassOf, all_key_res))

old_key_res = URIRef (AONS + "Kennung")
graph.add((old_key_res,RDF.type, OWL.DatatypeProperty))
graph.add((old_key_res, RDFS.range, URIRef(XSD + "string")))
graph.add((old_key_res, RDFS.domain, schlussel_res))
graph.add((old_key_res,RDFS.comment,Literal("alter 15stelliger Schluessel")))

c.execute("select KEY, NAME, LANGTEXT, SUPERCLASS from KEY_TABLE")
n = c.fetchall()
for keyData in n:
    #print (keyData)
    if keyData[1] != None:
        if "***" not in keyData[1]:
            #print(keyData)
            #print(name[0])
            key_name = str(keyData[0])+"_"+to_camel_case(keyData[1])
            #print (key_name)
            class_name = quote_plus(key_name)
            #print(class_name)
            name_res = URIRef(AONS + class_name)
        #    print (name_res)
                
            graph.add((name_res,RDF.type, OWL.Class))
            graph.add((name_res, RDFS.subClassOf, schlussel_res))
            graph.add((name_res, RDFS.label, Literal(keyData[1], lang="de")))
            graph.add((name_res, RDFS.comment, Literal(keyData[2], lang="de")))
            graph.add((name_res, old_key_res, Literal(keyData[0])))
            
        else:
            pass
        
        
c.execute("select KEY, SUPERCLASS from KEY_TABLE where SUPERCLASS not null")
s = c.fetchall()

for keys in s:
    
    cons_query= prepareQuery("""
            construct
            {?keycl rdfs:subClassOf ?supercl.}
            where
            {?keycl asbkey13:Kennung ?Kennung.
             ?supercl asbkey13:Kennung ?KennungSuper.}""" 
            , initNs={'asbkey13':AONS})

    for row in graph.query(cons_query, initBindings={'Kennung': Literal(keys[0]), 'KennungSuper':Literal(keys[1])}):
        print(row)
        graph.add(row)

f = open (r"Ontologies\oldkeysW3.ttl","wb")
f.write(graph.serialize( format='turtle'))



