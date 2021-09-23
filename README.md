# Wiki-Search-Engine
**A python based implementation of an indexer and search engine intended to be used in tandem with wikipedia dumps.**

## The indexer
The indexer creates an inverted index for the wikipedia dump provided. The xml file is parsed using the sax parser for which I created a custom content handler. The indexer takes around 11 hours to parse, merge and resplit an 80GB wikipedia dump, which is remarkably fast.
The inverted index is composed of a posting list of the form ```<token> <posting-0> <posting-1> ... <posting-n>``` where ```posting: docIDt<title-freq>b<body-freq>i<infobox-freq>c<categories-freq>r<references-freq>l<links-freq>``` as well as a list of all document titles for easy retrieval. 
To facilitate queries over individual parts of the wikipedia document (for example, search for Dwayne Johnson in the title and Scorpion King in the body) each posting had to have the frequencies of the tokens in each of the parts of the wikipedia document. In order to reduce the space that the inverted index takes on the disk, I've used hex encoding for the docIDs and frequencies. 

### How it works
The sax content handler reads each wikipedia page, cleans it (this involves removing special characters, removing stopwords, stemming etc.), converts it into a postings list and adds it to the inverted index. To ensure that the program doesn't run out of memory, this partial inverted index is dumped to a file every 50,000 documents and is reset. During this process, the list of titles of each of the documents is also stored and dumped to a file every 50,000 documents read.
After the parser runs its course, and the partial inverted indices are created, the merger kicks in and performs a binary merge (concatenates posting lists for the same tokens in two files, over the course of this process the inverted index is always sorted by token) in order to create one large inverted index that contains all the tokens and posting lists. Since reading such a large file into memory may not be feasible, the large inverted index is once again chunked into smaller indices of 100,000 tokens, and a list of the last token in each of the files is also stored in a file to facilitate quick lookup. 
If there were 350,000 pages in the wikipedia dump, then 7 individual inverted indices would be created. The binary merge would look like the following
```7 - 4 - 2 - 1``` where the numbers represent the number of files at each stage of the merge (think of a binary tree being constructed from the leaf nodes). 

### File structure
- ```index.sh```   - A bash script that simply allows you to run the indexer. Pass in the path to the wikipedia dump and the path to the inverted index directory to run the script. 
- ```indexer.py``` - The main python script that handles the parsing and file merging. 
- ```cleaner.py``` - Contains a class that performs the clean and chunk operation on the wikipedia pages. Cleaning involves removing special characters, removing stopwords and stemming while chunking refers to dividing the document into the 6 parts of a wikipedia page (title, body, infobox, categories, references, links). 
- ```parser.py```  - Contains the sax content handler that parses each individual page in the wikipedia document and adds it to the inverted index. 
- ```merger.py```  - Contains a class that performs the merge operation on all the individual inverted indices as well as split the index into chunks of 100,000 tokens each. 
- ```boa.py```     - Boa is a novel method (later found to be similar to the 'champion index' concept) that I came up with in order to decrease search times and reduce the index size. Instead of storing very large posting lists for every token, the size of the index for each token is restricted to a maximum of 60,000 (10,000 for each part of the page). This ensures fast lookup, and marginal reduction in query result relevance. 

## The searcher
The searcher searches the inverted index for the query terms and returns relevant titles. It works on binary search and tf-idf computations and returns results within 3 seconds for most queries. 

### How it works
The query string can be of the form 
```t:<word> b:<word> ...``` or simply ```<word> <word>```, the major distinction being that if a search parameter is specified ```{t, b, i, c, r, l}``` then only documents with the token in that part of the wikipedia document will be considered when returning results. To use the searcher, a file with queries on distinct lines must be created and passed to the searcher as an argument.
Each of the above cases can be reduced to the search for a single token, for example let's take Anakin. To find this token in the inverted index, the searcher will try to find which file Anakin may be in using the list of all the end words created during index creation, and open the right file. Once the right file is opened, binary search is done over all the tokens in the file and if the token is found its posting list is returned. 
With the posting list, a tf-idf computation is applied and this value is added to a dictionary that maps docID's to their total tf-idf scores (since there can be multiple tokens in the search query, the total tf-idf value is of relevance instead of individual scores for each token). 
To solve the issue of hyper-relevance (when one document is very relevant to one token in the search query, but may not be very relevant to the other tokens), I came up with a smart way to weight the query results by simply adding a large constant to the total tf-idf values in case the token is present in the document. This ensures that if more tokens from the search query are present in the document, the document will automagically rank higher in our relevance scoring system. Once this ranking for all the tokens in the query string is complete, the top 10 document titles (based on tf-idf values) are dumped into an output file along with the time that it took for the query to execute.

### File structure
- ```search.sh```      - A bash script that helps you use the searcher. Pass in the path to the inverted index directory as well as the file path that contains the search query strings to run the script.
- ```searcher.sh```    - The main python script that handles the searching. 
- ```cleaner.py```     - A subset of the previous cleaner & chunker, only performs the clean operation on the query tokens. 
- ```binsearcher.sh``` - Contains the class that applies the binary search algorithm, performs tf-idf computation and dumps results to the file. 
