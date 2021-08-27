import os
import sys
from cleaner import *
from binsearcher import *

index_dir = sys.argv[1]
search_str = sys.argv[2]

cleaner = Cleaner()
searcher = BinSearcher(index_dir, cleaner)
searcher.search(search_str)