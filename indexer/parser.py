import time
import xml.sax as sx
from cleaner import *
from memory_profiler import profile

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
        self.inv_index = {}
        
    def add_page(self, page=None, force_write=False):
        if page:
            c = 0
            ind = {}
            words = set()
            for key in page.keys():
                temp = {}
                has = {}
                for word in page[key]:
                    flag = False
                    if len(word) > 15:
                        flag = True
                    for letter in word:
                        if letter not in has.keys():
                            has[letter] = 0
                        has[letter] += 1
                    for key in has.keys():
                        if has[key] > 5:
                            flag = True
                    has.clear()
                    if flag:
                        continue
                    if word not in temp.keys():
                        temp[word] = 0
                    temp[word] += 1
                    words.add(word)
                ind[self.keys[c]] = temp
                c += 1
                del temp
                del has
                
            for word in words:
                encoding = str(hex(self.pages))[2:]
                for key in ind.keys():
                    if word in ind[key].keys():
                        encoding += key + str(hex(ind[key][word]))[2:]
                if word not in self.inv_index.keys():
                    self.inv_index[word] = []
                self.inv_index[word].append(encoding)
                del encoding
            del ind
            del words
            
        if self.pages % 10000 == 0 or force_write:
            f = open(f'{self.index_dir}/index{int((self.pages+9999)/10000)}.txt', "w")
            for key in sorted(self.inv_index.keys()):
                data = key + ' ' + ' '.join(self.inv_index[key]) + '\n'
                f.write(data)
            self.inv_index.clear()
            f.close()
            del f
            
            
        if self.pages % 10000 == 0 or force_write:
            f = open(f'{self.index_dir}/titles{int((self.pages+9999)/10000)}.txt', 'w')
            f.write(' '.join(self.titles))
            del self.titles
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

            del title
            del body
            del infobox
            del cat
            del ref
            del links
            del page
            
            if self.pages % 1000 == 0:  
                print(f"Successfully parsed {self.pages} pages", flush=True)
        if tag == 'mediawiki':
            self.add_page(force_write=True)
        
    def characters(self, content):
        if self.current == 'id' and not self.id:
            self.id = content
        elif self.current == 'text':
            self.body.append(content)
        elif self.current == 'title':
            self.title.append(content)
        
    def get_file_count(self):
        return int((self.pages+9999)/10000)