from math import log

from inputs import *
from file_functions import *;
from Parser import *;
from Indexer import *
from CommonUtils import *

from Summarisation import *

query =     "hurricane isabel damage";

#Relevance information has beeen set to zero.

parsed_documents_path = os.path.join(master_path, parsed_docs_folder_name);
oneGram = 1 
inv_index           = build_inverted_index(parsed_documents_path,oneGram);
docLengthDict       = getDocumentLengthDict();


query_rel_docs_dict = get_query_rel_docs_dict();
# print(query_rel_docs_dict)


################################################

def calcdocLengthSum():
    sumAlldocLength = 0;
    for docId in docLengthDict:
        docLength = int (docLengthDict[docId])
        sumAlldocLength += docLength
    return sumAlldocLength;

def calcAvgDocLength():
    return calcdocLengthSum()/ len(docLengthDict)

def calcK(docID):
    dl = docLengthDict[docID];
    K = k1 * ((1 -  b) +  b * dl/avgDl);
    return K;


##################################################
# qfi  -  the term frequency in the query,
# As the relevance info is not given 
# the following should be zero 
ri  = 0;
R   = 0;

# Constants -----------------------------
k1  =1.2 
k2  =100
b   =0.75

N   =  len(docLengthDict) # number of documents containing the given term
avgDl = calcAvgDocLength()
print("N                : "  ,  N);
print("Avg doc length   : "  ,  avgDl);



# ****************************************************
# getDf: 
# dfDict - represents the dict containing 
           # {term1 : NumberOf DocumentsContainingIT,
           # {term2: NumberOf DocumentsContainingIT.. }

# term - String,
#       the term for which the df has to be returned

# returns 0 if the given term is not in dfDict

# Tests success===============
# d = {"ap" : 13, "apple" : 100}

# print(getDf("ap"));  => 13
# print(getDf(ap0")); => 0

# ***************************************************
def getDf(term):
    # if the term is not present in any doc
    default  =0;

    if term in inv_index:
        
        tuplesList =inv_index[term];
        # print("df  of term ",len(tuplesList))
        return len(tuplesList);
    else:
        return 0;

# *************************************************
# getTfInDoc():

# given : docId

# returns : 
# the number of term frequencies in a given doc
# ****************************************************
def getTfInDoc(term,docId):
    if term in inv_index:
        termTupleTuple = inv_index[term];
        for tup in termTupleTuple:
            if str(tup[0]) == str(docId):
                return tup[1];  
    
    # else the following return is executed
    return  0;

def getTopHits(rankedScoreList,n):
    return rankedScoreList[:n]

# *****************************************
# queryScoreDocument()
# The below function calculates  the score for a document 
# for the complete query
# ******************************************
def  queryScoreDocument(query,docId):
    termList = query.split(" ");
    # Doc score for the given query
    docScore = 0 
    for queryTerm in termList:
        # qfi  -  the term frequency in the query,
        qfi = query.count(queryTerm)
        ni  = getDf(queryTerm);
        # print("qfi.,................",qfi)
        docScore += termScoreDocument(qfi,queryTerm, docId,ni);
    return docScore;


# The below function calculates  the score for a document 
# for  a given term from the query
def  termScoreDocument(qfi,term,docId,ni):
    # print("term_score .... ",qfi,term,docId)

    K   = calcK(docId);

    # ==========================================
    fi = getTfInDoc(term, docId)
    numerator =   ((ri + 0.5) /  (R - ri + 0.5))
    denominator =(ni - ri + 0.5)/(N - ni - R + ri + 0.5)

    logVal  =  log( numerator/ denominator )
    expr1   =   (k1 + 1)*fi / (K + fi)
    expr2   =  (k2 + 1)*qfi/ (k2 + qfi);

    docScore = logVal * expr1 * expr2;

    # print("Term :---------------   '", term);
    # print("logVal         : ", logVal, \
    #   "\nexpr1        : ", expr1, \
    #   "\nexpr2        : ", expr2, \
    #   "\nnumerator    : ", numerator,\
    #   "\ndenominator  : ", denominator)
    # print("\nDoc score : ", docScore);

    return docScore;

# print(termScoreDocument(1,"is",0));

# Test**********************************************
# docId = 0
# query = "is name is";
# docSocreForQuery = queryScoreDocument("is name is",docId);
# print("Query      : ",query,\
#   "\ndoc_id       : ",docId,\
#   "\nDoc score    : ",docSocreForQuery);



# scoreAllDocuments********************************
# returns : List of tuples like 
# [(1, 8.0),
# (2, 9.0)]
# where each tuple is (docId, score )
def scoreAllDocuments(query, docList):
    docScoreDict ={};
    for docId in docList:
        scoreListValues = [];
        score  =  queryScoreDocument(query, docId);
        docScoreDict[docId]  = score;
        # print(docId, "        : ",docScoreDict[docId]);   
    return docScoreDict;

# sortDocIdListByScore****************************
# returns : List of tuples like  (sorted from top scores to low scores)
# [  (2, 9.0),
#    (1, 8.0)]
# where each tuple is (docId, score )

