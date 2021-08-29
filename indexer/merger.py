import os
from collections import defaultdict
import re

class Merger:
    def __init__(self, inv_ind_count, index_dir):
        self.inv_ind_count = inv_ind_count
        self.index_dir = index_dir   
        self.cur_count = inv_ind_count+1
        
    def merge_files(self, file1, file2):
        fp1 = open(file1, "r")
        fp2 = open(file2, "r")
        out = open(f'./inverted_index/index{self.cur_count}.txt', "w")
        line1 = []
        line2 = []
        while not fp1.closed and not fp2.closed:
            if len(line1) == 0:
                line1 = fp1.readline().strip().split()
                if len(line1) == 0 or line1[0] == '':
                    fp1.close()
                    break
            if len(line2) == 0:
                line2 = fp2.readline().strip().split()
                if len(line2) == 0 or line2[0] == '':
                    fp2.close()
                    break
            if line1[0] == line2[0]:
                data = line1[0] + ' ' + ' '.join(sorted(line1[1:] + line2[1:])) + '\n'
                out.write(data)
                line1 = []
                line2 = []
            elif line1[0] < line2[0]:
                data = line1[0] + ' ' + ' '.join(sorted(line1[1:])) + '\n'
                out.write(data)
                line1 = []
            else:
                data = line2[0] + ' ' + ' '.join(sorted(line2[1:])) + '\n'
                out.write(data)
                line2 = []
        
        while not fp1.closed:
            line1 = fp1.readline().strip().split()
            if len(line1) == 0 or line1[0] == '':
                fp1.close()
                break
            data = line1[0] + ' ' + ' '.join(sorted(line1[1:])) + '\n'
            out.write(data)
        
        while not fp2.closed:
            line2 = fp2.readline().strip().split()
            if len(line2) == 0 or line2[0] == '':
                fp2.close()
                break
            data = line2[0] + ' ' + ' '.join(sorted(line2[1:])) + '\n'
            out.write(data)
        
        out.close()

        return f'./inverted_index/index{self.cur_count}.txt'
            
    def create_index(self):
        files = [f'./inverted_index/index{i+1}.txt' for i in range(self.inv_ind_count)]
        
        while len(files) > 1:
            print(f"Merging {len(files)} files", end='\r')
            nx_files = []
            for i in range(0, len(files)-1, 2):
                nx_files.append(self.merge_files(files[i], files[i+1]))
                self.cur_count += 1
            if len(files)%2:
                nx_files.append(files[-1])
            files = nx_files
        
        self.cur_count -= 1
        for i in range(1, self.cur_count):
            os.remove(f'./inverted_index/index{i}.txt')
        os.rename(f'./inverted_index/index{self.cur_count}.txt', f'./inverted_index/master_index.txt')
        
        current = 1
        count = 0
        fp = open('./inverted_index/master_index.txt', "r")
        out = open(f'./{self.index_dir}/invindex{current}.txt', "w")
        ends = open(f'./{self.index_dir}/library.txt', "w")
        stat = open(f'./invertedindex_stat.txt', 'a')
        total_count = 0
        while not fp.closed:
            line = fp.readline().strip() + '\n'
            if len(line) == 1:
                out.close()
                break
            out.write(line)
            count += 1
            if count % 100000 == 0:
                total_count += 100000
                word1 = line.split()[0]
                ends.write(word1 + '\n')
                out.close()
                current += 1
                out = open(f'./{self.index_dir}/invindex{current}.txt', "w")
        
        total_count += count % 100000
        total_count = str(total_count) + '\n'
        stat.write(total_count)
        ends.close()
        fp.close()
        os.remove('./inverted_index/master_index.txt')