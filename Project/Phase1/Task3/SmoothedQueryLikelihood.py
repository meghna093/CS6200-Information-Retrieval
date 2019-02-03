import math
import os


from math import log
from inputs import *
from file_functions import *;
from Parser import *;
from Indexer import *
from CommonUtils import *

from Summarisation import *




parsed_documents_path = os.path.join(master_path, parsed_docs_folder_name);
oneGram = 1 

docLengthDict       = getDocumentLengthDict();



INPUT_DIRECTORY = ""
INPUT_FOLDER = parsed_documents_path
QUERY = query_file_path
SMOOTHED_MODEL_SCORE_LIST = smoothened_LM_file_name
LAMBDA = 0.35



# Tests success===============
# d = {"ap" : 13, "apple" : 100}

# print(getDf("ap"));  => 13
# print(getDf(ap0")); => 0

# ***************************************************
def getDf(term,inv_index):
    # if the term is not present in any doc
    default  =0;

    if term in inv_index:
        
        tuplesList =inv_index[term];
        # print("df  of term ",len(tuplesList))
        return len(tuplesList);
    else:
        return 0;

# *************************************************


# *************************************************
# getTfInDoc():

# given : docId

# returns : 
# the number of term frequencies in a given doc
# ****************************************************
def getTfInDoc(term,docId,inv_index):
    if term in inv_index:
        termTupleTuple = inv_index[term];
        for tup in termTupleTuple:
            if str(tup[0]) == str(docId):
                return tup[1];  
    
    # else the following return is executed
    return  0;


#returns the length 
def calculateLength(INPUT_FOLDER):
    fileLengths = {}
    files = os.listdir(INPUT_FOLDER)
    for file in files:
        file =os.path.join(INPUT_FOLDER, file)
        doc = open(file,'r').read()
        file = file[:-4]
        file = os.path.basename(file)


        fileLengths[file] = len(doc.split())
    # print("length :",fileLengths)
    return fileLengths

# returns_doc_length
def queries(fileName):
    f = open(fileName,'r')
    queryList = []
    for line in f:
        line=" ".join(line.split())
        line=line.strip() 
        # print("q" , line)
        if line[-1] == '\n':            # Remove new line character
            queryList.append(line[0:-1])
        elif line[-1] == ' ':           # Remove last space
            queryList.append(line[0:-1])
        else:
            queryList.append(line)

    queryProcessor(queryList)
    return queryList


def queryProcessor(querySet):
    queryTerms = {}
    for query in querySet:
        queryTerms[query] = query.split(" ")      
    return queryTerms


# write the final maximum results document to a file
def rankAllDocs(docWeights, qid, max_hits, file):
    # file = open(SMOOTHED_MODEL_SCORE_LIST, "a")
    sortedList = sorted(docWeights, key=docWeights.__getitem__)
    top = sortedList[-(max_hits):]
    top.reverse()
    rank = 0
    for doc in top:
        rank += 1
        text= str(qid+1) + "   " + "Q0" + "   " +\
        str(doc) + "   " + str(rank) + "   " + str(docWeights[doc]) +\
        "   " + "SQLM" +"\n"
        file.write(text)
    file.write("\n\n ---------------------------------------------------------------------------------------\n\n\n")


# def ifDocPresentInTerm():


#calculating Query Likelihood Score for each query term
def SQLMScore(max_hits, total_collection,\
    index, querySet, uniqueDocuments, doclength, file_name = SMOOTHED_MODEL_SCORE_LIST):
    #default parameters
    qid = -1
    i=0
    temp_score_sum=0
    queryTerms = queryProcessor(querySet)
    file = open(file_name, "w")
    for query in querySet:
        qid += 1
        docWeights = {}
        for document in uniqueDocuments:
            documentScore = 0
            for queryTerm in list(set(queryTerms[query])):
                 if queryTerm in index.keys():                        
                    termWeight_doc = getTfInDoc(queryTerm,document,index)
                    modD=doclength[str(document)]
                    termWeight_collection= getDf(queryTerm,index)
                    queryFreq_by_modD= termWeight_doc/modD
                    collectionFreq_by_total_collection= termWeight_collection/total_collection
                    score = (((1-LAMBDA)*queryFreq_by_modD)+(LAMBDA*collectionFreq_by_total_collection))
                    temp_score_sum+=math.log(score)
            docWeights[document] = temp_score_sum
            temp_score_sum=0
        rankAllDocs(docWeights, qid, max_hits, file)


#Execution - for unstopped
def main_unstopped():
    inv_index           = build_inverted_index(parsed_documents_path,oneGram);
    max_hits = 100
    uniqueDocuments=[]
    uniqueDocuments = [file[:-4] for file in os.listdir(INPUT_FOLDER)] #unique_docs(index) # Set of Docs
    total_docs = len(uniqueDocuments)          # Int- Size of Corpus
    doclength = calculateLength(INPUT_FOLDER)              # INt- Size of each document in a Dictionary    
    querySet = (get_query_list());    
    total_collection=sum(doclength.values())
    print("Processing scores...............")
    SQLMScore(max_hits, total_collection, 
    inv_index, querySet, uniqueDocuments, doclength)      # Function call which computes document score
    return;


# Execution for stopped
def main_stopped():
    inv_index           = build_inverted_index(stopped_parsed_docs_path,oneGram);
    max_hits = 100
    uniqueDocuments=[]
    uniqueDocuments = [file[:-4] for file in os.listdir(stopped_parsed_docs_path)] #unique_docs(index) # Set of Docs
    total_docs = len(uniqueDocuments)          # Int- Size of Corpus
    doclength = calculateLength(stopped_parsed_docs_path) # INt- Size of each document in a Dictionary    
    querySet = (get_query_list());    
    total_collection=sum(doclength.values())
    print("Processing scores...............")
    docLengthDict       = getDocumentLengthDict(stopped_parsed_docs_path);
    querySet = get_stopped_query_list(stopwords(),get_query_list())
    SQLMScore(max_hits, total_collection, 
    inv_index, querySet, uniqueDocuments, doclength,file_name = SmoothenedQueryStoppedFile)  # Function call which computes document score
    return;

# Execution for stemmed
def main_stemmed():
    inv_index           = build_inverted_index(stemmed_parsed_docs_path,oneGram);
    max_hits = 100
    uniqueDocuments=[]
    uniqueDocuments = [file[:-4] for file in os.listdir(stemmed_parsed_docs_path)] #unique_docs(index) # Set of Docs
    total_docs = len(uniqueDocuments)          # Int- Size of Corpus
    doclength = calculateLength(stopped_parsed_docs_path) # INt- Size of each document in a Dictionary    
    querySet = (get_query_list());    
    total_collection=sum(doclength.values())
    print("Processing scores...............")
    docLengthDict       = getDocumentLengthDict(stemmed_parsed_docs_path);
    querySet = get_stemmed_queries()
    SQLMScore(max_hits, total_collection, 
    inv_index, querySet, uniqueDocuments, doclength,file_name = SmoothenedStemmedFile)  # Function call which computes document score
    return;



# main_unstopped()
# main_stopped()
main_stemmed()
