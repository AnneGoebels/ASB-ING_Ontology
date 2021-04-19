
import os
import json
import re
import fnmatch
from lxml import html

from lxml import etree
from pprint import pprint
from lxml.html.clean import Cleaner
import logging

def getXmiData(file):
    #load xmi file (uml model)
    f = open(file,"rb")
    parser = etree.XMLParser()
    tree = etree.fromstring(f.read(),parser)
    

    #get name and ID of classes (also UML classes)
    model_meta={}
    classes = tree.xpath('//element[@xmi:type="uml:Class"]', namespaces=tree.nsmap)
    
    for cls in classes:
        cls_meta={}
        cls_meta['name']=cls.get("name")
        cls_meta['id']=cls.xpath("@xmi:idref",namespaces=tree.nsmap)[0].__str__()
        comment = cls.xpath('properties/@documentation',namespaces=tree.nsmap)
        if len(comment) >= 1 :
            c = comment[0]
            
            if '"' in c:
                x = c.replace('"',"'")
                cls_meta['comment']= x.strip()
                #print (x)
            
            else:
                cls_meta['comment']= c.strip()
        else:
            cls_meta ['comment'] = []
    
    
    #look for sub and super classes of the class   
        super_subs= cls.xpath('links/Generalization', namespaces=tree.nsmap)
        cls_meta['superclasses']=[]
        cls_meta['subclasses']=[]
        for sub_super in super_subs:
            start = sub_super.get("start")
    
            end = sub_super.get("end")
            id =  cls_meta.get('id')
            
            if end == id :
                cls_meta.get("subclasses").append(start)
            if start == id:
                cls_meta.get("superclasses").append(end)
        
    
    #add attributes of each class, with type and bounds
        
        cls_meta['attributes']=[]
        attribs = cls.xpath('attributes/attribute', namespaces=tree.nsmap)
        for att in attribs:                  
            att_meta={}
            att_meta['name']=att.get("name")
            att_meta['id']=att.xpath("@xmi:idref", namespaces=tree.nsmap)[0]
            att_meta['type']=att.xpath("properties[@type]", namespaces=tree.nsmap)[0].get("type")
            att_meta['upper']=att.xpath("bounds[@upper]", namespaces=tree.nsmap)[0].get("upper")
            att_meta['lower']=att.xpath("bounds[@lower]", namespaces=tree.nsmap)[0].get("lower")
            comment = att.xpath('documentation/@value',namespaces=tree.nsmap)
            #print (comment)
            if len(comment) >= 1:
                c = comment[0]
                if '"' in c:
                    x = c.replace('"',"'")
                    att_meta['comment']= x.strip()
                    #print (x)

                else:  
                    att_meta['comment']= c.strip()
            else:
                att_meta['comment'] = []
                #print (comment[0])
        
            
            atts= cls_meta.get('attributes')
            atts.append(att_meta)
         
           
    
    #look for Aggregations
        aggregations = cls.xpath('links/Aggregation', namespaces=tree.nsmap)
        if len(aggregations)!= 0:
            
            cls_meta["aggregations"]=[]
            for agg in aggregations:
                agg_id = agg.xpath("@xmi:id",namespaces=tree.nsmap)[0].__str__()
                
                end = agg.get("end")
                id = cls_meta.get("id")
                
                if end == id:
                    pass
                else:
                    agg_meta={}
                    agg_meta ["id"]=agg_id
                    agg_meta["target"]= end
                    
                    cardinality = tree.xpath("//connector[@xmi:idref='"+agg_id+"']/target/type/@multiplicity", namespaces=tree.nsmap)
                    agg_meta["cardinality"]=cardinality
                    
                    aggs=cls_meta.get("aggregations")
                    aggs.append(agg_meta)

        model_meta[cls_meta.get('id')]=cls_meta
        
    #look for associations
        associations = cls.xpath('links/Association', namespaces=tree.nsmap)
        if len(associations)!= 0:
            
            cls_meta["associations"]=[]
            for ass in associations:
                ass_id = ass.xpath("@xmi:id",namespaces=tree.nsmap)[0].__str__()
                
                end = ass.get("end")
                id = cls_meta.get("id")
                
                if end == id:
                    pass
                else:
                    ass_meta={}
                    ass_meta ["id"]=ass_id
                    ass_meta["target"]= end
                    
                    asso=cls_meta.get("associations")
                    asso.append(ass_meta)

        model_meta[cls_meta.get('id')]=cls_meta
    
    
   
    
    #datatype classes (object property ranges)
    
    #datatypes = tree.xpath('//packagedElement[@xmi:type="uml:PrimitiveType"]', namespaces=tree.nsmap)
    #for types in datatypes:
    #    data_meta={}
    #    name=types.xpath("@name",namespaces=tree.nsmap)[0].__str__()
    #    data_meta['name']= name
        
    #    model_meta[data_meta.get('name')]= data_meta
    
    
    return model_meta


#datei = "Bauwerke_Datentypen.xml"
#x = getXmiData(datei)
#print (x)
