import time
import xml.sax as sx
from utils import *
from collections import defaultdict

class Handler(sx.ContentHandler):
    def __init__(self):
        self.title = ''
        self.body = ''
        self.current = ''
        self.id = None
        self.cleaner = CleanerChunker()
        self.printed = 10
        self.pages = 0
        self.inv_index = defaultdict(list)
        self.page_ind = defaultdict(int)

    def add_page(self, page=None, force_write=False):
        if page:
            keys = ['t', 'b', 'i', 'c', 'r', 'l']
            c = 0
            ind = defaultdict()
            words = set()
            for key in page.keys():
                temp = defaultdict(int)
                for word in page[key]:
                    temp[word] += 1
                    words.add(word)
                ind[keys[c]] = temp
                c += 1
            
            self.page_ind[self.pages] = self.id
            
            for word in words:
                encoding = str(self.pages)
                for key in ind.keys():
                    if ind[key][word]:
                        encoding += key + str(ind[key][word])
                self.inv_index[word].append(encoding)
        if self.pages % 10000 == 0 or force_write:
            file = ""
            for key in sorted(self.inv_index.keys()):
                data = key + ' ' + ' '.join(self.inv_index[key]) + '\n'
                file += data
            f = open(f'./inverted_index/index{int((self.pages+9999)/10000)}.txt', "w")
            f.write(file)
            self.inv_index.clear()
                
                

    def startElement(self, tag, attributes):
        self.current = tag
        
    def endElement(self, tag):
        if tag == 'page':# and self.printed:
            #print(self.id)
            #print(self.title)
            #print(self.body)

            body, infobox, cat, ref, links = self.cleaner.chunk(self.body)
            title = self.cleaner.clean(self.title)

            page = {"title":title, "body":body, "infobox":infobox, 
                    "categories":cat, "references":ref, "links":links}
            
            self.pages += 1
            self.add_page(page=page)
            
            self.title = ''
            self.body = ''
            self.id = None
            self.printed -= 1
        
            if self.pages % 1000 == 0:
                print(f"Successfully parsed {self.pages} pages", end="\r")
        
        if tag == 'mediawiki':
            self.add_page(force_write=True)
        
    def characters(self, content):
        if self.current == 'id' and not self.id:
            self.id = int(content)
        elif self.current == 'text':
            self.body += content
        elif self.current == 'title':
            self.title += content
        
    def get_file_count(self):
        return int((self.pages+9999)/10000)