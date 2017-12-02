try:
	import pandas as pd
	from gensim import corpora,models,similarities
	import gensim
	import pyLDAvis.gensim
	import treetaggerwrapper
	from gensim.models import LdaModel,LsiModel,CoherenceModel,Word2Vec
	from stop_words import get_stop_words
	from sklearn.cluster import KMeans, MiniBatchKMeans
except:print("see requierments for needed packages")
import csv,json,sys,os
size=300

def MeanWV(doc,model):
	g=[0 for i in range(size)]

	for i in doc:
		vectw=[ww for ww in model.wv[i]]
		for j in range(size):g[j]+=vectw[j]
	return [i/len(doc) for i in g]
	
def kmeanTest(data,true_k,_verbose=True):
	km = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1,verbose=_verbose)
	model = gensim.models.wrappers.FastText.load_fasttext_format('../../divers/wiki.fr')
	X=[MeanWV(doc,model)for doc in data]
	km.fit(X)

	

def filterData(name,keywords=['porc','cantine']):
	data = pd.read_csv(name,sep=';')
			
	with open('cantineporc.json', 'w') as outfile:
		json.dump(categories, outfile)
	

#build topic model of a corpus
def build_topic(name,jsoname,contentField="text",usetfidf=False,output=False,plot=True,filetype='csv',sfilename=None):
	data_JLM=None
	if sfilename:
		with open(sfilename) as f:fr_stop = [i.split('\n')[0] for i in f.readlines()]
	else:fr_stop = get_stop_words('fr')
	try:
		with open(jsoname) as json_data: data_JLM = json.load(json_data)	
		docs=data_JLM["tweets"]
		dictionary = gensim.corpora.Dictionary(docs)
		corpus=[dictionary.doc2bow(doc) for doc in docs]
	except:
		docs=[]
		corpus=[]
		dictionary = gensim.corpora.Dictionary(docs)
		if filetype=='csv':data = pd.read_csv(name,sep=';')[contentField]#
		else:exit()
		tagger=treetaggerwrapper.TreeTagger(TAGLANG='fr',TAGDIR="../ouest-france2/TreeTagger")
		for text in data:
			try:tags=tagger.tag_text(text)
			except:continue
		
			doc=[]
			for i in tags:
				tmp=i.split("\t")
				if len(tmp)<3 or len(tmp[0])<4:continue
				if tmp[1] in ["NOM","VER"] and tmp[-1] not in fr_stop and "’" not in tmp[-1] :doc+=[tmp[-1]]
			if "cantine" in doc and "porc" in doc:docs+=[doc]
			dic=dictionary.doc2bow(doc,allow_update=True)
			corpus+=[dic]
		with open(jsoname, 'w') as outfile:
			json.dump({"tweets":docs}, outfile)
	
	if usetfidf:
		tfidf = gensim.models.TfidfModel(corpus)
		corpus=tfidf[corpus]
	#kmeanTest(docs,10)
	ldamodel=LdaModel(corpus=corpus, id2word=dictionary,num_topics=5)
	if output:print(ldamodel.show_topics(num_topics=-1, num_words=10))
	
	if plot:
		data = pyLDAvis.gensim.prepare(ldamodel, corpus, dictionary)
		pyLDAvis.show(data)


#build a json file from fake story
#storyFilename:storyID_query_istrue_other (storyID,query,istrue,other should not contains _)

def fitStrie(storyFilename):
	data = pd.read_csv(storyFilename,sep=';')
	storyID,query,is_true,other=storyFilename.split("_")
	
	queries=data["queries"]
	platforms=data["platform"]
	media_types=data["media type"]
	dates=data["date"]
	authors=data["author"]
	"""fcbs,fcsl,fcsc=data["facebook shares"],data["facebook likes"],data["facebook comments"]
	twr,twrep,twl=data["twitter retweets"],data["twitter replies"],data["twitter likes"]
	yv,yl,yc,yf,yd=data["youtube views"],data["youtube likes"],data["youtube comments"],data["youtube favourites"],data["youtube dislikes"]
	ina,inl,inc=data["instagram followers"],data["instagram likes"],data["instagram comments"]
	wp,ws,wc=data["web pagerank"],data["web shares on twitter"],data["web comments"]
	sr,sl,sc=data["sinaweibo reposts"],data["sinaweibo likes"],data["sinaweibo comments"]
	dv,dc=data["dailymotion views"],data["dailymotion comments"]"""
	fcid=data["facebook author id"]
	twid=data["twitter author id"]
	yid=data["youtube author ID"]
	did=data["dailymotion author ID"]
	iid=data["instagram author id"]
	sid=data["sinaweibo author ID"]
	ids=[0 for i in range(len(data))]
	score=[0 for i in range(len(data))]

	tf = data["twitter followers"] # 4
	fs = data["facebook shares"] # 5
	pr = data["web pagerank"] # 6
	yv = data['youtube views'] # 7
	dv = data['dailymotion views'] # 8
	print(pr)
	for i in range(len(data)):
		score[i]=10*pr[i]
		
		if platforms[i]=="Facebook":
			score[i]=100*min(15000,fs[i])/15000
			ids[i]=fcid[i]
		if platforms[i]=="Twitter":
			score[i]=100*min(20000000,tf[i])/20000000
			ids[i]=twid[i]
		if platforms[i]=="Youtube":
			score[i]=100*min(200000,yv[i])/200000
			ids[i]=yid[i]
		if platforms[i]=="Instagram":
			ids[i]=iid[i]
			score[i]=10*pr[i]
		if platforms[i]=="Dailymotion":
			ids[i]=did[i]
			score[i]=100*min(200000,dv[i])/200000
		if platforms[i]=="Sinaweibo":
			ids[i]=sid[i]
			score[i]=10*pr[i]
		if platforms[i]=="Website":
			ids[i]="WEB"
			score[i]=10*pr[i]
	print(ids);exit()
	story={"datapoints":[],"agents":[]}
	for i in range(len(data)):	
		datapoint={"entity_id":query,"entity_type":queries[i],"platform":platforms[i],"media_type":str(media_types[i]),"case":storyFilename,"date":dates[i],"as_true":is_true,"visibility_score": 0}
		datapoint["agent_id"]=ids[i]
		datapoint["visibility_score"]=str(score[i])
		if score[i]>0 and score[i]<100:print(score[i])
		agent={"id":datapoint["agent_id"]}
		agent["name"]=authors[i]
		agent["visibility_score"]=None
		story["datapoints"]+=[datapoint]
		story["agents"]+=[agent]
	with open(storyID+query+is_true+".json", 'w') as outfile:
		json.dump(story, outfile)
				
		
		
	
	
#build_topic("circulation/stories/radarly_fillon_blanchi.csv",'fillon_blanchi.json',usetfidf=True,sfilename="../ouest-france2/stopwords.txt")
fitStrie('11_Mohamed SaouANDmacronmohamed_faux_saou-export-radarly-2180-documents-1512127315425.csv')


