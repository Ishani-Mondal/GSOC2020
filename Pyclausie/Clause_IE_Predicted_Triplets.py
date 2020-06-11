#!/usr/bin/env python
# coding: utf-8

# In[2]:


from pyclausie import ClausIE
cl = ClausIE.get_instance()

import json

resource_dict={}
with open('Obama_Json.json') as f:
    data = json.load(f)
    for elem in (data['Resources']):
        resource_dict[elem['@surfaceForm'].lower()]= elem['@URI']


# In[8]:


import spacy
nlp=spacy.load('en')
f=open('Obama_abstract.txt')
content=f.read()

doc=nlp(content)

sents=[]

for sent in doc.sents: 
    sents.append(sent.text)
i=1
triples = cl.extract_triples(sents)
for triple in triples:
    s=str(triple).split(",")[1].split("=")[1][1:-1].lower()
    p=str(triple).split(",")[2].split("=")[1][1:-1].lower().lower()
    o=str(triple).split(",")[3].split("=")[1][1:-2].lower()
    print(i, "<",s,">","<",p,">","<",o,">")
    i=i+1



