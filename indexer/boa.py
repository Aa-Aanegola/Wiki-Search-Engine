import os
import sys
from collections import defaultdict

class Constrictor:
    def __init__(self, index_dir, num_docs):
        self.index_dir = index_dir
        self.weights = {'T':5, 'I':3, 'B':1, 'C':2, 'R':0.5, 'L':0.5}
        self.num_docs = num_docs
        self.index_dir = index_dir
        
    def get_tf(self, posting):
        sel = 'id'
        prev = 0
        dic = defaultdict()
        for i in range(len(posting)):
            if posting[i].isdigit() or (posting[i]>='a' and posting[i]<='f'):
                continue
            dic[sel] = int(posting[prev:i], 16)
            sel = posting[i]
            prev = i+1
        dic[sel] = int(posting[prev:len(posting)], 16) 
        tf = 0
        for key in dic.keys():
            if key == 'id':
                continue
            tf += self.weights[key] * dic[key]
        return tf
    
    def parse(self, posting):
        sel = 'id'
        prev = 0
        dic = defaultdict()
        for i in range(len(posting)):
            if posting[i].isdigit() or (posting[i]>='a' and posting[i]<='f'):
                continue
            dic[sel] = int(posting[prev:i], 16)
            sel = posting[i]
            prev = i+1
        dic[sel] = int(posting[prev:len(posting)], 16) 
        return dic
    
    def compress(self, id):
        print(id)
        f = open(f'{self.index_dir}/invindex{id}.txt', 'r')
        new = open('temp.txt', 'w')
        index = [line.strip().split() for line in f.readlines()]
        f.close()
        for line in index:
            updat = defaultdict(float)
            for posting in line[1:]:
                tf = self.get_tf(posting)
                updat[posting] = tf
            sorted_postings = sorted(updat.items(), key=lambda kv: kv[1], reverse=True)
            to_d = [line[0]]
            counts = {"id":0, "T": 0, "I": 0, "B": 0, "R": 0, "C": 0, "L": 0}
            for posting, _ in sorted_postings:
                dic = self.parse(posting)
                flag = False
                for key in dic.keys():
                    if counts[key] < 10000:
                        flag = True
                        counts[key] += 1
                if flag:
                    to_d.append(posting)

            to_d_str = ' '.join(to_d) + '\n'
            new.write(to_d_str)
        new.close()
        os.remove(f'{self.index_dir}/invindex{id}.txt')
        os.rename('temp.txt', f'{self.index_dir}/invindex{id}.txt')

                
    def master_compress(self):
        for i in range(381):
            self.compress(i+1)
            
if __name__ == "__main__":
    index_dir = sys.argv[1]
    with open(f'{index_dir}/numdocs.txt', 'r') as f:
        num_docs = int(f.read())
    constrictor = Constrictor(index_dir, num_docs)
    constrictor.master_compress()