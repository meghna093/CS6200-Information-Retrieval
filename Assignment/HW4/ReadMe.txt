INFORMATION RETRIEVAL - HW4

########################################################################################

Language used : Java 8 for Task1 
		python 3.4.6 for Task2
				

The following libraries needs to be installed to run the code successfully:

For Task1:
	-> lucene-core-7.1.0.jar
	-> lucene-queryparser-7.1.0.jar
	-> lucene-analyzers-common-7.1.0.jar
	
For Task2:
	-> math
	-> traceback
	-> glob
	-> os

########################################################################################
Steps to run the program:

(Note: The corpus has text files named from 1 to 1000 to avoid duplicate names. For the corresponding name of the document for the displayed document ID please refer KeyValueMapping.txt)

Task1:

Task1 consists of Lucene implementation. It cannot be run using command prompt.
This code can be run using eclipse tool. Before running the code the above mentioned libraries should be imported.
Also the design of this code expects a query file which consists of all the given queries to be present in the same directory as the code.

This program produces the following text file:
	-> Lucene_document_list_tables.txt

The output for all the 9 queries are generated in the same file. It is then manually divided into 9 tables, each containing 100 document IDs ranked by scores. The following tables can be found within Lucene_document_list folder,
	-> query1_hurricane_isabel_damage
	-> query2_forecast_models
	-> query3_green_energy_canada
	-> query4_heavy_rains
	-> query5_hurricane_music_lyrics
	-> query6_accumulated_snow
	-> query7_snow_accumulation
	-> query8_massive_blizzards_blizzard
	-> query9_new_york_city_subway
	
(Note: Each text file for each query)

Task2:
Running the program through command prompt: python3.6 bm25.py

It generates the unigrams from the corpus generated from third assignment. Then based on the BM25 score it ranks the list of documents.

This program produces the following text file:
	-> BM25_document_list_tables.txt

The output for all the 9 queries are generated in the same file. It is then manually divided into 9 tables, each containing 100 document IDs ranked by scores. The following tables can be found within BM25_document_list folder,
	-> query1_hurricane_isabel_damage
	-> query2_forecast_models
	-> query3_green_energy_canada
	-> query4_heavy_rains
	-> query5_hurricane_music_lyrics
	-> query6_accumulated_snow
	-> query7_snow_accumulation
	-> query8_massive_blizzards_blizzard
	-> query9_new_york_city_subway
	
(Note: Each text file for each query)

########################################################################################

The following resources were used to off the internet to develop this program
	-> https://nlp.stanford.edu/IR-book/html/htmledition/a-first-take-at-building-              an-inverted-index-1.html
	-> https://blackboard.neu.edu/bbcswebdav/pid-15032873-dt-content-rid-                       24244906_1/courses/CS6200.15344.201810/HW4.java

########################################################################################