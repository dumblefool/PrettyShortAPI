# - *- coding: utf- 8 - *-

import sys
reload(sys)
sys.setdefaultencoding('utf8')
from nltk.tokenize.punkt import PunktSentenceTokenizer
from sklearn.feature_extraction.text import TfidfTransformer,CountVectorizer
import networkx
import re
from bs4 import BeautifulSoup
import requests
import urllib2
import json


def Summarize(data):
    data=' '.join(data.strip().split('\n'))
    st=PunktSentenceTokenizer()
    tokens=st.tokenize(data)
    n=CountVectorizer()
    m=n.fit_transform(tokens)
    normalized=TfidfTransformer().fit_transform(m)
    graph=normalized*normalized.T
    rank=networkx.from_scipy_sparse_matrix(graph)
    scores=networkx.pagerank(rank)
    ordered=sorted(((scores[i],s) for i,s in enumerate(tokens)),reverse=True)
    f=u" "
    for j in range(0,2):
                f=f+ordered[j][1]
    return f

def prest():
	page='https://newsapi.org/v1/articles?source=the-next-web&sortBy=latest&apiKey=14408ed403874cc99cce51e8816a22af'
	json_obj=urllib2.urlopen(page)
	datas=json.load(json_obj)
	s=[]
	for items in datas['articles']:
    		s.append(str(items['url']))

	output=u" "
	t=[]
	for url in s:
        	soup=BeautifulSoup(requests.get(url).text,"lxml")
		page=max(soup.find_all(),key=lambda x:len(x.find_all('p',recursive=False)))
		data=u" "
		input=page.find_all('p')
		for p in input:
    			data=data+p.text
		output=Summarize(data)
		t.append(output)	
	i=0
	summ=u'Summary'
	for item in datas['articles']:
    		item.update({summ:t[i]})
    		i=i+1
	json.dumps(datas)
	return datas
