from lxml import etree
error_list = []

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
        cls_meta['kategorie']=cls.get("name")
        cls_meta['id']=cls.xpath("@xmi:idref",namespaces=tree.nsmap)[0].__str__()
        cls_meta['keys']=[]
        constraints = cls.xpath('constraints/constraint/@description', namespaces=tree.nsmap)
        
        #print (constraints)
        if len(constraints) != 0: 
            values = constraints[0].splitlines()
            
            for i in values:
                i = i.replace("'", "")
                i = i.split(',', 1)
               
                if len(i) > 1:
                    key_meta={}
                    key_meta['number']= i [0]
                    key_meta['text']= i [1]

                    keys= cls_meta.get('keys')
                    keys.append(key_meta)

                    model_meta[cls_meta.get('id')]=cls_meta
                
                else: 
                    error_list.append(i)

    return model_meta   





