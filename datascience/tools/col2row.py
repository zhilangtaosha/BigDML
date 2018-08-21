#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Fun:python实现mysql的列转行
    Ref:
    State：完成初版，持续更新中
    Date:2017/11/20
    Author:tuling56
'''

import hues
import re, os, sys

reload(sys)
sys.setdefaultencoding('utf-8')


class CCol2Row():
    def __init__(self):
        self.fout=open('col2row.res','w')

    def __del__(self):
        self.fout.close()

    def col2row(self):
        header=[]
        with open('./data/col2row.csv','r') as f:
            headflag=False
            for line in f:
                fields=line.strip().split(',')
                if not headflag: # 先获取列标题
                    header=fields
                    headflag=True
                    continue

                row_class_elems=fields[0]
                for colname,colnum in zip(header[1:],fields[1:]):
                    output=row_class_elems+'\t'+colname+'\t'+str(colnum)+'\n'
                    self.fout.write(output)

# 测试入口
if __name__ == "__main__":
    ct = CCol2Row()
    ct.col2row()

