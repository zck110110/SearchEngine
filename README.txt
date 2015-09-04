Chikai Zhang
id : 644368

The python file “RetrievalEngine.py” is the information retrieve engine for project of
“Building and evaluating an information retrieval engine”
It combine the evaluation function. 

Need import:nltk, nltk.data, re, math 

Output term:
1. output file:
    a .xls file will be build and store the information like recall, MRR, precision, MAP
2. out print:
    print all evaluation result
    for example:
                       +++++++++++++++++++++++++++++++
		    precision (average by all number of queries) : 0.516
                       average precision at 10 : 0.516
                       recall average: 0.0630761877955
                       MRR : 0.682333333333 
	             Average precision (average by precision at K) : [.44047619047619047,……]
                      MAP : 0.622256503527
                      ++++++++++++++++++++++++++++++

How to use ?
1 change the relevant directory of dataset, query set, qerl file with follow three variable:

directoryOfBLOGS
directoryOfQUERIES
directoryOfQERLS

for example :
directoryOfBLOGS='/Users/chikai/MYWORK/semester_1_2015/websearch/proj1data/blogs' directoryOfQUERIES ='/Users/chikai/MYWORK/semester_1_2015/websearch/proj1data/06.topics.851-900.txt' directoryOfQERLS = '/Users/chikai/MYWORK/semester_1_2015/websearch/proj1data/qrels.february'

2. change the limitation of number of documents retrieve

Find the variable:                 matchDocSNumLimit
Change initial value of it, the default is 10   -> retrieve 10 documents for each query

e.g          matchDocSNumLimt=10

3. if what query expansion function please change the variable  value as below:

wether_query_expansion = 1

   if not what to use the query expansion, do not do anything
   the default value is :

wether_query_expansion =0 

Hit: not do query expansion function the performance is better

4.  find “out” variable at end part of this code
e.g 
    out = open('Evaluation.xls','w')
change the file name of output
if not change, default is ‘Evaluation.xls’

Thanks for reading !


