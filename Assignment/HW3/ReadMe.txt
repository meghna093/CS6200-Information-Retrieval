INFORMATION RETRIEVAL - HW3

##############################################################################

Language used : python 3.4.6

The following libraries needs to be installed to run the code successfully:
	-> urlopen
	-> urlretrieve
	-> BeautifulSoup
	-> string
	-> re
	-> operator
	-> os


##############################################################################

There are three parts in this assignment

Task1->Generating the corpus
	a) Using the 1000 URLs crawled in the first assignment generate a corpus.
	   
Task2->Implementing an inverted indexer and creating inverted indexes
	a) Implementing a simple inverted indexer using the corpus in Task1 as 	
	   input and produce inverted indices as output for ngrams where n = 1,2 and 3.
   
Task3->Corpus statistics
	a) Generating a term frequency table using inverted indices from Task2.
	b) Generating a document frequency table using inverted indices from Task2.
	c) Deducing a stop list using unigram data from Task2.
	d) Assigning a cutoff value for stop words and justification for the same.
   
##############################################################################

Steps to run the program:

Task1:
Running the program through command prompt: python3.6 CorpusGeneration.py

Using the 1000 URLs crawled in the first assignment the program will generate a corpus with 1000 files corresponding to 1000 URLs. The files are named using numbers ranging from 1 to 1000 to avoid duplicate names.

The corresponding URL name of the text files in corpus can be found in KeyValueMapping.txt


Task2 and Task3:
Running the program through command prompt: python3.6 InvertedIndexer.py

The user will not be prompted for any inputs. The value for ngram will be passed with in the program. For unigram data the program will be passed with value 1.
The same way for bigram and trigram program will be passed with values 2 and 3 respectively. The program should be executed 3 times, each time for each ngram.
Task2 and Task3 are combined into same program.
This program uses the corpus generated in Task1 and produces inverted indices for ngrams where n = 1,2 and 3.
These inverted indices are used to produce term frequency tables and document frequency tables for each ngram that is unigram, bigram and trigram.

Based on the unigram data a list of stop words is deduced and a cutoff frequency for stop words is selected.

This program produces the following files:
Part of Task2:
	->1_gram_inverted_index
	->2_gram_inverted_index
	->3_gram_inverted_index

Part of Task3:
	->DF_1_gram
	->DF_2_gram
	->DF_3_gram
	->TF_1_gram
	->TF_2_gram
	->TF_3_gram


##############################################################################

The following resources were used to off the internet to develop this program
	-> https://stackoverflow.com/questions/28019543/inverted-index-given-a-list-of-             document-tokens-using-python
	-> https://queryunderstanding.com/tokenization-c8cdd6aef7ff#.syx2pp8lm
	-> https://nlp.stanford.edu/IR-book/html/htmledition/a-first-take-at-building-              an-inverted-index-1.html

##############################################################################

