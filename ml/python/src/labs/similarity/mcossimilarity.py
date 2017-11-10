#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Fun:相似性计算
    Ref:
    Date:2016/10/13
    Author:tuling56
'''
import os
import sys
import math

reload(sys)
sys.setdefaultencoding('utf-8')


'''
    Part1:相似性计算
'''
#   使用 |A&B|/sqrt(|A || B |)计算余弦距离
def calcCosDistSpe(user1,user2):
    avg_x=0.0
    avg_y=0.0
    for key in user1:
        avg_x+=key[1]
    avg_x=avg_x/len(user1)

    for key in user2:
        avg_y+=key[1]
    avg_y=avg_y/len(user2)

    u1_u2=0.0
    for key1 in user1:
        for key2 in user2:
            if key1[1] > avg_x and key2[1]>avg_y and key1[0]==key2[0]:
                u1_u2+=1
    u1u2=len(user1)*len(user2)*1.0
    sx_sy=u1_u2/math.sqrt(u1u2)
    return sx_sy

#   计算余弦距离
def calcCosDist(user1,user2):
    sum_x=0.0
    sum_y=0.0
    sum_xy=0.0
    for key1 in user1:
        for key2 in user2:
            if key1[0]==key2[0] :
                sum_xy+=key1[1]*key2[1]
                sum_y+=key2[1]*key2[1]
                sum_x+=key1[1]*key1[1]

    if sum_xy == 0.0 :
        return 0
    sx_sy=math.sqrt(sum_x*sum_y)
    return sum_xy/sx_sy

#   相似余弦距离
def calcSimlaryCosDist(user1,user2):
    sum_x=0.0
    sum_y=0.0
    sum_xy=0.0
    avg_x=0.0
    avg_y=0.0
    for key in user1:
        avg_x+=key[1]
    avg_x=avg_x/len(user1)

    for key in user2:
        avg_y+=key[1]
    avg_y=avg_y/len(user2)

    for key1 in user1:
        for key2 in user2:
            if key1[0]==key2[0] :
                sum_xy+=(key1[1]-avg_x)*(key2[1]-avg_y)
                sum_y+=(key2[1]-avg_y)*(key2[1]-avg_y)
        sum_x+=(key1[1]-avg_x)*(key1[1]-avg_x)

    if sum_xy == 0.0 :
        return 0
    sx_sy=math.sqrt(sum_x*sum_y)
    return sum_xy/sx_sy


if __name__ == "__main__":
    pass

