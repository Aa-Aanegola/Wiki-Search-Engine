from Stemmer import Stemmer
from nltk.corpus import stopwords
import re

class CleanerChunker:
    def __init__(self):
        self.stemmer = Stemmer('english')
        self.stopwords = set(stopwords.words('english'))

    def clean(self, text):
        """
            Removes all URLs, html entities, Image tags and special characters
            Removes all image tags
            Removes all special characters and whitespace
            Tokenizes the data
            Removes stop words
            Converts words to stems
        """
        text = text.lower()
        text = re.sub(r'http[^ ]*\ ', r' ', text)
        text = re.sub(r'&lt|&gt|&amp|&quot|&apos|&nbsp', r' ', text)
        text = re.sub(r'[^a-z0-9 ]', r' ', text)
        tokens = text.split()
        tokens_nostop = [word for word in tokens if word not in self.stopwords]
        ret = self.stemmer.stemWords(tokens_nostop)
        return ret
    
    def get_body(self, text):
        return self.clean(re.sub(r'\{\{[^\}]*\}\}', r' ', text))
    
    def get_infobox(self, text):
        ret = re.findall(r'\{\{infobox([^\}]*)\}\}', re.sub('\n', ' ', text))
        return self.clean(' '.join(ret))
    
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