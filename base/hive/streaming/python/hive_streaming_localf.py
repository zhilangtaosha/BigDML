#!/usr/bin/env python

import sys,re,os,re


ban_ver_list=[]

def load_data():
    global ban_ver_list
    with open('ban_ver','r') as f:
        for line in f:
            line=line.strip('\n').strip()
            ban_ver_list.append(line)


load_data()
#print version_list
#sys.exit(1)

for line in sys.stdin:
    try:
        # 920F48C20720EA0CF58E33280D53D6EC6F7B7E0F        [3,1]   ["5004","0","0"]        0,0,0   220.137.221.17  1507564796
        pid,mlint,flstr,sstr,fip,ftime = line.rstrip().split('\t')
        max_lint=str(max(eval(mlint)))
        first_lstr=eval(flstr)[0]
        sstr=sstr.replace(',','_')
        if first_lstr in ban_ver_list:
            continue
        print '\t'.join([pid,max_lint,first_lstr,sstr,fip,ftime])
        #print '\t'.join(['a','b','c','d','e','f'])
    except:
        t,value,traceback = sys.exc_info()
        continue

