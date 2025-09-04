import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # raise NotImplementedError
    all_pages=set(corpus.keys())



    if len(corpus[page])==0:
        pages_link=all_pages

    else:
        pages_link=corpus[page]


    result={}

    for target_page in all_pages:
        probability=0

        probability+=(1-damping_factor)/len(all_pages)

        if target_page in pages_link:
            probability+=(damping_factor)/len(pages_link)

        result[target_page]=probability

    return result


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # raise NotImplementedError
    pages_count={page:0 for page in corpus.keys()}

    current_page=random.choice(list(corpus.keys()))

    pages_count[current_page]+=1

    for i in range(n-1):
        probability_dict=transition_model(corpus,current_page,damping_factor)

        next_page=random.choices(
            list(probability_dict.keys()),
            weights=list(probability_dict.values())
        )[0]

        current_page=next_page
        pages_count[next_page]+=1

    for page in pages_count.keys():
        pages_count[page]=pages_count[page]/n

    return pages_count

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # raise NotImplementedError
    all_pages=set(corpus.keys())
    
    N=len(corpus)

    pagerank={}

    for page in all_pages:
        pagerank[page]=1/N

    converged=False

    while not converged:
        new_pagerank={}

        for page in all_pages:

            incoming_rank=0

            for other_pages in all_pages:
                if len(corpus[other_pages])==0:
                    incoming_rank+=pagerank[other_pages]/N

                elif page in corpus[other_pages]:
                    outgoing_links=len(corpus[other_pages])
                    incoming_rank+=pagerank[other_pages]/outgoing_links 

            new_pagerank[page]=(1-damping_factor)/N+damping_factor*incoming_rank

        
        converged=True

        for page in all_pages:
            if abs(new_pagerank[page]-pagerank[page])>0.001:
                converged=False
                break

        pagerank=new_pagerank

    return pagerank

if __name__ == "__main__":
    main()
