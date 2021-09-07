import os
import sys
import xml.sax as sx
from parser import Handler
from merger import Merger
import time

dc = sys.argv[1]
parser = sx.make_parser()
handler = Handler(sys.argv[2])
parser.setContentHandler(handler)

st = time.time()
if not os.path.isdir(f'{sys.argv[2]}'):
    os.mkdir(f'{sys.argv[2]}')
print("Currently parsing...")
parser.parse(dc)
print('\nCurrently merging...')
merger = Merger(6, sys.argv[2])
merger.create_index()
print(f"\nTotal time taken: {time.time() - st}")