from os.path import exists
import traceback
import os

rel_dictionary = {}
rank_dictionary = {}
counter = 64
file_list = []


def precision_recall(name, f):
    try:
        PDictionary = {}
        RDictionary = {}
        avg_precision = 0
        no_extension = name[:name.rindex('.')]
        out = open("Output/" + no_extension + '_PrecisionAndRecall.txt', 'w')
        out_avg = open("Output/" + no_extension + "_Avg_Precision.txt", 'w')
        for each in range(1, len(rank_dictionary) + 1):
            qr = str(each)
            avrg_precision = 0
            dcount = 0
            documentFound = 0
            total_precision = 0
            if qr not in rel_dictionary:
                PDictionary[qr] = []
                RDictionary[qr] = []
                out.write('The given query ' + qr + ' has no relevance set. Therefore the precison and recall = 0\n')
                continue
            relevant_document = rel_dictionary[qr]
            relevant_count = len(relevant_document)
            PDictionary[qr] = []
            RDictionary[qr] = []
            for document in rank_dictionary[qr]:
                dcount += 1
                DocID = document.split()[2]
                DocRank = document.split()[3]
                DocScore = document.split()[4]
                flag = False
                for relevant_doc in relevant_document:
                    if DocID == relevant_doc.split()[2]:
                        flag = True
                        break
                if flag:
                    documentFound += 1
                    pr = float(documentFound) / float(dcount)
                    total_precision += pr
                    PDictionary[qr].append({DocID: pr})
                    recall = float(documentFound) / float(relevant_count)
                    RDictionary[qr].append({DocID: recall})
                    out.write(str(qr) + " Q0 " + DocID + " " + str(DocRank) + " " + str(DocScore) + " R " + str(pr) + " " + str(recall) + "\n")
                else:
                    pr = float(documentFound) / float(dcount)
                    PDictionary[qr].append({DocID: pr})
                    recall = float(documentFound) / float(relevant_count)
                    RDictionary[qr].append({DocID: recall})
                    out.write(str(qr) + " Q0 " + DocID + " " + str(DocRank) + " " + str(DocScore) + " NR " + str(pr) + " " + str(recall) + "\n")
            if documentFound != 0:
                avrg_precision += float(total_precision) / float(documentFound)
            else:
                avrg_precision = 0
            out_avg.write(str(qr) + " " + str(avrg_precision) + "\n")
            avg_precision += avrg_precision
        map = float(avg_precision) / float(counter)
        f.write( name.replace(".txt", "") + ": " + str(map) + '\n')
        out_avg.close()
        out.close()
    except:
        print("Try block error")
        print(traceback.format_exc())


def dictionary_construction(file):
    global counter
    if exists("Input/" + file ):
        relevant_file = open('cacm.rel', 'r')
        ranked_file = open("Input/" + file, 'r')
        for lines in relevant_file.readlines():
            qid = lines.split()[0]
            if qid not in rel_dictionary:
                rel_dictionary[qid] = [lines[:-1]]
            else:
                data = rel_dictionary[qid]
                data.append(lines[:-1])
        relevant_file.close()
        for lines in ranked_file.readlines():
            qid = lines.split()[0]
            if qid not in rank_dictionary:
                rank_dictionary[qid] = [lines[:-1]]
            else:
                data = rank_dictionary.get(qid)
                data.append(lines[:-1])
        counter = len(rank_dictionary)
        ranked_file.close()
    else:
        print(file, 'The given file does not exist')


def patk(file):
    try:
        pat5 = {}
        pat20 = {}
        qr_ID = 1
        noextension_file = file[:file.rindex('.')]
        out_pat5 = open("Output/" + noextension_file + "_P@5.txt", 'w')
        out_pat20 = open("Output/" + noextension_file + "_P@20.txt", 'w')
        while qr_ID != counter + 1:
            if not rel_dictionary.get(str(qr_ID)):
                pat5[qr_ID] = 0.0
                pat20[qr_ID] = 0.0
                qr_ID += 1
                continue
            relevant_document_list = rel_dictionary[str(qr_ID)]
            top5 = rank_dictionary[str(qr_ID)][:5]
            top20 = rank_dictionary[str(qr_ID)][:20]
            precision_at5 = 0
            for document in top5:
                docid = document.split()[2]
                for rel in relevant_document_list:
                    if docid == rel.split()[2]:
                        precision_at5 += 1
            pat5[qr_ID] = precision_at5 / 5.0
            out_pat5.write(str(qr_ID) + " " + str(pat5[qr_ID]) + " PK5\n")
            precision_at20 = 0
            for document in top20:
                docid = document.split()[2]
                for rel in relevant_document_list:
                    if docid == rel.split()[2]:
                        precision_at20 += 1
            pat20[qr_ID] = precision_at20 / 20.0
            out_pat20.write(str(qr_ID) + " " + str(pat20[qr_ID]) + " PK20\n")
            qr_ID += 1
        out_pat5.close()
        out_pat20.close()
    except:
        print("Try block error")
        print(traceback.format_exc())


def mrr(file, file_1):
    QID = 1
    RR = 0
    while QID != counter + 1:
        if str(QID) not in rel_dictionary:
            RR += 0
            QID += 1
            continue
        relevant_documents = rel_dictionary[str(QID)]
        ranked_documents = rank_dictionary[str(QID)]
        for document in ranked_documents:
            flag = False
            DocID = document.split()[2]
            for relevant_doc in relevant_documents:
                if DocID == relevant_doc.split()[2]:
                    RR += 1.0 / float(document.split()[3])
                    flag = True
                    break
            if flag:
                break
        QID += 1
    MRR = RR / float(counter)
    file_1.write(file.replace(".txt", "") + ": " + str(MRR) + '\n')


def main():
    global file_list, rank_dictionary, rel_dictionary
    file_list = ["TFIDF_Output.txt", "PRF_BM25.txt", "Lucene_Baseline.txt", "Lucene_Stopped.txt", "bm25Results.txt", "bm25StoppedResults.txt",
                 "SQLMStopped.txt"]
    if not os.path.exists("Output"):
        os.makedirs("Output")
    f = open("Output/MAP.txt", 'w')
    f1 = open("Output/MRR.txt", 'w')
    for item in file_list:
        dictionary_construction(item)
        mrr(item, f1)
        patk(item)
        precision_recall(item, f)
        rank_dictionary = {}
        rel_dictionary = {}
    f.close()
    f1.close()


main()
