import os
import sys
import xml.sax as sx
from parser import Handler
from merger import Merger
import time

dc = sys.argv[1]
parser = sx.make_parser()
handler = Handler()
parser.setContentHandler(handler)

st = time.time()
if not os.path.isdir('./inverted_index'):
    os.mkdir('./inverted_index')
print("Currently parsing...")
parser.parse(dc)
stat = open('./invertedindex_stat.txt', "w")
word_count = str(handler.get_word_count()) + '\n'
stat.write(word_count)
stat.close()
print('\nCurrently merging...')
merger = Merger(6, sys.argv[2])
merger.create_index()
print(f"\nTotal time taken: {time.time() - st}")