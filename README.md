# ASB-ING_Ontology 

The ASB-ING Ontology is directly derived from the new German ASB-ING data model, provided as UML. The scripts shows how the conversion of the original UML model to the Ontology works. As the ASB-ING data model is not official published yet, it is not part of the data set here. 

The ASB-ING Ontology consists of three parts. 
The Core Ontology contains the main elements and attributes of the original new ASB-ING schema.
Additionally, there are two sub-ontologies representing the key classes of the old and the new ASB-ING Versions. 
The old keys have the prefix "asbkey13"and the new keys "asbkey".
The file "ASB-Ontology_Merged" merged them all into one turtle file. 

These ontologies can be used to derive Linked Data Versions of SIB-Bauwerke Datasets. 
The scripts for the conversion of the ontologies can be found in the Scripts folder.

Recently the onotology is published using the following URI's, however we are working on proberly publish them using the w3id.org domain as soon as possible. The Sub-Ontologies don't have an html documentation yet, but they will be provided soon.

Core Ontology :

html: https://annegoebels.github.io/index-en.html
ttl: https://annegoebels.github.io/ontology.ttl
json-ld: https://annegoebels.github.io/ontology.json
N-Triples: https://annegoebels.github.io/ontology.nt
rdf/xml: https://annegoebels.github.io/ontology.xml

Keys Sub-Ontology:

ttl: https://annegoebels.github.io/SubOntNewKeys.ttl


Old Keys Sub-Ontology:

ttl: https://annegoebels.github.io/SubOntOldKeys.ttl


Contact:
Anne Göbels
Design Computation RWTH
goebels@dc.rwth-aachen.de
