#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Fun:测试混淆矩阵的使用
    Ref:
    Date:2016/9/23
    Author:tuling56
'''
import os
import sys
import re

reload(sys)
sys.setdefaultencoding('utf-8')
import numpy as np

'''
    基本使用
'''
from sklearn import metrics
def mmetrics():
    true_v=[[0,0,1],[0,1,0],[1,0,0],[1,0,0],[0,1,0]]  #映射成ABC
    #predict_v=[[0,0,1],[0,1,0],[1,0,0],[1,0,0],[0,1,0]]
    #true_v=['C','A','D','B']
    #predict_v=['C','A','A','A']
    #print metrics.confusion_matrix(true_v, predict_v)#,labels=true_v)

    # 列表到字典的反向映射
    #labelv[ord(label)-ord('A')]=1
    #true_v_lable=[ chr(l.index(1)+65) for l in true_v ]  #转换
    true_v_lable=map(lambda x:chr(x.index(1)+65),true_v)
    print true_v_lable

    true_v_array=np.array(true_v)
    #np数组如何对每一行进行操作
    print true_v_array.tolist()

'''
    计算精确度
'''
def calc_pre():
    mm=np.array([[164,2,8,2],[3,143,6,1],[4,5,336,4],[2,6,5,208]],dtype=np.float32)
    right=np.diag(mm)
    true_all=mm.sum(1)
    pre_all=mm.sum(0)

    print "准确率：",right/pre_all
    print "召回率：",right/true_all



if __name__ == "__main__":
    #mmetrics()
    calc_pre()

