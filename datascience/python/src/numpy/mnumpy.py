#-*-coding:utf-8-*-
__author__ = 'yjm'
'''
  功能注释：numpy的数据结构ndarray
'''

import os
import sys
import numpy as np

reload(sys)
sys.setdefaultencoding('utf-8')


'''
    numpy使用基本例子
'''
#不使用numpy(zip函数相当于对两个列表进行解包)
def mvectoradd(n):
    itemlist=range(n)
    a= [item**2 for item in itemlist]  #回家在囊
    b=[item**3 for item in itemlist]
    ab=[]
    for aitem,bitem in zip(a,b):
        temp=aitem+bitem
        ab.append(temp)
    print a,'\n',b,'\n',ab

#使用numpy(相当于运算符重载)
def mvectoradd_numpy(n):
    a=np.arange(n)**2
    b=np.arange(n)**3
    c=a+b
    print(c)

'''
    numpy基本语法
'''

# 构建多维数组
def mnmpy():
    a = np.array([[[2,3,4,4],[4,5,6,6],[7,8,9,9]]
                    ,[[0,1,2,2],[3,4,5,8],[6,7,8,8]]
                    ,[[0,1,2,2],[3,4,5,8],[6,7,8,8]]
                    ,[[0,1,2,2],[3,4,5,8],[6,7,8,8]]
                    ])
    print a, a.shape,type(a)
    #数组展平
    print a.flatten()

    #数组按行列累计求和
    print np.cumsum(a,axis=0)


# numpy数据类型转换
def numpyconver():
    # 数字转字符串
    #x=np.ones((100,100))*-99
    #x=x.astype(np.str)
    #print x

    # 数字直接不同精度转换
    a=np.array([['-0.022','12','23','0.5'],
               ['-0.022','','213.2','0.5']])
    a[a=='']='0.0'
    print a.astype(np.float)
    #print map(float,a[0])

# numpy数据保存
def numpynum():
    a = np.asarray(((1,2.2,3,2.232),(4,5,6,0.5656565)))
    np.savetxt(sys.stdout, a,delimiter=',',fmt='%d %5.4f %d %4.2f')


# numpy字符串类型
def numpyarr():
    names = np.array([['Bob', 'Joe', 'Will','zhang'], ['Bob', 'Will', 'Joe', 'Joe']])
    print names
    np.savetxt(sys.stdout,names,delimiter=',',newline='\n',fmt='%-06s')

if __name__ == "__main__":
    #mnmpy()
    #mvectoradd(6)
    #mvectoradd_numpy(6)
    #numpyconver()
    numpyarr()
