from bs4 import BeautifulSoup
from colorama import *
import traceback
from os.path import exists
import os


cwd = os.getcwd()
cacm = os.path.join(cwd, 'cacm')
input_path = os.path.join(cwd, 'LUCENE')


def query_processing():
    try:
        if exists(cwd + "\\intial_query.txt"):
            os.remove(cwd + "\\intial_query.txt")
        given_query = open(cwd + "\\cacm.query", 'r').read()
        file_list = open(cwd + "\\intial_query.txt", 'a')
        while given_query.find('<DOC>') != -1:
            given_query, qry = input_query(given_query)
            if given_query.find('<DOC>') == -1:
                file_list.write(qry)
            else:
                file_list.write(qry+"\n")
    except:
        print("Try block error")
        print(traceback.format_exc())


def input_query(init_query):
    try:
        qr = init_query[init_query.find('</DOCNO>') + 8:init_query.find('</DOC>')]
        qr = qr.strip()
        temp = qr.split()
        qr = " ".join(temp)
        init_query = init_query[init_query.find('</DOC>') + 6:]
        return init_query, qr
    except:
        print("Try block error")
        print(traceback.format_exc())


def snippet_generation(query_input, given_file):
    try:
        print("\nSnippet generation for query" + query_input + "\n")
        qr_term_list = query_input.split()
        if len(qr_term_list) > 2:
            first, qr_term, rem = unigram_snippet(qr_term_list, given_file, 3)
            if first is not False:
                print("**********Document Name:" + given_file + "**********")
                print(first+" "+"\033[31;43m"+qr_term+"\033[m"+" "+rem)
            else:
                first, qr_term, rem = unigram_snippet(qr_term_list, given_file, 2)
                if first is not False:
                    print("**********Document Name:" + given_file + "**********")
                    print(first+" "+"\033[31;43m"+qr_term+"\033[m"+" "+rem)
                else:
                    first, qr_term, rem = unigram_snippet(qr_term_list, given_file, 1)
                    if first is not False:
                        print("**********Document Name:" + given_file + "**********")
                        print(first+" "+"\033[31;43m"+qr_term+"\033[m"+" "+rem)
                    else:
                        print("Given query term not found in " + given_file)
        elif len(qr_term_list) > 1:
            first, qr_term, rem = unigram_snippet(qr_term_list, given_file, 2)
            if first is not False:
                print("**********Document Name:" + given_file + "**********")
                print(first+" "+"\033[31;43m"+qr_term+"\033[m"+" "+rem)
            else:
                first, qr_term, rem = unigram_snippet(qr_term_list, given_file, 1)
                if first is not False:
                    print("**********Document Name:" + given_file + "**********")
                    print(first+" "+"\033[31;43m"+qr_term+"\033[m"+" "+rem)
                else:
                    print("Given query term not found in " + given_file)
        else:
            first, qr_term, rem = unigram_snippet(qr_term_list, given_file, 1)
            if first is not False:
                print("**********Document Name:" + given_file + "**********")
                print(first+" "+"\033[31;43m"+qr_term+"\033[m"+" "+rem)
            else:
                print("Given query term not found in " + given_file)
    except:
        print("Try block error")
        print(traceback.format_exc())


def unigram_snippet(term_list, name, n):
    try:
        look_next = 40
        last = 50
        data = open(cacm + "\\" + name + ".html", 'r').read()
        soup = BeautifulSoup(data, "html.parser")
        soup.prettify().encode("utf-8")
        document_data = soup.find('pre').get_text()
        for i in range(len(term_list) - (n - 1)):
            if n == 3:
                word = term_list[i] + " " + term_list[i + 1] + " " + term_list[i + 2]
            elif n == 2:
                word = term_list[i] + " " + term_list[i + 1]
            else:
                word = term_list[i]
            if document_data.find(word) != -1:
                initial_index = max(document_data.index(word)-look_next, 0)
                if initial_index != 0:
                    while initial_index > 0:
                        if document_data[(initial_index-1):initial_index] not in [" ", "\n"]:
                            initial_index -= 1
                        else:
                            break
                total = document_data.index(word) + len(word) + last
                final_index = min(total, len(document_data))
                if final_index != len(document_data):
                    while final_index < len(document_data):
                        if document_data[final_index:(final_index+1)] not in [" ", "\n"]:
                            final_index += 1
                        else:
                            break
                begg = document_data[initial_index:document_data.index(word)]
                query_part = document_data[document_data.index(word):(document_data.index(word)+len(word))]
                res = document_data[(document_data.index(word)+len(word)):final_index]
                return begg, query_part, res
        return False, False, False
    except:
        print("Try block error")
        print(traceback.format_exc())


def read_lucene(query_id):
    try:
        files = []
        lucene_score = open(input_path + "\\LUCENE_OUTPUT.txt")
        for lines in lucene_score.readlines():
            col = lines.split()
            if col[0] == str(query_id):
                print(col[2])
                files.append(col[2])
        lucene_score.close()
        return files
    except:
        print("Try block error")
        print(traceback.format_exc())


if __name__ == "__main__":
    try:
        init()
        query_processing()
        qID = 0
        initial_query = open('intial_query.txt', 'r')
        for query in initial_query.readlines():
            qID += 1
            print("TOP 100 DOCUMENTS FOR QUERY ID:", qID)
            file_input = read_lucene(qID)
            for file_name in file_input:
                snippet_generation(query, file_name)
    except:
        print("Try block error")
        print(traceback.format_exc())
