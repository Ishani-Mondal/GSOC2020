#!/usr/bin/env python
# coding: utf-8

# In[79]:


#!/usr/bin/env python
# coding: utf-8

from pyclausie import ClausIE
import spacy
from rdflib import Graph
from rdflib import URIRef, BNode, Literal
from rdflib.namespace import RDF, FOAF
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk import pos_tag
import spacy
nlp = spacy.load("en_core_web_sm")
from nltk.corpus import wordnet as wn

cl = ClausIE.get_instance()
'''
Reading the Obama Abstract File
'''
f=open('Obama_abstract.txt')
content=f.read()
nlp=spacy.load('en')
doc=nlp(content)

'''
Parsing the JSON generated by Spotlight
'''

import json

resource_dict={}
with open('Obama_Json.json') as f:
    data = json.load(f)
    for elem in (data['Resources']):
        resource_dict[elem['@surfaceForm'].lower()]= elem['@URI']
        
        
sents=[]

for sent in doc.sents:
    sents.append(sent.text)
    
'''
Using PyClausIE Algorithm to Extract out the Triples in TEXT Format
'''

triples = cl.extract_triples(sents)
lemmatizer = WordNetLemmatizer()

"""
Using a handful of white-list of lexicalized verbs
"""
nlp=spacy.load('en')

import json
with open('type_dict.json') as f:
    type_dict = json.load(f)

with open('white_dict.json') as f:
    white_dict = json.load(f)
    
with open('synset_dict.json') as f:
    synset_dict = json.load(f)

place_list=[]
person_list=[]

f=open('place_list.txt')
content=f.read()
for line in content.split("\n"):
    place_list.append(line)
    
f=open('person_list.txt')
content=f.read()
for line in content.split("\n"):
    person_list.append(line)



"""
Creating the RDF Graph using the triples
"""
f1=open('RDF_Triples.txt','w')

rdfGraph = Graph()

for triple in triples:
    sentence = str(triple).split(",")[1].split("=")[1][1:-1]+ " "+str(str(triple).split(",")[2].split("=")[1])[1:-1]+" "+str(str(triple).split(",")[3].split("=")[1])[1:-2]
    
    s=str(triple).split(",")[1].split("=")[1][1:-1].lower()
    p=str(str(triple).split(",")[2].split("=")[1])[1:-1].lower()
    o=str(str(triple).split(",")[3].split("=")[1])[1:-2].lower()
    
    doc = nlp(s+" "+p+" "+o)
    doc1 = nlp(s+" "+p+" "+o)
    
    nps=[]
    doc=nlp(s)
    for np in doc.noun_chunks:
        nps.append(np.text)
        

    #if(s.lower()=='he'):
    s=resource_dict['obama']
    
    doc=nlp(o)
    
      
    '''
    Substituting the DBPedia Spotlight Resource URLS
    '''
    subjects=[]
    if(len(nps)>0):
        if(nps[0].lower() in resource_dict.keys()):
            subjects.append(resource_dict[nps[0]])
            subject = URIRef(subjects[0])
        else:
            for key, elem in resource_dict.items():
                if(key.lower() in nps[0].lower()):
                    subjects.append(nps[0].replace(key,resource_dict[key]))
                    
    else:
        subjects.append(s)   
    
    modified_p=lemmatizer.lemmatize(p, 'v')+" "+str(o.split(" ")[0])
    if(modified_p in white_dict.keys() or modified_p in type_dict.keys()):
        p=modified_p
        o=" ".join(o.split(" ")[1:])
        
    attr=[]
    for chunk in doc1.noun_chunks:
        if(chunk.root.dep_=='attr'):
            #print(chunk.root.text)
            attr.append(chunk.root.text)
        elif(len(attr)==0 and chunk.root.dep_=='pobj'):
            #print(chunk.root.text)
            attr.append(chunk.root.text)
    
    for elem in list(white_dict.keys()):
        if(elem in o):
            o=o.replace(elem, "")
            p=white_dict[elem]
        if(elem in p):
            p=p.replace(elem, white_dict[elem])
            
    for elem in list(type_dict.keys()):
        if(elem in p):
            p=p.replace(elem, type_dict[elem])

    
    if(len(attr)>0 and p.startswith("http")):
        syns=str(str(wn.synsets(attr[0])[0]).split("'")[1]).split(".")[0]
        if(attr[0] in list(resource_dict.keys())):
            f1.write(s+"\t"+p+"\t"+str(resource_dict[attr[0]])+"\n")
        else:
            for item in place_list:
                if(item in p):
                    for elem in list(resource_dict.keys()):
                        if(elem in o):
                            f1.write(s+"\t"+p+"\t"+str(resource_dict[elem])+"\n")

            for item in person_list:
                if(item in p):
                    for elem in list(resource_dict.keys()):
                        if(elem in attr[0]):
                            f1.write(s+"\t"+p+"\t"+str(resource_dict[attr[0]])+"\n")
                            print(s,p,)
                    syns=str(wn.synsets(attr[0])[0]).replace("Synset('","").replace(".n.01')","")
                    if(syns in list(synset_dict.keys())):
                        f1.write(s+"\t"+p+"\t"+str(synset_dict[syns])+"\n")


# In[80]:


from rdflib import Graph
from rdflib import URIRef, BNode, Literal
from rdflib.namespace import RDF, FOAF

f=open('RDF_Triples.txt')
content=f.read()
rdfGraph = Graph()

for line in content.split("\n"):
    if(line!=""):
        subject = URIRef(line.split("\t")[0])
        if("type" in line.split("\t")[1]):
            predicate = RDF.type
        else:
            predicate = URIRef(line.split("\t")[1])
        object1= URIRef(line.split("\t")[2])
        
        rdfGraph.add((subject, predicate, object1))



print(rdfGraph.serialize(format='turtle').decode('utf-8'))



