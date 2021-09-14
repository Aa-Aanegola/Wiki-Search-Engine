import time
import xml.sax as sx
from cleaner import *
from memory_profiler import profile
from collections import defaultdict

class Handler(sx.ContentHandler):
    def __init__(self, index_dir):
        self.title = []
        self.body = []
        self.current = ''
        self.id = None
        self.cleaner = CleanerChunker()
        self.pages = 0
        self.index_dir = index_dir
        self.titles = []
        self.keys = ['T', 'I', 'B', 'C', 'R', 'L']
        self.inv_index = defaultdict(list)
        
    def add_page(self, page=None, force_write=False):
        if page:
            c = 0
            ind = defaultdict()
            words = set()
            for key in page.keys():
                temp = defaultdict(int)
                has = defaultdict(int)
                for word in page[key]:
                    flag = False
                    if len(word) > 15:
                        flag = True
                    for letter in word:
                        has[letter] += 1
                    for key in has.keys():
                        if has[key] > 5:
                            flag = True
                    has.clear()
                    if flag:
                        continue
                    temp[word] += 1
                    words.add(word)
                ind[self.keys[c]] = temp
                c += 1
                
            for word in words:
                encoding = str(hex(self.pages))[2:]
                for key in ind.keys():
                    if word in ind[key].keys():
                        encoding += key + str(hex(ind[key][word]))[2:]
                self.inv_index[word].append(encoding)
                
            
        if self.pages % 50000 == 0 or force_write:
            f = open(f'{self.index_dir}/index{int((self.pages+49999)/50000)}.txt', "w")
            for key in sorted(self.inv_index.keys()):
                data = key + ' ' + ' '.join(self.inv_index[key]) + '\n'
                f.write(data)
            self.inv_index.clear()
            f.close()
            
            
        if self.pages % 50000 == 0 or force_write:
            f = open(f'{self.index_dir}/titles{int((self.pages+49999)/50000)}.txt', 'w')
            f.write(' '.join(self.titles))
            self.titles = []
            f.close()
        
        if force_write:
            f = open(f'{self.index_dir}/numdocs.txt', 'w')
            f.write(str(self.pages))
            f.close()

    def startElement(self, tag, attributes):
        self.current = tag
        
    def endElement(self, tag):
        if tag == 'page':     
            self.body = ' '.join(self.body)
            self.title = ' '.join(self.title)
            
            self.titles.append(self.title.lower())
            
            body, infobox, cat, ref, links = self.cleaner.chunk(self.body)
            title = self.cleaner.clean(self.title)
    
            page = {"title":title, "body":body, "infobox":infobox, 
                    "categories":cat, "references":ref, "links":links}
            
            self.pages += 1
            self.add_page(page=page)
            
            self.title = []
            self.body = []
            self.id = None
            
            if self.pages % 1000 == 0:  
                print(f"Successfully parsed {self.pages} pages", flush=True)
        if tag == 'mediawiki':
            self.add_page(force_write=True)
        
    def characters(self, content):
        if self.current == 'id' and not self.id:
            self.id = int(content)
        elif self.current == 'text':
            self.body.append(content)
        elif self.current == 'title':
            self.title.append(content)
        
    def get_file_count(self):
        return int((self.pages+49999)/50000)
