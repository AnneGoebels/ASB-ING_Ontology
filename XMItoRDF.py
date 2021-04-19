# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 12:50:34 2020

@author: Anne
"""



from urllib.parse import quote_plus
from rdflib import (XSD, BNode, ConjunctiveGraph, Graph, Literal, Namespace,URIRef)
from rdflib.namespace import OWL, RDF, RDFS
import sqlite3


conn = sqlite3.connect ("ASBING.db")
c=conn.cursor()

def dataToRdf(model_meta):

    graph =Graph()
    ANS = Namespace("http://asbingowl.org/def/2016/asbingowl#")
    AONS = Namespace("http://asbingowl.org/def/2013/asbingowl/keys#")
    ANSK = Namespace("http://asbingowl.org/def/2016/asbingowl/keys#")

    graph.bind("owl", OWL)
    graph.bind("asb",  ANS)
    graph.bind("asbkey13",  AONS)
    graph.bind("asbkey",  ANSK)


    
    class_ids = []
    
    #construct classes (also complex datatypes)
    for meta_class_id, meta_class in model_meta.items():
        class_ids.append(meta_class_id)
        cls_name = meta_class.get("name")
        cls_url_name = quote_plus(cls_name)
        cls_res = URIRef(ANS +cls_url_name)
        
        graph.add((cls_res,RDF.type, OWL.Class))
        graph.add((cls_res, RDFS.label, Literal(meta_class.get('name'), lang="de")))
        
        #if len(meta_class.get('comment')) >4:
        if meta_class.get('comment') != None:
            if len(meta_class.get('comment')) >3:
                graph.add((cls_res, RDFS.comment, Literal(meta_class.get('comment'))))
            else:pass
        else: pass
    
    c.execute("select ASB, SUBCLASS from DATAMAPPING WHERE SUBCLASS NOT NULL")
    dataclasses = c.fetchall()
    for asbclass, dataclass in dataclasses:
        graph.add((URIRef(ANS +dataclass), RDF.type, OWL.Class))
        graph.add((URIRef(ANS +dataclass), RDFS.subClassOf, URIRef(ANS +asbclass)))
      
    #print(graph.serialize(format="turtle").decode("utf-8"))
    
    all_key_res = URIRef (ANS + "GesamteSchluessel")
    graph.add((all_key_res,RDF.type, OWL.Class))
    graph.add((all_key_res,RDFS.comment,Literal("abstrakte Klasse fuer neue und alte Schluesseltabellen")))

    
    super_prop= URIRef(ANS + "hatSchluesselKennung")
    graph.add((super_prop, RDF.type, OWL.ObjectProperty))
    graph.add((super_prop, RDFS.range, all_key_res))
    
    
    
    #write attributes
    for meta_class_id,meta_class in model_meta.items():
        domain_name = meta_class.get("name")
        if meta_class.get("attributes",[]) != None:
            for att in meta_class.get("attributes",[]):
    
                prop_name = domain_name+"_"+att.get("name")
                prop_url_name = quote_plus(prop_name)
                #print (prop_name)
    
                prop = URIRef(ANS + prop_url_name)
                
                asbdatatype = att.get("type")
                print(asbdatatype)
                c.execute("SELECT XSD, SUBCLASS FROM DATAMAPPING WHERE ASB =?", (asbdatatype,))
                res = c.fetchone()
                print (type(res))
               
                if type(res) != tuple :
                    print (asbdatatype)
                    prop_range = URIRef(ANS + asbdatatype)
                    graph.add((prop, RDF.type, OWL.ObjectProperty))
                    graph.add((prop, RDFS.subPropertyOf, super_prop))
                    graph.add((prop, RDFS.range, prop_range))
                    graph.add((super_prop, RDFS.domain, URIRef(ANS+ domain_name)))
              
                
                elif type(res) == tuple:
                    if res[1] == None:
                        print(res[0])
                        graph.add((prop,RDF.type, OWL.DatatypeProperty))
                        graph.add((prop, RDFS.range, URIRef(XSD+ res[0])))
                    
                    else:
                        #print(res[1])
                        graph.add((prop, RDF.type, OWL.ObjectProperty))
                        graph.add((prop, RDFS.range, URIRef(ANS + res[1])))
                       
                        
                        graph.add((URIRef(ANS+ ("has"+res[0])) ,RDF.type, OWL.DatatypeProperty))
                        graph.add((URIRef(ANS+ ("has"+res[0])), RDFS.range, URIRef(XSD+ res[0])))
                        graph.add((URIRef(ANS+ ("has"+res[0])), RDFS.domain, URIRef(ANS + res[1])))
                        
                
                graph.add((prop, RDFS.domain, URIRef(ANS+ domain_name)))
                graph.add((prop, RDFS.label , Literal(prop_url_name,lang='de')))
                
                #if len(att.get('comment')) >4:
                    
                if att.get('comment') != None:
                    if len(att.get('comment')) >3:
                        graph.add((prop, RDFS.comment, Literal(att.get('comment'))))
                    else:pass
                else: pass
    
        else:
            pass
    
    #print(graph.serialize(format="turtle").decode("utf-8"))

        
    
    
    #hierarchy
   
    
    for meta_class_id,meta_class in model_meta.items():
        cls_name = meta_class.get('name')
        super_names = list(set(meta_class.get('superclasses',[])))
        #print (super_names)
        if len(super_names) != 0:
            for super_name in super_names:
                cls_res = URIRef(ANS[cls_name])
                super_cls =  model_meta.get(super_name)
                #print(super_cls)
                if super_cls != None:
                    super_cls = URIRef (ANS[model_meta[super_name]['name']])
    
                    graph.add((cls_res, RDFS.subClassOf, super_cls))
                else:
                    pass
        else:
            pass
    
        
    #write aggregations
    
    partOf= URIRef(ANS + "isPartOf")
    graph.add((partOf, RDF.type, OWL.ObjectProperty))
    graph.add((partOf, RDFS.label, Literal("isPartOf", lang='de')))
    
    
    for meta_class_id,meta_class in model_meta.items():
        cls_name = meta_class.get('name')
        for agg in meta_class.get('aggregations',[]):
            target = (agg.get('target'))
            cardi = (agg.get('cardinality'))
            
            cls_res = URIRef(ANS[cls_name])
            graph.add((partOf, RDFS.domain, cls_res))
            target_res = URIRef (ANS[model_meta[target]['name']])
            graph.add((partOf, RDFS.range, target_res)) 
            graph.add((cls_res, partOf, target_res))
            
            #restr = BNode()
            
            #x.add((restr, RDF.type, OWL.Restriction))
            #x.add((restr, OWL.OnProperty, partOf_Rel))
            #x.add((restr, OWL.Cardinality, Literal (cardi, datatype=XSD.integer) ))

#write associations#

    asso = URIRef(ANS + "associatedWith")
    graph.add((asso, RDF.type, OWL.ObjectProperty))
    graph.add((asso, RDFS.label, Literal("associatedWith", lang='de')))
    
    for meta_class_id,meta_class in model_meta.items():
        cls_name = meta_class.get('name')
        for ass in meta_class.get('associations',[]):
            target = (ass.get('target'))
            if target in class_ids:
            
                cls_res = URIRef(ANS[cls_name])
                graph.add((asso, RDFS.domain, cls_res))
                target_name = model_meta[target]['name']
                #print (target_name)
                target_res = URIRef (ANS + target_name)
                graph.add((asso, RDFS.range, target_res)) 
                graph.add((cls_res, asso, target_res))
            
            else:
                pass
                #print(target)


    return graph




