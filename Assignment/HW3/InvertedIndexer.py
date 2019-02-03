import os
import operator

# The following code is used to produce inverted indices for ngrams where n = 1, 2 and 3
# for the corpus generated from task 1.
# This also produces term frequency and document frequency tables for each inverted index
# generated in the previous step.

directory = os.getcwd()
root_path = os.path.join(directory, 'Corpus')

# The following code is used to generate the term frequency table for each ngram.


def generate_next_table(term_sort, n):
    file = open("TF_" + str(n) + "_gram.txt", 'w')
    for term in term_sort:
        file.write(str(term[0]) + ":" + str(term[1]) + "\n" )
    file.close()


# The following code is used to generate the document frequency table for each ngram.


def generate_next_table_2(sorted_document_frequency, n):
    file = open("DF_" + str(n) + "_gram.txt", 'w')
    for term in sorted_document_frequency:
        file.write(str(term[0]) + " " + str(term[1]) + " " + str(len(term[1])) + "\n")
    file.close()


def generate_table(inverted_index, n):
    frequency_dictionary = {}
    document_dictionary = {}
    for a in inverted_index:
        freq = 0
        append_list = []
        for number in inverted_index[a].keys():
            append_list.append(number)
            freq += inverted_index[a][number]
        frequency_dictionary.update({a: freq})
        document_dictionary.update({a: append_list})
    # Sorting the terms
    term_sort = sorted(frequency_dictionary.items(), key=operator.itemgetter(1), reverse=True)
    generate_next_table(term_sort, n)
    # Sorting the documents
    sorted_document_frequency = sorted(document_dictionary.items(), key=operator.itemgetter(0))
    generate_next_table_2(sorted_document_frequency, n)


# Code for generating inverted indices

def ngram_generation(n):
    terms = {}
    inverted_indexer = {}
    files = [id for id in os.listdir(root_path) if id.endswith(".txt")]
    count = 0
    for id in files:
        number = files[count][:-4]
        print(number)
        document = open(os.path.join(root_path, id), 'r').read()
        terms.update({id: len(document.split())})
        term_list = document.split()
        for x in range(len(term_list) - n + 1):
            if n == 2:
                a = term_list[x] + " " + term_list[x + 1]
            elif n == 3:
                a = term_list[x] + " " + term_list[x + 1] + " " + term_list[x + 2]
            else:
                a = term_list[x]
            if a not in inverted_indexer.keys():
                dictionary = {number: 1}
                inverted_indexer.update({a: dictionary})
            elif number not in inverted_indexer[a].keys():
                inverted_indexer[a].update({number: 1})
            else:
                inverted_indexer[a][number] += 1
        count += 1
    print(inverted_indexer)
    file = str(n) + "_gram_inverted_index.txt"
    for y, z in inverted_indexer.items():
        print('Inverted Index', y, ':', z, '\n')
        with open(file, 'a') as out:
            out.write('{0}:{1}\n'.format(y, z))
            out.close()
    generate_table(inverted_indexer, n)


ngram_generation(1)


