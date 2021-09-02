from Stemmer import Stemmer
from nltk.corpus import stopwords
import re

class Cleaner:
    def __init__(self):
        self.stemmer = Stemmer('english')
        self.stopwords = set(stopwords.words('english'))

    def clean(self, text):
        token = text.lower()
        tokens_nostop = ["" if token in self.stopwords else token]
        ret = self.stemmer.stemWords(tokens_nostop)[0]
        return ret