#author: chikai zhang (644368)
#This python code use the nltk,re,os,math. This is a information retrieve engine
#5 function for tokenization, cosine similarity, information retrieve, calculate Precisio at K and average
#three main parts: 1. query processing 2.build inverse index 3, information retrieve and evaluation
#out put the evaluation results of this information engine
#all evaluation data write into a .xls file
#Copyright reserved
import nltk
import re
import numpy
import nltk.data
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
import os
import math
from nltk.corpus import wordnet as wn

#tokenize process function, input raw string, out put list of words,
#also has the query expansion function based on "num" value: 0 not do, 1 do
def mytokenizeprocess(words,num):
    newwords = words.lower()
    newwords = tokenizer.tokenize(newwords)
    if num ==1:
        new=[]
        for w in newwords:
            new.append(w)
            for synset in wn.synsets(w):
                for lemma in synset.lemmas():
                    new.append(lemma.name())
        new = set(new)
        new = list(new)
        newwords = new
    outword = []
    for word in newwords:
        if word not in stops:
            outword.append(myst.stem(word))#stemmer
    return outword

#consine simlarity of query and relvant documents
def cosinesmilarity(query,diction,termdft,total,doclen,docnumlimit):
    accmulators={}
    normal={}
    for w in range(0,len(query)):
        if diction.has_key(query[w]):
            for blogid in diction[query[w]]:
                if accmulators.has_key(blogid):
                    #normal[blogid]=normal[blogid]+math.pow(diction[query[w]][blogid]*math.log10(total/termdft[w]),2)
                    #accmulators[blogid]=accmulators[blogid]+diction[query[w]][blogid]*math.log10(total/termdft[w])
                    normal[blogid]=normal[blogid]+math.pow(math.log10(diction[query[w]][blogid]+1)*math.log10(total/termdft[w]),2)
                    accmulators[blogid]=accmulators[blogid]+math.log10(1+diction[query[w]][blogid])*math.log10(total/termdft[w])
                else:
                    accmulators[blogid]=math.log10(1+diction[query[w]][blogid])*math.log10(total/termdft[w])
                    normal[blogid]=math.pow(math.log10(1+diction[query[w]][blogid])*math.log10(total/termdft[w]),2)
                    #accmulators[blogid]=diction[query[w]][blogid]*math.log10(total/termdft[w])
                    #normal[blogid]=math.pow(diction[query[w]][blogid]*math.log10(total/termdft[w]),2)
    for selectblogid in accmulators:
        accmulators[selectblogid]=accmulators[selectblogid]/math.sqrt(normal[blogid])
        #accmulators[selectblogid]=accmulators[selectblogid]/doclen[selectblogid]
    sortlist = sorted(accmulators.iteritems(),key=lambda d:d[1],reverse= True)
    outlist = sortlist[0:docnumlimit]
    return outlist

#find the document relevant number,output retrieve documents id dict
def NumberOfRelDocs(posting,myqreldict,numb):
    out=[]
    if myqreldict.has_key(numb) and len(posting)>0:
        for i in range(0,len(posting)):
                if myqreldict[numb].has_key(posting[i][0]):
                    out.append(i)
        return out
    else:
        return out
#calculate the precision at K
def PatK(reldocs,k):
    if len(reldocs)<1:
        return 0
    else:
        cnt = 0.0
        for relvid in reldocs:
            if (relvid+1)>k:
                break
            cnt=cnt + 1.0
        out = cnt/k
        return out
#calluate the average precision by precision at K
def AveP(reldocs):
    if len(reldocs)<1:
        return 0.0
    else:
        cnt =0.0
        out = 0.0
        for relvid in reldocs:
            cnt=cnt+1.0
            PK= cnt/(relvid+1)
            out = out+PK
        out = out/len(reldocs)
        return out

## The Main Programming begining
#the main varialbels, file directory for documents set ,query set, judgement set
directoryOfBLOGS='/Users/chikai/MYWORK/semester_1_2015/websearch/proj1data/blogs'
directoryOfQUERIES ='/Users/chikai/MYWORK/semester_1_2015/websearch/proj1data/06.topics.851-900.txt'
directoryOfQERLS = '/Users/chikai/MYWORK/semester_1_2015/websearch/proj1data/qrels.february'
myst=LancasterStemmer()#use for stemming processing
stops = set(stopwords.words('english'))#stop words set of nltk
tokenizer = RegexpTokenizer('[A-Za-z0-9]+|\$[\d\.]+')#define tokenizer
termdict={}# dictionary of inverse indexing
docmentlen={}#dictionary of each document length after text processing
mycount = 0# count number of words in a document
filenumber = 0#count the total file number in a documents set for later use
matchDocSNumLimt=10# limit number of retrieve documents

#variables use in the query processing and evaluation
newcount = 0
querynumberlist = []
retrieve=[]#store the retrieve document id list
sprecision = 0#single precision of each quary
srecall = 0#single recall of each quary
precision=[]
recall = []
RR=[]
MRR=0
AVEERGEP=[]#store each query average precision(calculate by precision at K)
precisionatK=[]
MAP=0#mean average precision
wether_query_expansion=0# if 1 do the query expansion, if 0 not do
# open qrels(the true answers) file and generate the dict of whole relevant docs
qrelsfile = open(directoryOfQERLS)
qreldict={}#dictionary of judgement document id
while 1:
    qlines = qrelsfile.readlines(10000)
    if not qlines:
        break
    for qline in qlines:
        qline=qline.strip('\n')
        qline=qline.split(' ')
        relvnum=int(qline[3])
        if qreldict.has_key(qline[0]):
            if relvnum>0:
                qreldict[qline[0]][qline[2]]=relvnum

        else:
            qreldict[qline[0]]={}
            if relvnum>0:
                qreldict[qline[0]][qline[2]]=relvnum
