from Stemmer import Stemmer
from nltk.corpus import stopwords
import re

class CleanerChunker:
    def __init__(self):
        self.stemmer = Stemmer('english')
        self.stopwords = set(stopwords.words('english'))
        extra_stops = set(['cite', 'https', 'http', 'com', 'url', 'categori'
                                'ref', 'reflist', 'title', 'name', 'author', 
                                'data', 'also', 'link', 'org', 'publish', 'websit',
                                'caption', 'imag', 'infobox', 'wiki'])
        self.stopwords = set.union(self.stopwords, extra_stops)

    def clean(self, text):
        text = text.lower()
        text = re.sub(r'http[^ ]*\ ', r' ', text)
        text = re.sub(r'&lt|&gt|&amp|&quot|&apos|&nbsp', r' ', text)
        text = re.sub(r'[^a-z0-9 ]', r' ', text)
        tokens = text.split()
        tokens_nostop = [word for word in tokens if word not in self.stopwords]
        ret = self.stemmer.stemWords(tokens_nostop)
        return ret
    
    def get_body(self, text):
        body = []
        prev = 0
        for info in re.finditer(r'\{\{\ *infobox', text):
            body.append(text[prev:info.start()])
            i = info.start()+2
            bracks = 2
            while bracks != 0 and i < len(text):
                if text[i] == '{':
                    bracks += 1
                elif text[i] == '}':
                    bracks -= 1
                i += 1
            prev = i
        body.append(text[prev:])
        return self.clean(' '.join(body))
    
    def get_infobox(self, text):
        infoboxes = []
        for info in re.finditer(r'\{\{\ *infobox', text):
            i = info.start()+2
            bracks = 2
            while bracks != 0 and i < len(text):
                if text[i] == '{':
                    bracks += 1
                elif text[i] == '}':
                    bracks -= 1
                i += 1
            infoboxes.append(text[info.start():i])
        return self.clean(' '.join(infoboxes))
    
    def get_references(self, text):
        res = []
        for ref in re.finditer(r'==\ *references\ *==', text):
            next_debar = re.search(r'==\ *[a-z]*\ *==|\[\[category', text[ref.end():])
            if next_debar:
                res.append(text[ref.end():ref.end()+next_debar.start()])
            else:
                res.append(text[ref.end():])
        return self.clean(' '.join(res))
        
    def get_categories(self, text):
        ret = re.findall(r'\[\[category:(.*)', text)
        return self.clean(' '.join(ret))
    
    def get_links(self, text):
        res = []
        for ref in re.finditer(r'==\ *external links\ *==', text):
            next_debar = re.search(r'\[\[category', text[ref.end():])
            if next_debar:
                res.append(text[ref.end():ref.end()+next_debar.start()])
            else:
                res.append(text[ref.end():])
        return self.clean(' '.join(res))
    
    def chunk(self, text):
        text = text.lower()
        chunks = (text, "")
        res = re.search(r'==\ *references\ *==', text)
        if res:
            chunks = (text[:res.start()], text[res.start():])
        return self.get_body(chunks[0]), \
            self.get_infobox(chunks[0]), \
            self.get_categories(chunks[1]), \
            self.get_references(chunks[1]), \
            self.get_links(chunks[1])