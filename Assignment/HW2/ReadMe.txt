INFORMATION RETRIEVAL - HW2

##############################################################################

Language used : python 3.4.6

The following libraries needs to be installed to run the code successfully:
	-> math
	-> time
	-> operator

##############################################################################

There are three parts in this assignment

1) Build a directed graph of URLs
	a) Use the 1000 URLs crawled in the previous assignment and build a    
	   direct graph. This will be known as G1.
	b) Crawl 1000 URLs using a depth first search based crawler and using 
	   these 1000 URLs build a directed graph. This will be known as G2. 
	   
2) Implement a Page Rank algorithm and calculate the page ranks of G1 and G2.
   Also calculate the entropy and perplexity values of the page ranks.
   
3) Qualitative analysis of top 10 pages by page rank and top 10 pages by    
   in-links for G1 and G2.
   
##############################################################################

Steps to run the program:

Running the program through command prompt: python3.6 PageRank.py

User will be prompted to enter the path that has the graph file.
Enter the file path.

The program will give a list of top 50 web pages along with its page rank and in-link count in a sorted order.
It will also provide perplexity of the page ranks.

Page rank of top 50 web pages of G1 can be found in file    : G1_PageRank
In-link count of top 50 web pages of G1 can be found in file: G1_Inlinks
Perplexity of page ranks of G1 can be found in file         : G1_Perplexity

Page rank of top 50 web pages of G2 can be found in file    : G2_PageRank
In-link count of top 50 web pages of G1 can be found in file: G2_Inlinks
Perplexity of page ranks of G2 can be found in file         : G2_Perplexity

##############################################################################

The following resources were used to off the internet to develop this program
	-> https://www.youtube.com/watch?v=-uR7BSfNJko
	-> https://www.youtube.com/watch?v=QVcsSaGeSH0
	-> https://docs.python.org/3.2/install/
	-> http://programminghistorian.github.io/ph-submissions/lessons/published/exploring-and-analyzing-network-data-                with-python

##############################################################################