def sortDocIdListByScore(docScoreDict):
    sortedDocScoreDict = sorted(docScoreDict.items(), \
    key=lambda k_v:  k_v[1], reverse=True)
    return sortedDocScoreDict;



# ================getSearchResults==============================
# queryList : represents the list of queries 
# each query in the list could be a single token or
# a string with multiple words

# n        : represents the number of top results to be returned 
# ==============================================================

# returns a list of doc id with their scores 
# Sorted  based on the document score in reverse 

# Example: 
# getSearchResults (hurricane isabel damage, 2)

#     docId :   Score
# => [{12 : 9.0},
    # {8  : 8.5}]



# getSearchResults***********************
# given :
# query -  String, the query for which the search must be performed
        # ex: "Hurricane", "Green Lights"
# hits  -  the number of results to be displayed 
#           (top n : from high to low bm25 scores)

# returns 
# the top n docId:score tuples array 
# example : [(23,9.0), (12,8.0)]

def getSearchResults(query,hits = -1):
    print("Searching for :  ",query)
    scoredDocList       =   scoreAllDocuments(query,getdocIdList());
    sortedDocScoreList  =   sortDocIdListByScore(scoredDocList);
    if hits == -1 : len(sortedDocScoreList)
    topHitsList         =   getTopHits(sortedDocScoreList, hits);
    return topHitsList


# return dict 
# for each query in queryList
    # with query from queryList as key
    # results : List of tuples as valu
def searchListOfQueries(queryList, hits = -1):
    queryResults = {};


    for query in queryList:
        queryResults[query] = getSearchResults(query,hits);

    return queryResults;



def topHitsDictToString(topHitsDict,hideScores = False):
    newStr = ""
    for searchQuery in topHitsDict:
        
        newStr = newStr + "\n" + str(searchQuery) + "--------------\n"
        for docScoreTuple in topHitsDict[searchQuery]:
            if hideScores == True:
                newStr = newStr + "   " + str(docScoreTuple[0])
            else :
                newStr = newStr + "\n" + str(docScoreTuple)
    return newStr

def writeTopHitsDictToTxt(fileName,topHitsDict, hideScores = False):
    with open(fileName, 'w') as file:
        file.write(topHitsDictToString(topHitsDict, hideScores) );
    return;


def top_hit_dict_to_summarise(all_queries_results):
    new_all_QueriesResults = ()
    print(all_queries_results)
    for query in all_queries_results:
        print("query : ",query)
        doc_id_list_with_scores = all_queries_results[query]
        print("Doc id with scores ",doc_id_list_with_scores)
        doc_id_list = [x[0] for x in doc_id_list_with_scores]
        doc_id_list = tuple(doc_id_list)
        print("new Doc id with scores ",doc_id_list)
        print("query tuple ", (query,doc_id_list))

        new_all_QueriesResults = new_all_QueriesResults + ((query,doc_id_list),)
        print("new_all_QueriesResults", new_all_QueriesResults)    
    return new_all_QueriesResults

# def calcR(term,query_rel_doc_list,inv_index):
def topHitsDictToTxtFile(topHitsDict,file_name):
    newStr = ""
    query_id = 0;
    file = open(file_name, "w")
    for searchQuery in topHitsDict:
        query_id += 1
        rank = 0 
        newStr = newStr + "\n" + str(searchQuery) + "--------------\n"
        text = ""
        for docScoreTuple in topHitsDict[searchQuery]:
            rank +=1;
            
            doc_id =str(docScoreTuple[0])
            doc_id = CACM_PREFIX + doc_id
            
            score = str(docScoreTuple[1])
            system_name  = "BM25"

            text= text + str(query_id) + "   " + "Q0" + "   " +   str(doc_id) +\
            "   " + str(rank) + "   " + str(score) + "   " + system_name +"\n"
        file.write(text)
    return None

# ======================================================================
# #Without stopped_list
# list_of_queries = get_query_list();
# topHitsTupTup = searchListOfQueries(list_of_queries,100);
# topHitsDictToTxtFile(topHitsTupTup,bm25ResultsFile)

#With stopped
stopped_list_of_queries = get_stopped_query_list(stopwords(),get_query_list())


# topHitsDictToTxtFile(topHitsTupTup,bm25StoppedResultsFile)


# to_sumamrise  = top_hit_dict_to_summarise((("ab",((1,1.0), (2,2.0) )),("ab1",((11,1.0), (21,2.0) ))))
# to_sumamrise  = top_hit_dict_to_summarise(topHitsTupTup)
# print("To summarise")

# print(to_sumamrise)

# results_to_summarise = getRelevanceResult(to_sumamrise)
# print_to_file("bm25_summary.txt", results_to_summarise)

# print(topHitsDictToString(topHitsTupTup, hideScores = False));


# writeTopHitsDictToTxt(bm25ResultsFile, topHitsTupTup,hideScores = True )
# writeTopHitsDictToTxt(bm25ScoredResultsFile, topHitsTupTup,hideScores = False )