qrelsfile.close()



#list of files blogs, process one by one generate the dictionary
for filename in os.listdir(directoryOfBLOGS):
    directory = directoryOfBLOGS+'/'+filename
    reformfilename=filename.split('.')
    newfilename=reformfilename[0]
    file=open(directory)
    filenumber = filenumber+1
    while 1:
        lines = file.readlines(10000)
        if not lines:
            break
        for line in lines:
            #word process
            processedwords = mytokenizeprocess(line,0)
            mycount=mycount+len(processedwords)
            #create dictionary
            for word in processedwords:
                if termdict.has_key(word):
                    if termdict[word].has_key(newfilename):
                        termdict[word][newfilename]=termdict[word][newfilename]+1
                    else:
                        termdict[word][newfilename]=1
                else:
                    termdict[word]={}
                    termdict[word][newfilename]=1
    docmentlen[newfilename]=mycount
    mycount=0
    file.close()

#query process, output the ranked list of document of queries
file1 = open(directoryOfQUERIES)
while 1:
    queryline= file1.readlines(10000)
    if not queryline:
        break
    else:

        for line in queryline:
            m = re.split('<|>',line)
            if len(m)>2 and m[1]=='num':
                querynumber = filter(str.isdigit,m[2])
                querynumberlist.append(querynumber)
            elif len(m)>2 and m[1]=='title':
                #do the query expansion
                myout = mytokenizeprocess(m[2],wether_query_expansion)
                newcount=newcount+1
                #sort the query with the df,less df value in the front
                dft = []
                for w in range(0,len(myout)):
                    if termdict.has_key(myout[w]):
                        dftmin=len(termdict[myout[w]])
                    else:
                        dftmin = 0
                    j= w+1
                    while j<len(myout):
                        if (termdict.has_key(myout[j]) and dftmin>len(termdict[myout[j]])):
                            dftmin = len(termdict[myout[j]])
                            temp = myout[w]
                            myout[w]=myout[j]
                            myout[j]=temp
                            j=j+1
                        else:
                            j=j+1
                    dft.append(dftmin)
                    dftmax = 0
                retrieve = cosinesmilarity(myout,termdict,dft,filenumber,docmentlen,matchDocSNumLimt)
                findrelnumb = NumberOfRelDocs(retrieve,qreldict,querynumber)
                IntRelvFileNumb= len(findrelnumb)
                IntRelvFileNumb = float(IntRelvFileNumb)
                if len(retrieve)<1:
                    sprecision = 0
                else:
                    sprecision= IntRelvFileNumb/len(retrieve)
                precision.append(sprecision)
                srecall = IntRelvFileNumb/len(qreldict[querynumber])
                recall.append(srecall)
                #find RR and MRR
                if IntRelvFileNumb<1.0:
                    R=0
                    RR.append(R)
                    MRR=MRR+R
                else:
                    #1/RANK -> R
                    R=1.0/(findrelnumb[0]+1)

                    RR.append(R)
                    MRR=MRR+R
                #find precision at k OR average precision, MAP
                Poften=PatK(findrelnumb,10)
                precisionatK.append(Poften)
                singleavp = AveP(findrelnumb)
                AVEERGEP.append(singleavp)
                MAP=MAP + singleavp
file1.close()
MRR=MRR/newcount
MAP = MAP/newcount
CHECK=0
for i in precisionatK:
    CHECK = CHECK +i
pak = CHECK/50
CHECK=0
for i in precision:
    CHECK=CHECK+i
AVP = CHECK/50
CHECK=0
for i in recall:
    CHECK=CHECK+i
AVR =CHECK/50
# wirth precision, recall ,Avp, MAP,MRR, RR into the .xls file
out = open('Evaluation.xls','w')
out.write('precisionAt10')
out.write('\t')
out.write(str(pak)+'\t')
out.write('\n')
out.write('AveragePrecision(10)')
out.write('\t')
out.write(str(AVP)+'\t')
out.write('\n')
out.write('AverageRecall')
out.write('\t')
out.write(str(AVR)+'\t')
out.write('\n')
out.write('precision')
for w in precision:
    out.write('\t')
    out.write(str(w)+'\t')
    out.write('\n')
out.write('recall')
for w in recall:
    out.write('\t')
    out.write(str(w)+'\t')
    out.write('\n')
out.write('RR')
for w in RR:
    out.write('\t')
    out.write(str(w)+'\t')
    out.write('\n')
out.write('MRR')
out.write('\t')
out.write(str(MRR)+'\t')
out.write('\n')
out.write('avep')
for w in AVEERGEP:
    out.write('\t')
    out.write(str(w)+'\t')
    out.write('\n')
out.write('MAP')
out.write('\t')
out.write(str(MAP)+'\t')
out.write('\n')
print '+++++++++++++++++++++++++++++++'
print 'Precision (average by all number of queries) :',AVP
print 'Average precision at 10 :',pak
print 'Recall average:',AVR
#print 'RR : ',RR
print 'MRR :',MRR
print 'Average precision (average by precision at K) :',AVEERGEP
print 'MAP :', MAP
print '++++++++++++++++++++++++++++++'








#def precision():
