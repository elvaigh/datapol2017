import newspaper
import pandas as pd

#get article content by url
name="Données/base_des_hoax.csv"
data = pd.read_csv(name)["URL of publication"]
tmp=[]
for i in data:
	for url in i.split("\n"):tmp+=[url]

for url in tmp:
	try:
		if '\r' in url:x=ulr.split('\r')[0]
		else:x=url
		print(x)
		article = newspaper.Article(x,language='fr')
		article.download()
		article.parse()
	
		
	except:continue
	#article.publish_date;article.text
	

