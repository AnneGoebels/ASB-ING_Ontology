from urllib.parse import quote_plus
from rdflib.namespace import OWL, RDF, RDFS, XSD
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.plugins.sparql import prepareQuery

from rdflib.term import BNode 
import xmi_new_keys_parse
import sqlite3

def to_camel_case(text):
    s = text.replace("-", " ").replace("_", " ").replace("*"," ").replace("."," ").replace("/","_").replace(",","_").replace("(", "_").replace(")", "_")
    s = s.split()
    if len(text) == 0:
        return text
    return s[0] + ''.join(i.capitalize() for i in s[1:])

conn = sqlite3.connect ("DataResources\ASBING.db")
c=conn.cursor()

model_meta = xmi_new_keys_parse.getXmiData("DataResources\schluessel.xml")

g = Graph()

 #w3id version
ANS = Namespace("https://w3id.org/asbingowl/core#")
AONS = Namespace("https://w3id.org/asbingowl/keys#")
ANSK = Namespace("https://w3id.org/asbingowl/keys/2013#")



g.bind("owl", OWL)
g.bind("asb",  ANS)
g.bind("asbkey13",  AONS)
g.bind("asbkey",  ANSK)


g.parse(r"Ontologies\oldkeysW3.ttl", format="ttl")

all_key_res = URIRef (ANSK + "GesamteSchluessel")

new_schlussel_res = URIRef (ANSK + "Schluesseltabellen")
g.add((new_schlussel_res,RDF.type, OWL.Class))
g.add((new_schlussel_res,RDFS.comment,Literal("Abstract superclass of all new keys")))
g.add ((new_schlussel_res, RDFS.subClassOf, all_key_res))


new_value_res = URIRef (ANSK + "Kennung")
g.add((new_value_res, RDF.type, OWL.DatatypeProperty))
g.add((new_value_res, RDFS.range, URIRef(XSD + "string")))
g.add((new_value_res, RDFS.domain, new_schlussel_res))

for meta_class_id, meta_class in model_meta.items():
        kategorie_name = meta_class.get("kategorie")
        kategorie_res = URIRef(ANS+ kategorie_name)
        
        if meta_class.get("keys",[]) != None:
            for key in meta_class.get("keys",[]):
                
                
                key_name_cam = to_camel_case(key.get("text"))
                key_name_comp = kategorie_name+"_"+key_name_cam
                key_name_url = quote_plus(key_name_comp)
                name_res = URIRef(ANSK + key_name_url)
                
                key_number = key.get("number")
                
                g.add((name_res,RDF.type, OWL.Class))
                g.add((name_res, RDFS.subClassOf, new_schlussel_res))
               # x= BNode()
               # g.add((name_res, haskeyunion_res, x))
                g.add((name_res, new_value_res, Literal(key_number)))
                g.add((name_res, RDFS.subClassOf, kategorie_res ))
                g.add((name_res, RDFS.label, Literal(key.get("text"), lang="de")))
                
                
                if len(key_number) > 2 and "." in key_number :
                    supercl_number = key.get("number")[0:-2]
                    if supercl_number[-1] == ".":
                        #print(supercl_number)
                        supercl_number = supercl_number[0:-1]
                    #print(supercl_number)
                    
                    cons_query= prepareQuery("""
                    construct
                    {?keycl rdfs:subClassOf ?supercl.}
                    where
                    {?supercl asbkey:Kennung ?KennungSuper.
                     ?supercl rdfs:subClassOf ?kategorie.}""" 
                    , initNs={'asbkey':ANSK})

                    for row in g.query(cons_query, initBindings={'keycl': name_res, 'KennungSuper':Literal(supercl_number), 'kategorie':kategorie_res}):
                        #print(row)
                        g.add(row)
                
                c.execute("select Alte_Nummer from SCHLUESSEL_MAPPING_TABLE WHERE (Kategorie=? and Neue_Position =? and Bewertung >= 0.79)",(kategorie_name, key_number))
                r = c.fetchone()
                if r != None and r!= []:
                    nmbr = r[0]
                    #print(nmbr)
                    cons_query2= prepareQuery("""
                    construct
                    {?keycl owl:sameAs ?oldcl.
                     ?oldcl owl:sameAs ?keycl.}
                     where
                    {?oldcl asbkey13:Kennung ?Kennung.}""" 
                    , initNs={'asbkey13':AONS, 'owl':OWL})

                    for row in g.query(cons_query2, initBindings={'keycl': name_res, 'Kennung':Literal(str(nmbr))}):
                       # print(row)
                        g.add(row)
                    
                    
                    
#print(g.serialize(format="turtle").decode("utf-8"))
                
f = open (r"Ontologies\allkeysW3.ttl","wb")
f.write(g.serialize( format='turtle'))



