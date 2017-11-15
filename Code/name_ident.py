from os import listdir

import pdb
import nltk
import sys,csv
import re
import string
from nltk import pos_tag
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.tokenize import wordpunct_tokenize
from itertools import chain, groupby, product
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.cluster.kmeans import KMeansClusterer

vectorizer = TfidfVectorizer(input='filename',decode_error='ignore',min_df=0.5,max_df = 0.8,sublinear_tf=True,use_idf=True)
prop_noun_mp = {}
phrases_mp = {}
clusters_mp = {}
word_vec = None

def dataProcessing():
    global prop_noun_mp
    global phrases_mp
    for txt in listdir("Text"):
        stopwords = nltk.corpus.stopwords.words("english")
        puncts = list(string.punctuation)
        # pdb.set_trace()
        puncts.remove('-')
        ignore = set(stopwords + puncts)
        phrases = set()
        # pdb.set_trace()
        data = open("./Text/"+txt, 'r').read()
        data = data.decode('utf-8')
        sent_tokenize_list = sent_tokenize(data)
        sent_list = sent_tokenize(data)
        pos_list = []
        for i in sent_tokenize_list:
            i = i.replace('-\n',"")
            i = i.replace('\n'," ")
            # pdb.set_trace()
            if re.match('.*\[.*\].*', i, re.DOTALL) or re.match('.*\([a-z]*.*[0-9]{4}.*\).*', i, re.DOTALL): #extracting all the sentences having citations for e.g.[1],[3, 5]
                # print i
                b = word_tokenize(i)
                vares = pos_tag(b)
                # print vares
                for var in vares:
                    # print var
                    try:
                        word = var[0].decode('string-escape')
                        if (len(word)>1) and (word.find('/')<0) and (word.find('|')<0):
                            if var[1]=="NNP":
                                # pdb.set_trace()
                                pos_list.append(word)
                    except:
                        pass
            # print pos_list
            # pdb.set_trace()
        for i in sent_list:
        	word_list = [word.lower() for word in wordpunct_tokenize(i)]
        	phrase_list = []
        	for group in groupby(word_list, lambda x: x in ignore):
        		if not group[0]:
        			phrase_list.append(tuple(group[1]))
        	phrases.update(phrase_list)
        # print phrases
        phrases_mp[txt] = phrases
        prop_noun_mp[txt] = pos_list
        # pdb.set_trace()

def tf_idf(fileslist):
    # fileslist = []
    global word_vec
    for txt in listdir("Text"):
        if txt.endswith(".txt"):
            fileslist.append("Text/"+txt)
    # pdb.set_trace()
    word_vec = vectorizer.fit_transform(fileslist)
    word_vec = word_vec.toarray()

def kcluster(fileslist):
    global clusters_mp
    nClusters = int(sys.argv[1])
    kclusterer = KMeansClusterer(nClusters, distance=nltk.cluster.util.cosine_distance, repeats=25)
    assigned_clusters = kclusterer.cluster(word_vec, assign_clusters=True)
    print fileslist
    # print assigned_clusters
    for i in range(nClusters):
        clusters_mp[i] = []
    for fle in range(len(assigned_clusters)):
        val = fileslist[fle]
        val = val[5:]
        clusters_mp[assigned_clusters[fle]].append(val)

def main():
    fileslist=[]
    # dataProcessing()
    # print phrases_mp
    # print prop_noun_mp
    tf_idf(fileslist)
    kcluster(fileslist)
    for i in clusters_mp:
        print "Cluster " + str(i) + ": "
        print len(clusters_mp[i])
        for j in clusters_mp[i]:
            print j + " "
        print

if __name__ == '__main__':
    main()
