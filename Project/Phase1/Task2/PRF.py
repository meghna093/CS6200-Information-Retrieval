from bs4 import BeautifulSoup
from nltk import ngrams
import os
import re
import traceback
import glob
import math


unigram = []
indexer = {}
tf = {}
ind_list = {}
qr_list = {}
dlist = []
tfidf_count = {}
bm25_score = {}
dlength = {}
stopwords = []
file_list = []
dir = 'cacm'
corpus_length = 0


def call_jobs():
    global tfidf_count, dlength, qr_list, bm25_score, stopwords
    qr_list = read_query()
    final_length = 0
    dlength = {}
    for item in ind_list:
        for one in ind_list[item]:
            final_length += one[1]
            if (one[0]) in dlength:
                dlength[one[0]] += one[1]
            else:
                dlength[one[0]] = one[1]
    x = len(dlength)
    print("Pseudo Relevance Feedback\n")
    for query_id in qr_list:
        print("BM25 score for query:", query_id)
        for each_document in dlist:
            bm25_score[each_document] = 0.0
        bm25_score = bm25(ind_list, query_id, qr_list[query_id], {}, dlength, final_length, bm25_score, [])
        sorted_bm25 = sorted(bm25_score.items(), key=lambda z: z[1], reverse=True)
        high_tf = get_high_tf(sorted_bm25[:10], stopwords)
        print(qr_list[query_id])
        # print(high_tf)
        for each in high_tf:
            qr_list[query_id].append(each)
        print(qr_list[query_id])
        for each_document in dlist:
            bm25_score[each_document] = 0.0
       # print(bm25_score[each_document])
        bm25_score = bm25(ind_list, query_id, qr_list[query_id], {}, dlength, final_length, bm25_score, [])
        sorted_bm25 = sorted(bm25_score.items(), key=lambda z: z[1], reverse=True)
        write_file_prf(query_id, sorted_bm25[:100], "PRF_BM25", "bm25")


def write_file_prf(query_id, val, name, alg_name):
    if not os.path.exists("Phase1"):
        os.makedirs("Phase1")
    ranking = 1
    for item in val:
        document = str(item[0])[:len(item[0])-4]
        if query_id == 1 and ranking == 1:
            with open("Phase1/" + name + ".txt", 'w') as f:
                f.write(str(query_id) + " Q0 " + document + " " + str(ranking) + " " + str(item[1]) + " " +
                        alg_name + "\n")
        else:
            with open("Phase1/" + name + ".txt", 'a') as f:
                f.write(str(query_id) + " Q0 " + document + " " + str(ranking) + " " + str(item[1]) + " " +
                        alg_name + "\n")
        ranking += 1


def stop_words():
    stopwords_list = []
    for item in open('common_words', 'r').readlines():
        stopwords_list.append(item.strip("\n"))
    return stopwords_list


def read_query():
    query = {}
    counter = 1
    query_text = open('cacm.query.txt', 'r')
    q_soup = BeautifulSoup(query_text, 'html.parser')
    q_soup.prettify().encode('utf-8')
    for text in q_soup.findAll('docno'):
        text.extract()
    for text in q_soup.findAll('doc'):
        qr = text.get_text().strip(' \n\t')
        qr = str(qr)
        qr = qr.lower()
        qr = transformation(qr)
        write_query_file(counter, qr)
        query[counter] = qr.split(" ")
        counter += 1
    return query


def write_query_file(query_id, queries):
    if query_id == 1:
        with open("query.txt", 'w') as f:
            f.write(str(query_id) + " " + queries + "\n")
    else:
        with open("query.txt", 'a') as f:
            f.write(str(query_id) + " " + queries + "\n")


def get_high_tf(count, stop_words):
    unigrams = []
    tf = {}
    final = []
    for item in count:
        for each in ngrams((open("cacm/" + str(item[0]), 'r').read()).split(), 1):
            unigrams.append(each[0])
    for item in unigrams:
        if item in tf:
            tf[item] += 1
        else:
            tf[item] = 1
    sorted_tf = sorted(tf.items(), key=lambda x : x[1], reverse=True)
    for each in sorted_tf:
        if each[0] not in stop_words:
            final.append(each[0])
    return final[:5]


def transformation(data):
    data = re.sub(r'[@_!\s^&*?#=+$~%:;\\/|<>(){}[\]"\']', ' ', data)
    term_list = []
    for term in data.split():
        term_len = len(term)
        if term[term_len - 1:term_len] == '-' \
                or term[term_len - 1:term_len] == ',' \
                or term[term_len - 1:term_len] == '.':
            term = term[:term_len - 1]
            term_list.append(handle_punctuation(term))
        else:
            term_list.append(handle_punctuation(term))
    term_list = [x for x in term_list if x != '']
    term_list = " ".join(term_list)
    if ' PM ' in term_list or 'PM ' in term_list or 'PMB ' in term_list:
        term_list_proc = term_list.split('PM')[0]
        term_list_proc += " pm"
        return term_list_proc
    elif ' AM ' in term_list or 'AM ' in term_list:
        term_list_proc = term_list.split('AM')[0]
        term_list_proc += " am"
        return term_list_proc
    else:
        return term_list


