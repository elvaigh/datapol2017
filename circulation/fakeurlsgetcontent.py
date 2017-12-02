import json,os
import urllib.request
from bs4 import BeautifulSoup

import newspaper

with open('updates.json') as json_data: data= json.load(json_data)
sites=list(data['sites'].keys())
print(sites)
urls=list(data['urls'].keys())
print(urls);exit()
def getJsonFiles(FilesDir):
	filesNames=[]
	for element in os.listdir(FilesDir):
		if not os.path.isdir(element) and element.endswith('.json'):filesNames+=[FilesDir+'/'+element]
	return filesNames

linkdir="Données/Social Listening des 5 Principaux Candidats (Radarly Linkfluence)/links/"
for url in urls:
	paper = newspaper.build('http://'+url)
	"""for article in paper.articles:
		print(article.url)"""
	for category in paper.category_urls():print(category)


"""used=0
files=getJsonFiles(linkdir)
for usedurls in files:
	used=0
	with open(usedurls) as json_data: usedurls= json.load(json_data)
	for x in usedurls:
		url1,urls2=x['url']["terminal"],x['url']["normalized"]
		if url1 in urls or urls2 in urls:used+=1
	print(used)"""

