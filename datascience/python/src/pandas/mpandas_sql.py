#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：pandas和sql互操作
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime,timedelta,date


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
    mpds=PandasSQL()
    mpds.pJoin()

