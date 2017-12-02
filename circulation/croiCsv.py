#!/usr/bin/env python3
    
import json,os,math,csv

"""merge list of csv based on list of fields

features:list of common fields
csvs: list of files to merge
"""

def mergeOnFeatures(features,csvs):
	if len(csvs)<2:exit()
	a = pd.read_csv(csvs[0],sep=";")
	b = pd.read_csv(csvs[1],sep=";")
	#b = b.dropna(axis=1)
	merged = a.merge(b, on=features)
	for i in range(2,len(csvs)):
		tmp=pd.read_csv(csvs[i],sep=";")
		merged = tmp.merge(merged, on=features)
	merged.to_csv("output.csv", index=False)

