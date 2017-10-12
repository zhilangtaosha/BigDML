#!/usr/bin/env python

import sys,re,os,re
for line in sys.stdin:
    try:
        # 920F48C20720EA0CF58E33280D53D6EC6F7B7E0F        [3,1]   ["5004","0","0"]        0,0,0   220.137.221.17  1507564796
        pid,mlint,flstr,sstr,fip,ftime = line.rstrip().split('\t')
        max_lint=str(max(eval(mlint)))
        first_lstr=eval(flstr)[0]
        sstr=sstr.replace(',','_')
        print '\t'.join([pid,max_lint,first_lstr,sstr,fip,ftime])
    except Exception,e:
    :
        t,value,traceback = sys.exc_info()
        continue

