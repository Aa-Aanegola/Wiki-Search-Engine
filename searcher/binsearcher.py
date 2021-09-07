import json
from collections import defaultdict
import re
from math import log

class BinSearcher:
    def __init__(self, index_dir, cleaner, num_docs):
        self.index_dir = index_dir
        self.cleaner = cleaner
        f = open(f'{index_dir}/library.txt', 'r')
        self.indices = [line.strip() for line in f]
        f.close()  
        self.expand = {'t':'title', 'b':'body', 'i':'infobox', 'c':'categories', 'r':'references', 'l':'links'}
        self.weights = {'t':5, 'i':3, 'b':1, 'c':2, 'r':0.5, 'l':0.5}
        self.num_docs = num_docs
        self.map = defaultdict(float)
        
    def get_word(self, token):
        select = 'a'
        if len(token) > 2 and token[1] == ':':
            return token[2:]
        return select, token
        
    def parse(self, posting):
        sel = 'id'
        prev = 0
        dic = defaultdict()
        for i in range(len(posting)):
            if posting[i].isdigit():
                continue
            dic[sel] = int(posting[prev:i])
            sel = posting[i]
            prev = i+1
        dic[sel] = int(posting[prev:len(posting)]) 
        return dic    
    
    def set_list(self, select, token):
        token = self.cleaner.clean(token)
        if not len(token):
            return []
        
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
        mid = -1
        
        while l <= r:
            mid = int((l+r)/2)
            line = index[mid]
            if line[0] == token:
                break
            elif line[0] < token:
                l = mid+1
            else:
                r = mid-1
        if l>r:
            return
    
        line = index[mid][1:]
        idf = log(self.num_docs/len(line))
        for posting in line:
            if select not in posting and select != 'a':
                continue
            dic = self.parse(posting)
            tf = 0
            for key in dic.keys():
                if key == 'id':
                    continue
                tf += self.weights[key] * dic[key]
            tf = log(1+tf)
            self.map[dic['id']] += tf 
    
    
    def search(self, search_str):
        search_str = search_str.lower()
        tokens = search_str.split()
        for token in tokens:
            select, temp = self.get_word(token)
            self.set_list(select, temp)
            
        top_res = sorted(self.map.items(), key=lambda kv: kv[1], reverse=True)[:10]
        
        res = []
        for item in top_res:
            f = open(f'./{self.index_dir}/titles{item[0]//100000+1}.txt', 'r')
            titles = f.readlines()
            res.append(titles[item[0]%100000].strip())
            f.close()
        print(res)