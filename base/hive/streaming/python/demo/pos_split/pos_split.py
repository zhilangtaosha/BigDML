#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Fun:pythom streanming 字符串分割
    Author:tuling56
    Date:
'''
import os,sys

reload(sys)
sys.setdefaultencoding('utf-8')


'''
    针对下划线分割的情况
    例如:1_2_3
'''
def pos_split_underline(instr):
    ds,movieidlist=instr.strip().split("\t")
    movieid_l=movieidlist.split("_")
    for k,v in enumerate(movieid_l):
        print "\t".join([ds,str(k),v])

'''
    针对数组形式的字符串
    例如:'[1,2,3]'
'''
def pos_split_arrstr(instr):
    ds,midlist=instr.strip().split("\t")
    #print instr,ds,midlist
    mid_l=eval(midlist)
    print mid_l
    for k,v in enumerate(mid_l):
        print "\t".join([ds,str(k),str(v)])


for line in open('pos_split_num.txt'):
#for line in sys.stdin:
    pos_split_arrstr(line)
