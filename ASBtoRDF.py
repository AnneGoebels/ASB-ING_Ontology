# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 11:31:32 2020

@author: Anne
"""

from rdflib.graph import Graph
import XMIParser 
import XMItoRDF


dataModel = XMIParser.getXmiData (r"C:\GitHub\TwinGen\DataResources\ASB-Ing-neu-20201216.xml")



g = XMItoRDF.dataToRdf(dataModel)

g2 = Graph()
file = r"C:\GitHub\TwinGen\Ontologies\keys_all.ttl"
g2.parse(file, format="turtle")

g += g2

f = open ("Ontologies\ASB_Ontology_FINAL.ttl","wb")
f.write(g.serialize( format='turtle'))