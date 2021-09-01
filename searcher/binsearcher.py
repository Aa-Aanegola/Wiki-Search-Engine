import json
from collections import defaultdict
import re

class BinSearcher:
    def __init__(self, index_dir, cleaner):
        self.index_dir = index_dir
        self.cleaner = cleaner
        f = open(f'{index_dir}/library.txt', 'r')
        self.indices = [line.strip() for line in f]
        f.close()  
        self.expand = {'t':'title', 'b':'body', 'i':'infobox', 'c':'categories', 'r':'references', 'l':'links'}
        
    def get_word(self, token):
        if len(token) > 2 and token[1] == ':':
            return token[2:]
        
    def get_list(self, token):
        if len(token) > 2 and token[1] == ':':
            token = token[2:]
        
        token = self.cleaner.clean(token)
        if not len(token):
            return []
        token = token[0]
        
        i = 0
        while i < len(self.indices):
            if token <= self.indices[i]:
                break
            i += 1
        index_file = open(f'{self.index_dir}/invindex{i+1}.txt', 'r')
        index = [line.strip().split() for line in index_file.readlines()]
        index_file.close()
        
        l = 0 
        r = len(index)-1
        
        while l <= r:
            mid = int((l+r)/2)
            line = index[mid]
            if line[0] == token:
                return line[1:]
            elif line[0] < token:
                l = mid+1
            else:
                r = mid-1
        return []
    
    def clean_map(self, map):
        master = {}
        for token in map.keys():
            temp = {}
            ids = [int(re.sub(r'([0-9]*).*', r'\1', word)) for word in map[token]]
            for label in ['t', 'b', 'i', 'c', 'r', 'l']:
                dat = [re.sub(r'.*%c([0-9]*).*' % label, r'\1', word) for word in map[token]]
                for i in range(len(dat)):
                    if dat[i] == map[token][i]:
                        dat[i] = ''
                ret = []
                for i in range(len(ids)):
                    if dat[i]:
                        ret.append(ids[i])
                temp[self.expand[label]] = ret
            master[token] = temp
        print(json.dumps(master, indent=4))
    
    def search(self, search_str):
        search_str = search_str.lower()
        tokens = search_str.split()
        map = defaultdict(list)
        for token in tokens:
            map[self.get_word(token)] = self.get_list(token)
        
        self.clean_map(map)