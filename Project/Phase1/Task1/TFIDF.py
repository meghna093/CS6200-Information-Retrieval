from bs4 import BeautifulSoup
from nltk import ngrams
import math
import os
import re
import traceback
import glob

dlist = []
tfidf_count = {}
dlength = {}
ind_list = {}
qr_list = {}
file_list = []
dir = 'cacm'
unigram = []
indexer = {}
tf = {}


def call_jobs():
    global tfidf_count, dlength, qr_list
    qr_list = read_query()
    final_length = 0
    dlength = {}
    for item in ind_list:
        for one in ind_list[item]:
            final_length += one[1]
            if (one[0])in dlength:
                dlength[one[0]] += one[1]
            else:
                dlength[one[0]] = one[1]
    x = len(dlength)
    for query_id in qr_list:
        print("TFIDF Score", query_id)
        for each_document in dlist:
            tfidf_count[each_document] = 0.0
        tfidf_count = tfidf(ind_list, qr_list[query_id], x, dlength, tfidf_count)
        tfidf_score = sorted(tfidf_count.items(), key=lambda a : a[1], reverse=True)
        write_file_tfidf(query_id, tfidf_score[:100], "TFIDF_Output", "tfidf")


def tfidf(index, query, n, doc_length, score):
    for word in query:
        if word in index:
            ni = len(index[word])
            idf = math.log10(float(n) / ni)
            for item in index[word]:
                tf = float(item[1]) / doc_length[item[0]]
                if (item[0]) in score:
                    score[item[0]] += tf * idf
                else:
                    score[item[0]] = tf * idf
    return score


def write_file_tfidf(query_id, val, name, alg_name):
    if not os.path.exists("Phase1"):
        os.makedirs("Phase1")
    ranking = 1
    for item in val:
        document = str(item[0])[:len(item[0])-5]
        if query_id == 1 and ranking == 1:
            with open("Phase1/" + name + ".txt", 'w') as f:
                f.write(str(query_id) + " Q0 " + document + " " + str(ranking) + " " + str(item[1]) + " " +
                        alg_name + "\n")
        else:
            with open("Phase1/" + name + ".txt", 'a') as f:
                f.write(str(query_id) + " Q0 " + document + " " + str(ranking) + " " + str(item[1]) + " " +
                        alg_name + "\n")
        ranking += 1


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
            indexer[item] = [[files,counter(item,temp)]]


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


def main():
    global ind_list, dlist
    print("Corpus Generation")
    fetch_data()
    print("Indexer")
    ind_list = index_creation("cacm/")
    for one in ind_list:
        for item in ind_list[one]:
            if item[0] not in dlist:
                dlist.append(item[0])
    call_jobs()


main()
