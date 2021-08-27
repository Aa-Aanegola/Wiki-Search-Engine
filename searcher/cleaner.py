from Stemmer import Stemmer
from nltk.corpus import stopwords
import re

class Cleaner:
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