# ASB-ING_Ontology 

The ASB-ING Ontology is directly derived from the new German ASB-ING data model, provided as UML. The scripts shows how the conversion of the original UML model to the Ontology works. As the ASB-ING data model is not official published yet, it is not part of the data set here. 

The ASB-ING Ontology consists of three parts. 
The Core Ontology contains the main elements and attributes of the original new ASB-ING schema.
Additionally, there are two sub-ontologies representing the key classes of the old and the new ASB-ING Versions. 
The old keys have the prefix "asbkey13"and the new keys "asbkey".
The file "ASB-Ontology_Merged" merged them all into one turtle file. 

These ontologies can be used to derive Linked Data Versions of SIB-Bauwerke Datasets. 
The scripts for the conversion of the ontologies can be found in the Scripts folder.
.