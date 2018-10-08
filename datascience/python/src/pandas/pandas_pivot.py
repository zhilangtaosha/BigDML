#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Fun:pandas数据变换和透视
    Ref:
    State：
    Date:2018/10/8
    Author:tuling56
'''


import hues
import re, os, sys

reload(sys)
sys.setdefaultencoding('utf-8')


import pandas as pd
import numpy as np


class CPandas(object):
    def __init__(self):
        pass

    # Series构建
    def series_build(self):
        s1=pd.Series(range(5))  # 列表未指定index
        s2=pd.Series([1,3,4,np.nan,6,8],index=['a','b','c','d','e','g'],name='xx')  # 列表指定index，命名索引
        s3= pd.Series(['c', 'a', 'd', 'a', 'a', 'b', 'b', 'c', 'c'],index=list("nibushigh"),name='xx') # 列表指定index(index可重复),命名索引
        s4=pd.Series({'a':[1,2,3,4],'b':[6,7,8],'c':{284, 34}}) # 字典法

        s1.name="name1" # 命名索引

        mask=s1.isin(['a','d'])
        print s1.value_counts()
        print s1[mask]


    # Dataframe构建
    def df_build(self):
        # Dataframe构建方式1：key是列，行元素分别是每个value，一一对应
        '''
               pop  year   state  noc
            A  1.5  2000    Ohio  NaN
            B  1.7  2001    Ohio  NaN
            C  3.6  2002    Ohio  NaN
            D  2.4  2001  Nevada  NaN
            E  2.9  2002  Nevada  NaN
        '''
        data = {'state': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada'],
                'year': [2000, 2001, 2002, 2001, 2002],
                'pop': [1.5, 1.7, 3.6, 2.4, 2.9]
               }
        df1 =pd.DataFrame(data,columns=['pop','year','state','noc'],index=list('ABCDE'))
        print df1
        print df1.state,df1['state'] # 取列数据，均返回Series
        print df1.ix['A']  # 取行数据，返回Series
        print '--------------------------------------------------------'

        # Dataframe构建方式2(逐行构建，列名由自己指定)
        datal=[['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada'],[2000, 2001, 2002, 2001, 2002], [1.5, 1.7, 3.6, 2.4, 2.9]]
        frame2=pd.DataFrame(datal,columns=['state','year','pop','add1','add2'])
        print frame2
        print '--------------------------------------------------------'

        # Dataframe构建方式3（嵌套字典）
        data3 = {'Nevada': {2001: 2.4, 2005: 2.9}, 'Ohio': {2000: 1.5, 2001: 1.7, 2002: 3.6}}
        frame3=pd.DataFrame(data3)
        print frame3,frame3.T
        print '--------------------------------------------------------'

        #Dataframe构建方式4（由numpy矩阵构建）
        data4=np.arange(6).reshape(2,3)
        print data4
        frame4=pd.DataFrame(data4,columns=['col1','col2','col3'],index=['row1','row2'])
        print frame4
        print '--------------------------------------------------------'

        #Dataframe构建方式5（由pd.Series构建）
        data5={"col1":pd.Series(np.arange(5),index=['r1','r2','r3','r4','r5']),"col2":pd.Series(['y','x','t','v','c'],index=['r1','r2','r3','r4','r5'])}
        print data5
        frame5=pd.DataFrame(data5,columns=['col1','col2','col3'],index=['r1','r2','r3','r4','r5'])
        print frame5
        print '--------------------------------------------------------'

    def run(self):
        self.df_build()


# 测试入口
if __name__ == "__main__":
    ct = CPandas()
    ct.run()

