#This code is used to crawl wikipedia web pages

#The given seed is 'https://en.wikipedia.org/wiki/Tropical_cyclone'

#For problem statment please refer the below link:
#https://blackboard.neu.edu/bbcswebdav/pid-14487715-dt-content-rid-23461007_1/courses/CS6200.15344.201810/hw1.pdf

#Coded by Meghna Venkatesha


#libraries required for regular expression and web requests
from bs4 import BeautifulSoup
import urllib.request
import re
import time


#FUNCTION : wiki_crawler(link, key_phrase)
#GIVEN : A seed to crawl the web pages of wikipedia with or without a key word
#RETURNS : List of wikipedia web pages
#          if key word is given then focused crawl if not general crawl


key = "\b[Rr][Aa][Ii][Nn]?"
def wiki_crawler(link, key_phrase= key):
   tp_links = []
   source_code = urllib.request.urlopen(link).read()

   links_list = re.findall(r'<a href="/wiki/.*?"', str(source_code))
   for link in links_list:
       if (re.search("[:#]", link) or link is "/wiki/Main_Page"):
           continue
       else:
           tp_links.append("https://en.wikipedia.org" + link[9:len(link) - 1])
   # tp_links=list(set(tp_links))
   tp_links1 = []
   for link in tp_links:
       if (link not in tp_links1):
           tp_links1.append(link)

   return tp_links1


#FUNCTION : key_match(link, key_phrase, depth)
#GIVEN : key word using which focused crawling is carried out
#RETURNS : focused list of links to web pages that consists of the given key word
#          if key word is not found, returns false

def key_match(link, key_phrase, depth):
   if ((key_phrase is key) or (depth == 1)):
       return True
   else:
       source_code = urllib.request.urlopen(link).read()
       soup = BeautifulSoup(source_code, "html.parser")
       [links.extract() for links in soup(['style', 'script', '[document]'])]
       text_content = soup.getText()
       if (text_content.lower().find(key_phrase.lower()) >= 0):
           return True
       else:
           return False


#FUNCTION : main()
#GIVEN : main() does not accept any input
#RETURNS : List of links to the crawled web pages

def main():
   seed_url = "https://en.wikipedia.org/wiki/Tropical_cyclone"
   depth_list = [seed_url]
   res_list = []
   depth = 1
   temp_list = []
   link_pool = []
   rel_list = []


   #Asking the user whether they want to do a focused crawl with a key word
   answer = input("Crawl using a key word?[y/n]")


   #If the user wants to crawl with the key word
   if (answer.lower()[0] is 'y'):
       key_phrase= "rain"
       print("Crawling with key word " + key_phrase)
   #If user wishes to crawl without the key word
   else:
       key_phrase = key
       print("Crawling without a key word")


   if (key_phrase.replace(" ", "") is ""):
       key_phrase = key

   depth_count = 0

   #Crawling until depth 6
   while (depth <= 6):
       print("Crawling started at depth " + str(depth))
       for link in depth_list:
           temp_list = wiki_crawler(link, key_phrase)
           time.sleep(1)

           if (link not in res_list and key_phrase is key):
               res_list.append(link)

           # Crawling limited to most 1000 links
           if (len(res_list) >= 10):
               break;

           for link in temp_list:

               if (
                   link is not 'en.wikipedia.org/wiki/Main_Page' and link not in res_list and link not in link_pool):
                   depth_count = depth_count + 1
                   if (key_match(link, key_phrase, depth + 1)):
                       rel_list.append(link)
                       link_pool.append(link)
                       if (key_phrase is not key):
                           res_list.append(link)
               if (depth_count >= 10 and key_phrase is not key):
                   for link in depth_list:
                       if (link not in res_list):
                           res_list.append(link)
                   break;
       if (len(res_list) >= 10):
           break;
       if (depth_count >= 10 and key_phrase is not key):
           break;
       depth_list = link_pool
       link_pool = []

       #Crawling limited to most 1000 links
       if (len(res_list) >= 10):
           break
       depth += 1

   #Printing the list of links of web pages
   for link in res_list:
       print(link)

#Call to the main()
main()

