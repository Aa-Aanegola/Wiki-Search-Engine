import json
from collections import defaultdict

class BinSearcher:
    def __init__(self, index_dir, cleaner):
        self.index_dir = index_dir
        self.cleaner = cleaner
        f = open(f'{index_dir}/library.txt', 'r')
        self.indices = [line.strip() for line in f]
        f.close()  
        
    def get_list(token):
        type = 'd'
        if len(token) > 2 and token[1] == ':':
            type = token[0]
            token = token[2:]
        token = self.cleaner.clean(token)
        
        i = 0
        while i < len(self.indices):
            if token <= self.indices[i]:
                break
            i++
        index_file = open(f'{index_dir}/invindex{i+1}.txt', 'r')
        offset_file = open(f'{index_dir}/offset{i+1}.txt', 'r')
        offsets = offset_file.read().split()
        offset_file.close()
        l = 0, r = len(offsets)-1
        
        while l < r:
            mid = int((l+r)/2)
            offset = offsets[mid]
            index_file.seek(offset)
            line = index_file.readline().strip().split()
            if line[0] == token:
                return line[1:]
            elif line[0] < token:
                l = mid+1
            else:
                r = mid-1
        return []
    
    def search(self, search_str):
        search_str = search_str.lower()
        tokens = search_str.split()
        map = defaultdict(list)
        for token in tokens:
            map[token] = self.get_list(token)
        
        print(map)