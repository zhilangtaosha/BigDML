#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Fun:python实现行转列
    Ref:http://blog.csdn.net/jackfrued/article/details/45021897?ref=myread
    State：开发中
    Date:2017/2/13
    Author:tuling56
'''
import re, os, sys
import hues

reload(sys)
sys.setdefaultencoding('utf-8')

from collections import OrderedDict


class CRow2Col():
    def __init__(self):
        #self.header=OrderedDict({"Mon":0,"Tue":0,"Wed":0,"Thu":0,"Fri":0,"Sat":0,"Sun":0})  #使用这种方式不能保证key有序
        self.header=OrderedDict([("Mon",-1),("Tue",-1),("Wed",-1),("Thu",-1),("Fri",-1),("Sat",-1),("Sun",-1)])
        self.indata=u'./data/row2col.data'
        self.resdict={}  # 最终的数据结构字典

    '''
        基本的行列转换
        ref:http://outofmemory.cn/code-snippet/6182/python-form-row-column-together-switch
        imp:如何笔记两个列表是否相等
    '''
    def demo(self):
        # 行数据（每一行代表一条记录）
        row=[('Person', 'Disks', 'Books'),
             ('Zoe', 12, 24),
             ('John', 17, 5),
             ('Julien', 3, 11)]

        # 列数据（每一列代表一条记录）
        col=[('Person', 'Zoe', 'John', 'Julien'),
             ('Disks', 12, 17, 3),
             ('Books', 24, 5, 11)]

        if col==zip(*row):
            print u'行-->列 成功'
        else:
            print u'行-->列 失败！'

        if row==zip(*col):
            print u'列-->行 成功'
        else:
            print u'列-->行 失败！'

    '''
        实战应用
        行转列（长格式转宽格式）  (需求说明：注意剔除了日期这列的数据）

        原始数据格式（行式）：
        20160214        201606  Sun     46334034
        20160215        201607  Mon     43849688
        20160216        201607  Tue     44276770
        20160217        201607  Wed     44819289
        20160219        201607  Fri     44190928
        20160221        201607  Sun     46551557

        目标数据格式（列式）：
        周别      Mon   Tue   Wed   Thu   Fri   Sat   Sun
        201607    xx    xx    xx    xx    xx    xx    xx
        201608    xx    xx    xx    xx    xx    xx    xx
    '''
    # 辅助函数：重置字典的默认值
    def __reset_dict(self):
        for k in self.header.keys():
            self.header[k]=-1

    # 辅助函数：转换后的信息导出
    def __print(self):
        # 打印头
        for key in self.header.keys():
            print key+"\t",
        print

        # 打印内容
        for k,v in self.resdict.iteritems():
            print k,v

    # 实现函数：1
    def row2col_m1(self):
        with open(self.indata, 'r') as f:
            weekstart,weekend=True,False
            for line in f:
                week,weekday,vv=line.strip().split('\t')
                self.header[weekday]=vv
                if week not in self.resdict.keys() or not self.resdict:    # 字典为空或者该周别不在字典中
                    if not weekstart:
                        self.resdict[week]='\t'.join([str(v) for v in self.header.values()])
                        self.__reset_dict()
                    else:
                        print u'该周还在继续'
                else:
                    weekstart=False
                    weekend=False
        print self.resdict

    # 实现函数:2
    def row2col_m2(self):
        with open(self.indata, 'r') as f:
            preweek=''
            weekstart=True
            week_end=False
            for line in f:
                week,weekday,vv=line.strip().split('\t')
                self.header[weekday]=vv
                if week!=preweek:
                    weekstart=True
                    preweek=week
                else:
                    weekstart=False  # 该州的数据在继续

                #这是更新
                self.resdict[preweek]='\t'.join([str(v) for v in self.header.values()]) # 更新
        self.__print()



# 测试入口
if __name__ == "__main__":
    r2c=CRow2Col()
    r2c.row2col_m2()

