#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Date:
    Author:tuling56
    Fun:  mysql数据可视化(利用Plotly库)
'''

import sys
import pandas as pd
import plotly
import MySQLdb
import plotly.plotly as py

reload(sys)
sys.setdefaultencoding('utf-8')

#py.sign_in('plotlyyjm', 'plotlyyjmplotlyyjm')
plotly.tools.set_credentials_file(username='tuling56', api_key='zch6u5fnbl') # 进行授权
import plotly.graph_objs as pc


'''
    MySQL数据可视化
'''
class MySQLDataV():
    def __init__(self):
        pass

    #创建数据库连接
    def initconn(self):
        try:
            self.conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='root',db='mjoin')
            #对打开是否成功的测试
            if  not self.conn.open:
                print('Error Open')
            else:
                print('conn has sucessfuly open')
        except Exception,e:
            print(e.args[0],e.args[1])
            sys.exit()
        cur=self.conn.cursor()

    #mysql数据可视化
    def visual(self):
        self.cur.execute("select Name, Continent, Population, LifeExpectancy, GNP from country")
        rows= self.cur.fetchall()
        pdrows=[ [ij for ij in i] for i in rows]
        print(pdrows)
        df=pd.DataFrame(pdrows)
        df.rename(columns={0: 'Name', 1: 'Continent', 2: 'Population', 3: 'LifeExpectancy', 4:'GNP'}, inplace=True)
        df = df.sort(['LifeExpectancy'], ascending=[1])

        country_names = df['Name']
        for i in range(len(country_names)):
            try:
                country_names[i] = str(country_names[i]).decode('utf-8')
            except:
                country_names[i] = 'Country name decode error'
        trace1 = pc.Scatter(x=df['LifeExpectancy'], y=df['GNP'],text=country_names, mode='markers')
        layout = pc.Layout(xaxis=pc.XAxis( title='Life Expectancy' ),yaxis=pc.YAxis( type='log', title='GNP' ))
        data = pc.Data([trace1])
        fig = pc.Figure(data=data, layout=layout)
        plotly.offline.plot(fig, filename='world GNP vs life expectancy')


# 测试入口
if __name__ == "__main__":
    mysqldatav=MySQLDataV()
    mysqldatav.initconn()
    mysqldatav.visual()


