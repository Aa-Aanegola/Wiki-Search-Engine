from Stemmer import Stemmer
from nltk.corpus import stopwords
import re

class Cleaner:
    def __init__(self):
        self.stemmer = Stemmer('english')
        self.stopwords = set(stopwords.words('english'))

    def clean(self, text):
        text = text.lower()
        text = re.sub(r'http[^ ]*\ ', r' ', text)
        text = re.sub(r'&lt|&gt|&amp|&quot|&apos|&nbsp', r' ', text)
        text = re.sub(r'[^a-z0-9\' ]', r' ', text)
        tokens = text.split()
        tokens_nostop = [word for word in tokens if word not in self.stopwords]
        ret = self.stemmer.stemWords(tokens_nostop)
        return ret