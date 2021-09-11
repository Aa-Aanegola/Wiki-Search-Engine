import os
import sys
from cleaner import *
from binsearcher import *

index_dir = sys.argv[1]
search_file = sys.argv[2]

with open(f'{index_dir}/numdocs.txt', 'r') as f:
    num_docs = int(f.read())

cleaner = Cleaner()
searcher = BinSearcher(index_dir, cleaner, num_docs)
searcher.master_search(search_file)