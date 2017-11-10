#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能：Python数据可视化：matplotlib实现
  参考：http://www.shareditor.com/blogshow/?blogId=55
       http://www.toutiao.com/i6410597836664078849/
       http://matplotlib.org/examples
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

'''
    基本使用
'''
def basic_plot():
    # 多维数组
    '''
    ldata=[1,2,7,3,8,4,5,5,6,10]
    ndata=np.array(ldata)
    plt.plot(ndata,np.sin(ndata),'--',linewidth=2,color='red')
    plt.show()
    '''

    x=[2,5,3,42,1,5]
    y1=[23,34,3,54,64,1]
    y2=[ v*np.sin(v) for v in y1]

    # 折线图
    '''
    plt.figure()
    plt.plot(x,y1,'o')
    plt.plot(x,y2,'--',linewidth=2,color='red')
    plt.xlabel(u'x轴')
    plt.ylabel(u'y轴(y1,y2)')
    plt.title(u'标题')
    plt.show()
    '''

    # 柱状图
    '''
    plt.figure()
    plt.bar(x,y1)
    plt.show()
    '''

    # 饼图
    plt.figure()
    labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
    sizes = [15, 30, 45, 150]
    explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
    plt.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',shadow=False, startangle=90,pctdistance=0.6)
    plt.axis('equal')         # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()


'''
    中级使用
'''
def medium_plot():
    #子图
    x=range(5)
    y1=[v+2 for v in x ]
    y2=[v+3 for v in x ]
    plt.figure()

    '''
    plt.subplot(211)
    plt.plot(x,y1)
    plt.xlabel('xsub1')
    plt.ylabel('ysub1')
    plt.title('titlesub1')

    plt.subplot(212)
    plt.plot(x,y2)
    plt.xlabel('xsub2')
    plt.ylabel('ysub2')
    plt.title('titlesub2')
    plt.show()
    '''

    #图例
    plt.plot(x,y1,label='tu1')
    plt.plot(x,y2,label='tu2')
    plt.legend()
    plt.show()




# 测试入口
if __name__ == "__main__":
    basic_plot()
    #medium_plot()


