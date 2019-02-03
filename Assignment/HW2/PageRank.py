import time
import math
import operator

# The following code is used to calculate the page rank and number of inlinks of a
# graph built using all the web pages crawled in previous assignment.
# This will be known as graph-1, G1.
# Also 1000 URLs are crawled using Depth First Search method using the same seed URL
# given in previous assignment. These links are converted into a graph using which the
# page rank and inlink count will be calculated. This will be known as graph-2, G2.
# Along with the page rank and inlinks, perplexity and entropy
# of G1 and G2 are also calculated.

def PageRank(filename):

    # Few of the variables that will be used through out the program are
    # defined and assigned here.
    starttime = time.time()
    d = 0.85        # Teleportation factor
    link_list = []  # Initial links list
    sink_link = []  # List of out links
    out_link = {}   # Count of number of out links
    link_det = {}   # Stores each link and list of inlinks for each link
    page_rank = {}
    next_page_rank = {}
    file_handle = open(filename)


# Accessing the graph file stored in the path given by the user.
    for links in file_handle.readlines():
        list_of_links = links.strip('\n').strip(' ').split(' ')
        link_list.extend(list_of_links)
        link_det["".join(list_of_links[0])] = list(set(list_of_links[1:]))
    link_list = list(set(link_list))
    file_handle.close()

# For every link in the link_list the number of outlinks are calculated and a list is
# generated for the outlinks.

    for link in link_list:
        outlinks_list = list(set(link_det.get(link, [])))
        for page in outlinks_list:
            if page not in out_link.keys():
                out_link[page] = 1
            else:
                out_link[page] += 1


    key_count = link_det.keys()
    sink_link = list(set(key_count) - set(out_link.keys()))

# The initial page rank value of all the links present in the link_list is calculated
# and assigned to all pages.
    init_pr = len(link_list)
    for link in link_list:
        page_rank[link] = 1 / init_pr


# Defining variables and assigning initial values to them to calculate the convergence
# of page rank by calculating the entropy value.
    convergence = 0
    convergence_val = 0
    entropy = 0
    for link in page_rank:
        entropy += (page_rank[link] * math.log(page_rank[link], 2))
    convergence_val = 2 ** (entropy * -1)
    count = 0
    while convergence != 4:
        count += 1
        page_rank_sink = 0
        for link in sink_link:
            page_rank_sink = page_rank_sink + page_rank[link]
        for page in link_list:
            pr = (1 - d) / init_pr
            pr += d * (page_rank_sink / init_pr)
            list_of_inlinks = link_det.get(page, [])
            for inlinks in list_of_inlinks:
                pr += ((d * page_rank[inlinks]) / (out_link[inlinks]))
            next_page_rank[page] = pr
        next_entropy = 0
        next_covergence_val = 0
        for link in next_page_rank:
            next_entropy += ( next_page_rank[link] * math.log(next_page_rank[link], 2))
        next_convergence = 2 ** (next_entropy * -1)

# Writing the perplexity values calculated into a file.
        perp_file_handle = open('G1_Perplexity.txt', 'a')
        perp_file_handle.writelines('At round {0} convergence value is {1} \n'.format(count, next_convergence))
        print('At round {0} convergence value is {1} \n'.format(count, next_convergence))

        if(math.fabs(next_convergence - convergence_val)) < 1:
            convergence += 1
        else:
            convergence = 0

        page_rank = next_page_rank
        next_page_rank = {}
        convergence_val = next_convergence
        next_convergence =  0

    print('After round {0} convergence is '.format(count))
    page_rank_sorted = sorted(page_rank.items(), key = operator.itemgetter(1), reverse=True)

    # Writing the sorted top 50 page rank values into a file.
    page_rank_file_handle=open('G1_PageRank.txt', 'a')
    page_rank_file_handle.writelines("Top 50 pages by their Document IDs and Page Ranks \n")
    page_rank_file_handle.writelines("*"*100 + "\n"*3)
    page_rank_file_handle.writelines("Document ID: Page Rank \n")
    for count in range(0,50):
        page_rank_file_handle.writelines(str(page_rank_sorted[count][0])+" : "+str(page_rank_sorted[count][1])+"\n")
    page_rank_file_handle.close()
    process_end_time=time.time()

    count_of_inlinks = {}

    for link in link_list:
        count_of_inlinks[link] = len(link_det.get(link))

    inlink_sorted = sorted(count_of_inlinks.items(),key=operator.itemgetter(1),reverse=True)

    # Writing the sorted top 50 inlink count values into a file.
    inlink_file_handle = open('G1_Inlinks.txt', 'a')
    inlink_file_handle.writelines("Top 50 pages by their Document IDs and Inlinks \n")
    inlink_file_handle.writelines("*" * 100 + "\n" * 3)
    inlink_file_handle.writelines("Document ID: Inlink Count \n")
    for count in range(0,50):
        inlink_file_handle.writelines(
            str(inlink_sorted[count][0]) + " : " + str(inlink_sorted[count][1]) + "\n")
    inlink_file_handle.close()

    # Writing the proportion of pages with no outlinks and proportion of pages
    # with no inlinks into a file.
    prop_file_handle = open('G1_Proportion.txt', 'a')

    zero_inlink = [n for n in link_det.keys() if not link_det[n]]
    prop_file_handle.writelines('Proportion of pages with no inliks: '+str(len(zero_inlink) / init_pr) + '\n')

    zero_outlink = len(sink_link)
    prop_file_handle.writelines('Proportion of pages with no outliks: ' + str((zero_outlink) / init_pr) + '\n')
    print(process_end_time-starttime)
    count = 0
    for link in page_rank:
        if page_rank[link] < (1/init_pr):
            count += 1


# The user is prompted to enter the path which holds the graph file.
def page_rank():
    file_name = input("Enter the path with graph file: ")
    PageRank(file_name)

page_rank()