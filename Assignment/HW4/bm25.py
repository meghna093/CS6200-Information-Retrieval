import math
import glob
import traceback
import os

# variable to store document dictionary and its corresponding term frequency
document_dictionary = {}

# variable to store document name dictionary and its corresponding document ID
token = {}

# generates inverted index for unigram
def generate_unigram():
    inverted_index = {}
    document_id = 0
    # try block
    try:
        # reading from corpus folder
        for filename in glob.glob(os.path.join('corpus', '*.txt')):
            with open(filename) as f:
                document_id += 1
                document = f.read()
                keys = str(filename).split('corpus/')[0][:-4]
                print("Index for " + keys)
                token[keys] = len(document.split())
                document_dictionary.update({keys: document_id})
                # creating a dictionary structure for inverted index
                for word in document.split():
                    if word not in inverted_index:
                        documents_dictionary = {keys: 1}
                        inverted_index[word] = documents_dictionary
                    elif keys in inverted_index[word]:
                        documents_dictionary = inverted_index[word]
                        val = documents_dictionary.get(keys)
                        val += 1
                        documents_dictionary[keys] = val
                    else:
                        documents_dictionary = {keys: 1}
                        inverted_index[word].update(documents_dictionary)
            f.close()
    # catch block
    except:
        print("Unigram generation error")
        print(traceback.format_exc())

    return inverted_index


# code to print the ranked list into a file in the given display format
def inverted_index_ranking(inverted_index):
    query_file = open('query_file.txt', 'r')

    for line in query_file.readlines():
        qlist = line.split(' ')
        qid = qlist[0]
        qstring = ' '.join(qlist[0:])[:-1].lower()
        print('Given query: ' + qstring)
        print('Generating ranked list')
        sorted_documents = bm25(qstring, inverted_index)

        if len(sorted_documents) == 0:
            print('Matching document not found')
        else:
            print('Printing ranked list')
            document_file = open('BM25_document_list.txt', 'a')
            for score in range(min(len(sorted_documents), 100)):
                rank = score + 1
                document_file.write(str(qid) + ' Q0 ' + str(sorted_documents[score][0]) + ' ' + str(rank) + ' ' + str(sorted_documents[score][1]) + ' BM25 ' + '\n')
            document_file.close()


# code to calculate bm25 score
def bm25(query, inverted_index):
    dictionary_score = {}
    dictionary_term = {}
    k1 = 1.2
    k2 = 100
    b = 0.75
    avdl = sum(token.values()) / float(1000)
    terms = query.split(' ')
    for term in terms:
        if term in dictionary_term:
            dictionary_term[term] += 1
        else:
            dictionary_term[term] = 1

    for document in token:
        dl = token[document]
        K = k1 * ((1 - b) + (b *(dl / avdl)))
        count = 0
        for term in dictionary_term:
            query_frequency = dictionary_term[term]
            x = len(inverted_index[term])
            document_dictionary = inverted_index[term]
            if document in document_dictionary:
                frequency = document_dictionary[document]
            else:
                frequency = 0
            temp_var1 = math.log10((1000 - x + 0.5) / (x + 0.5))
            temp_var2 = (((k1 + 1) * frequency) / (K + frequency))
            temp_var3 = (((k2 + 1) * query_frequency) / (k2 + query_frequency))
            count += temp_var1 * temp_var2 * temp_var3
        dictionary_score[document] = count
    sorted_documents = sorted(dictionary_score.items(), key=lambda x: x[1], reverse=True)
    return sorted_documents


# main function
def main():
    print("Generating Inverted Index")
    inverted_index = generate_unigram()
    inverted_index_ranking(inverted_index)


main()