def handle_punctuation(term):
    while term[:1] == "-" or term[:1] == "," or term[:1] == ".":
        if re.match(r'^[\-]?[0-9]*\.?[0-9]+$', term):
            return term
        if term[:1] == "-" or term[:1] == "." or term[:1] == ",":
            term = term[1:]
        else:
            return term
    return term


def fetch_data():
    try:
        counter = 1
        for filename in glob.glob(os.path.join('*.html')):
            with open(filename) as f:
                article = filename.strip('cacm/').strip('.html')
                data = f.read()
                counter += 1
                soup = BeautifulSoup(data, 'html.parser')
                soup.prettify().encode('utf-8')
                text = soup.find('text').get_text().encode('utf-8')
                content = text
                processed_data = transformation(content)
                processed_data = processed_data.lower()
                write_file_corpus(processed_data, article)
                f.close()
    except:
        print("Try block error")
        print(traceback.format_exc())


def write_file_corpus(data, file_name):
    try:
        if not os.path.exists(dir):
            os.makedirs(dir)
        index_terms = open(dir + '/' + file_name + '.txt', 'w')
        index_terms.write(data)
        index_terms.close()
    except:
        print("Try block error")
        print(traceback.format_exc())


def generate_index(files, gram):
    temp = gram
    for item in gram:
        if item in indexer:
            for one in indexer[item]:
                equal = 1
                if files == one[0]:
                    equal *= 0
                else:
                    equal *= 1
            if equal == 1:
                indexer[item] += [[files,counter(item,temp)]]
        else:
            indexer[item] = [[files, counter(item,temp)]]


def counter(term, grams):
    total = 0
    for items in grams:
        if term == items:
            total += 1
    return total


def index_creation(dir):
    global unigram, indexer
    indexer = {}
    for file in os.listdir(dir):
        if ".DS_Store" not in file:
            for item in ngrams((open(dir + file, 'r').read()).split(),1):
                unigram.append(item[0])
            generate_index(file, unigram)
            unigram = []
    return indexer


def bm25(ind_list, query_id, qr_list, relevance, dlength, final_length, bm25_score, stopwords):
    global corpus_length
    corpus_length = final_length
    already_cal = []
    for word in qr_list:
        if word not in stopwords and word not in already_cal and word in ind_list:
            already_cal.append( word )
            qfi = getqfi( word, qr_list )
            if len( relevance ) == 0:
                ri = 0
                for i in range( 0, len( ind_list[word] ), 1 ):
                    bm25_score[ind_list[word][i][0]] += getbm25( ind_list[word][i][1], len( ind_list[word] ),
                                                                 dlength[ind_list[word][i][0]], qfi, 0, ri )
            else:
                ri = get_ri( relevance[str( query_id )], ind_list[word] )
                for i in range( 0, len( ind_list[word] ), 1 ):
                    bm25_score[ind_list[word][i][0]] += getbm25( ind_list[word][i][1], len( ind_list[word] ),
                                                                 dlength[ind_list[word][i][0]], qfi,
                                                                 len( relevance[str( query_id )] ), ri )

    return bm25_score


def get_ri(relevant_docs, docs_with_term):
    ri = 0
    for items in docs_with_term:
        if items[0] in relevant_docs:
            ri += 1
    return ri


def getqfi(term, queries):
    count = 0
    for words in queries:
        if term == words:
            count += 1
    return count


def getbm25(fi, ni, dl, qfi, r, ri):
    total_docs = 3204
    avg_doc_len = float( corpus_length ) / total_docs
    k1 = 1.2
    b = 0.75
    k2 = 100
    num = float(ri + 0.5 ) / (r - ri + 0.5)
    den = float(ni - ri + 0.5 ) / (total_docs - ni - r + ri + 0.5)
    task1 = (math.log( float( num ) / den ))
    task2 = ((fi * (k1 + 1)) / (fi + (k1 * ((1 - b) + (b * (dl / avg_doc_len))))))
    task3 = ((qfi * (k2 + 1)) / (qfi + k2))
    result = task1 * task2 * task3
    return result


def main():
    global ind_list, dlist, bm25_score, stopwords
    print("Corpus Generation")
    fetch_data()
    print("Indexer")
    ind_list = index_creation("cacm/")
    for one in ind_list:
        for item in ind_list[one]:
            if item[0] not in dlist:
                dlist.append(item[0])
    stopwords = stop_words()
    call_jobs()


main()
