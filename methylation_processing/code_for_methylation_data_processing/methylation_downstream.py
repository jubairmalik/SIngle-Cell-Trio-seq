# -*- coding: utf-8 -*-
"""methaylation_multiple_gzFile.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1x92FanrXLUuLJBJFrlmE_kLG9hnYShad
"""
#only downstream part
import gzip
import csv
import pandas as pd
import numpy as np
import re
import glob
from collections import defaultdict
import os

path = './'
aty=os.listdir(path)
print(len(path))

import time

start_time = time.time()

#------------read gz file-------
import sys
import gzip
import shutil


def run(path):
    with gzip.open(path, 'rb') as f_in:
        #print('byte opened successfully')
        with open(path[:-3], 'wb') as f_out:
            #print('byte write successfully')
            shutil.copyfileobj(f_in, f_out)
            #print('byte copied and written successfully')

    gsm = pd.read_csv(path[:-3], delimiter='\t')
    gsm_pos_list = gsm['Pos']
    #print('before',len(gsm_pos_list ))
    gsm = gsm.loc[(gsm['Type'] == 'CpG') & (gsm['#Chr'] != 'chrX') & (gsm['#Chr'] != 'chrY')]
    gsm = gsm.reset_index()
    gsm = gsm.drop(columns='index')
    gsm_pos_list = gsm['Pos']
    #print('after',len(gsm_pos_list))
    gsm_MetRate_list = gsm['MetRate']
    #print(max(gsm_pos_list))

    gsm_pos_count_list = [0] * (max(gsm_pos_list) + 1)  #real list where I will get position
    gsm_MetRate_count_list = [0] * (max(gsm_pos_list) + 1)  #for indexing

    for i in range(len(gsm_pos_list)):
        #if i % 10000 == 0:
        #print(i)
        gsm_pos_count_list[gsm_pos_list[i]] += 1
        gsm_MetRate_count_list[gsm_pos_list[i]] += gsm_MetRate_list[i]
    #print(len(gsm_pos_list))
    #print(sum(gsm_pos_count_list))
    #print(sum(gsm_MetRate_list))
    #print(sum(gsm_MetRate_count_list))

    Ann = pd.read_csv('removing_duplicated_final.csv')



    end_column = Ann['end']
    ann_MetRate_list2 = []
    for _end in end_column:
        if _end + 500 > len(gsm_pos_count_list):
            _end2 = len(gsm_pos_count_list)
        else:
            _end2 = _end + 500
        #print("start: " + str(_end) + " end : " + str(_end2))
        #print(gsm_pos_count_list[_end:_end2+1])
        #rint(gsm_MetRate_count_list[_end:_end2+1])

        sum_denom = sum(gsm_pos_count_list[_end:_end2 + 1])
        if sum_denom > 0:
            ann_MetRate_list2.append(round(sum(gsm_MetRate_count_list[_end:_end2 + 1]) / sum_denom, 3))
        else:
            ann_MetRate_list2.append(0)

    #print(type(start_column[0]))
    #ann_MetRate_list_total = [((a + b) / 2.0) for a, b in zip(ann_MetRate_list, ann_MetRate_list2)]
    Ann["AvgMetRate"] = ann_MetRate_list2

    #Ann.to_csv('Gene_Annotation+GSM_dummy_start_end.csv', index=False)
    #print("required time : " + str(time.time() - start_time) + " s")
    #print('first: ',ann_MetRate_list)
    #print('sec: ',ann_MetRate_list2)
    Ann.to_csv(path[:-7] + '.csv', index=False)
    os.remove(path[:-3])
    reduce(path[:-7] + '.csv')
    os.remove(path[:-7] + '.csv')





def reduce(path):
    data = pd.read_csv(path)
    #print(data.head(5))

    data = data.sort_values('gene_name', ignore_index= True)
    #data.to_csv('new2.csv')
    #print(data.head(5))

    gene_name = data['gene_name']
    AvgMetRate = data['AvgMetRate']

    i = 0
    j = 1
    max_len = len(data['gene_name'])
    count = 0
    while True:
        count += 1
        #if count%1000==0:
            #print(count)
        if gene_name[i] == gene_name[i+j]:
            if AvgMetRate[i] > AvgMetRate[i+j]:
                #drop_list.append(i-1)
                data = data.drop(i+j)
                j += 1
            else:
                data = data.drop(i)
                i = i + j
                j = 1
        else:
            i = i + j
            j = 1
        if i + j == max_len:
            break

    #print(data.head(100))
    data.to_csv(path[:-4] + "_reduced.csv", index=False)


if __name__ == '__main__':
    #if len(sys.argv) == 2:
    list_dir = os.listdir(path)
    files = [x for x in list_dir if x.endswith('.gz')]
    #print(files)
    for _file in files:
        run(_file)
    #list_dir2 = os.listdir(os.getcwd())
    #files2 = [ x  for x in list_dir2 if x.endswith('.txt')]
    #for _file1 in files2:
    #  os.remove(_file1)
    print("required time : " + str(((time.time() - start_time)) / 60) + " min")
