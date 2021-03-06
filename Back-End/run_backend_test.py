from crawler import crawler
from pagerank import page_rank

# Get crawler object and crawl on urls found in urls.txt
crawler = crawler(None, 'urls.txt')
crawler.crawl()

document_index = crawler.get_document_index()

# Run pagerank on the links generated by the crawler
pagerank = page_rank(crawler._links)

for doc_id, rank in sorted(pagerank.iteritems(), key=lambda (k,v): (v,k), reverse=True):
    document = crawler._document_index[doc_id]
    print str(rank) + " : " + str(document[0]) + "\n"
