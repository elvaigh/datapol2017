try:
	import pandas as pd
except:print("you need to install pandas")


def simu(b,words):
	for w in words:
		sim=len(list(set(w) & set(b)))/len(list(set(w) | set(b)))
		if sim>0.7:return True
	return False
name="test.csv"
data = pd.read_csv(name,sep=';')
text=data["text"]
dates=data["date"]
urls=data["permalink"]
authors=data["author"]
content=[]
import csv
treated=[]
j=0
with open('test70.csv', 'w') as csvfile:
	spamwriter = csv.writer(csvfile, delimiter=';')
	spamwriter.writerow(["date","text","permalink","author"])
	for i in range(len(data)):
		tmp=[dates[i],text[i],urls[i],authors[i]]
		
		try:tt=text[i].split()
		except:tt=str(text[i]).split()
		if not simu(tt,treated):
			treated+=[tt]
			spamwriter.writerow(tmp)
		else:
			j+=1
			print(j)
		  
print("doublons",j)
