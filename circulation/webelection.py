#!/usr/bin/env python3
    
import json,os,math,csv
import operator
import multiprocessing
import pandas as pd
path="Données/Corpus Web Elections Présidentielles (Sciences Po Bibliothèque)/elections-presidentielles-2017.csv"

csvfile = open(path, 'r')
fieldnames=("Id","Nom","URL","Type Acteur","Candidat Premier Tour","Candidat Second Tour")
reader = csv.DictReader( csvfile, fieldnames)
output =[]
x1={}
x2={}
for each in reader:
    
    row ={}
    row['Nom'] = each['Nom']
    row['URL']  = each['URL']
    row['Type Acteur']  = each['Type Acteur']
    row['Candidat Premier Tour']   = each['Candidat Premier Tour']
    try:x1[each['Candidat Premier Tour']]+=1
    except:x1[each['Candidat Premier Tour']]=0
    try:x2[each['Candidat Second Tour']]+=1
    except:x2[each['Candidat Second Tour']]=0
    row['Candidat Second Tour']   = each['Candidat Second Tour']
    output.append(row) 
print(len(output))
#json.dump(output,open('Données/Corpus Web Elections Présidentielles (Sciences Po Bibliothèque)/elections-presidentielles-2017.json','w'),indent=4,sort_keys=False)

