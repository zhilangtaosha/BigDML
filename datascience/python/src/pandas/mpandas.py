#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：pandas的数据结构Series和dataFrame
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime,timedelta,date

'''
    Series类型学习
'''
class CSeries(object):
    def __init__(self):
        pass

    def unitily(self):
        version=pd.show_versions()
        print(version)

    # Series（一维不同质可变长数组）
    def mSeries(self):
        a=pd.Series(range(5))
        s=pd.Series([1,3,4,np.nan,6,8],index=['a','b','c','d','e','g'])  # 列表法
        s=pd.Series({'a':[1,2,3,4],'b':[6,7,8],'c':{284, 34}})           # 字典法
        s = pd.Series(['c', 'a', 'd', 'a', 'a', 'b', 'b', 'c', 'c'],index=list("nibushigh"))
        mask=s.isin(['a','d'])
        print s.value_counts()
        print s[mask]

        # 数据对齐
        d = {'a' : 0., 'b' : 1., 'c' : 2.}
        b=pd.Series(d)
        c=pd.Series(5., index=['a', 'b', 'c', 'd', 'e'])
        print a,b,c

        import matplotlib.pyplot as plt
        plt.hist(a,bins=3)
        plt.show()

        import seaborn
        seaborn.distplot(a,bins=3)


'''
    pandas基础
'''
class PandasBasic(object):
    def __init__(self):
        pass

    def demo(self):
        dates=pd.date_range('20140202',periods=6)
        df=pd.DataFrame(np.random.randn(6,4),index=dates,columns=list('ABCD'))
        #df.to_excel('hhah.xlsx',sheet_name='nigao')
        #print df
        #df=df.cumsum()
        #plt.figure()
        #df.plot()
        #plt.legend(loc='best')
        #plt.show()

        df1=pd.DataFrame({'id':[1,2,3,4,5],"raw_grade":['a','b','c','d','e']})
        df1['grade']=df1.raw_grade.astype('category')
        df1.grade.cat.categories=['very good','good','very bad']
        df1.grade=df1.grade.cat.set_categories


    #数据帧
    def pandas_build(self):
        # Dataframe构建方式1：key是列，行元素分别是每个value，一一对应
        data = {'state': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada'],
                 'year': [2000, 2001, 2002, 2001, 2002],
                 'pop': [1.5, 1.7, 3.6, 2.4, 2.9]}
        frame1 =pd.DataFrame(data,columns=['pop','year','state','noc'],index=list('ABCDE'))
        print frame1,frame1.state,frame1['state'],frame1.ix['A']
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

    # 索引和切片
    def pandas_select(self):
        data=pd.DataFrame(np.arange(16).reshape((4, 4)),index=['Ohio', 'Colorado', 'Utah', 'New York'], columns=['one', 'two', 'three', 'four'])
        print data

    # 数据读取和保存
    def readwirtexls(self):
        #from csv
        data=pd.read_csv('../../data/data.csv',header=False,index_col='fu5')
        print data
        #to csv
        data.to_csv('../../data/data1.csv',columns=['num'],header=True,index=True,index_label=range(2,30))



'''
    数据帧统计处理
    Ref:http://mp.weixin.qq.com/s/y6Sy2OV6b-25thHPRC30Tg
'''
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



'''
    pandas和sql互操作
'''
import MySQLdb
from sqlalchemy import create_engine

class PandasSQL(object):
    def __init__(self):
        pass

    def buildpandaFromSql(self):
        conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='root',db='study')
        cur=conn.cursor() #cursorclass=MySQLdb.cursors.DictCursor)
        cur.execute("select date,cnt,cnt_user from row2col_tbl limit 3")
        sqllist=cur.fetchall()
        sqlarray=np.array(sqllist,dtype='int')  #注意指定数据类型，否则会出错
        sqlframe=pd.DataFrame(sqlarray,columns=['date','cnt','cnt_user'],index=range(len(sqllist)))
        print sqlframe
        # numpy数组直接统计
        print sqlarray.any()


    # 保存和读取sql
    def readwritesql(self):
        engine = create_engine('mysql+mysqldb://root:root@localhost/study')

        # csv-->pandas-->mysql
        data=pd.read_csv('../../data/data.csv',header=False)
        print data,'\n',type(data)
        #data1=pd.DataFrame(['23.23',12,'ZHNWR','232'])
        data.to_sql('data',engine,if_exists='replace',index=False,chunksize=1000)

        # mysql -->pandas
        pr=pd.read_sql_table('data',engine,index_col=['fu5'],columns=['num'])
        pq=pd.read_sql_query("select num from data order by num",engine)
        print pr,pq

    # pandas实现连接操作
    def pJoin(self):
        #按默认的相同列名合并
        orders=pd.DataFrame(pd.read_csv('../../data/mjoin/orders.csv'))
        persons=pd.DataFrame(pd.read_csv('../../data/mjoin/persons.csv'))
        print orders
        print persons
        lj=pd.merge(orders,persons,how='left')
        print lj

        #按指定的列名合并
        pv=pd.DataFrame(pd.read_table('../../data/mjoin/date_fu2_pv',header=None,names=['date','fu2','pv']))
        uv=pd.DataFrame(pd.read_table('../../data/mjoin/date_fu2_uv',header=None,names=['date','fu2','uv']))
        lj=pd.merge(pv,uv,how='left',left_on=['date','fu2'],right_on=['date','fu2'])
        print lj




if __name__ == "__main__":
    mpds=PandasStat()
    mpds.groupby()

