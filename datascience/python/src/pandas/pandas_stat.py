#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Fun:pandas数据帧统计处理
    Ref:http://mp.weixin.qq.com/s/y6Sy2OV6b-25thHPRC30Tg
    State：
    Date:2018/10/8
    Author:tuling56
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime,timedelta,date


class PandasStat(object):
    def __init__(self):
        self.pdata=pd.read_table('../../data/git_data/date_pv_uv',header=None,names=['datec','pv','uv'])
        data = {'Age': [12, 16, 12, 16, 23],
                     'Sex': ['male', 'female', 'male', 'male', 'female'],
                     'Weight': [1.5, 1.7, 3.6, 2.4, 2.9],
                     'Height':[120,130,150,70,110]}
        self.pdata=pd.DataFrame(data)

    #　最值处理
    def maxmin(self):
        #将整型转换成日期
        year=map(lambda x:int(str(x)[0:4]),self.pdata['datec'])
        month=map(lambda x:int(str(x)[4:6]),self.pdata['datec'])
        day=map(lambda x:int(str(x)[6:8]),self.pdata['datec'])
        self.pdata['datec']=map(lambda x:date(x[0],x[1],x[2]),zip(year,month,day))

        #统计最大值，最小值，和均值等
        maxnewi,minnewi,sumnewi=max(self.pdata['pv']),min(self.pdata['pv']),sum(self.pdata['pv'])
        maxtotali,mintotali,sumtotali=max(self.pdata['uv']),min(self.pdata['uv']),sum(self.pdata['uv'])

        maxv=self.pdata.max()
        minv=self.pdata.min()
        sumv=self.pdata.sum()
        maxnewi,maxtotali=maxv['pv'],maxv['uv']
        minnewi,mintotali=minv['pv'],maxv['uv']

    # 分组统计
    def groupby(self):
        groupd=self.pdata.groupby('Age')
        print groupd.mean()

        # pandas按指定条件进行分组汇总(这里主要是日期)：http://toutiao.com/i6321318705200366081/
        #pdata = self.pdata.set_index('datec')
        #groupd1=pdata.resample('M',how=sum).fillna(0)
        #print groupd1


if __name__ == "__main__":
    mpds=PandasStat()
    mpds.groupby()

