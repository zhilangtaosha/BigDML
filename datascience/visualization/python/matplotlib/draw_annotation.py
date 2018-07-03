#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Fun:绘制图形标注
    Ref:
    State：
    Date:2017/5/11
    Author:tuling56
'''
import re, os, sys
import hues
import matplotlib.pyplot as plt

reload(sys)
sys.setdefaultencoding('utf-8')


'''
    绘图和标注(smdata,onediff都是OrderDict)
'''
def draw_annotation(view,onediff,smdata,peeks,high,cid,filesize,flag):
    smdata_x=map(lambda x:x[0],smdata.items())
    smdata_y=map(lambda x:x[1],smdata.items())
    onediff_x=map(lambda x:x[0],onediff.items())
    onediff_y=map(lambda x:x[1],onediff.items())
    peeks_x=map(lambda x:x[0],peeks.items())
    peeks_o=map(lambda x:x[1],peeks.items())

    # 差分统计
    mean_onediffv=sum(onediff_y)/len(onediff_y)
    max_onediffv=max(onediff_y)
    min_onediffv=min(onediff_y)
    threshhold=(max_onediffv-min_onediffv)/5

    # 求波峰点的差分数据
    peeks_diff=[]
    for p in peeks_x:
        if onediff.has_key(p):
            peeks_diff.append(onediff[p])
        elif p==smdata_x[-1]:
            peeks_diff.append(smdata_y[-1])  # smdata最后一点是波峰点，但没有差分数据,用原始数据代替差分数据
        else:
            print "wrong peek find"
            exit()

    # 图像设置
    plt.figure(figsize=(15,7))  # figsize()设置的宽高比例是是15:7，图片的尺寸会根据这个比例进行调节
    #plt.xlim(-3,19)
    lowlimit=min(onediff_y)-500 #y轴下限
    highlimit=max(view)+500     #y轴上限
    plt.ylim(lowlimit,highlimit)
    plt.grid(which='both')
    #plt1 = plt.subplot(2,2,1) # 在一张图上绘制多个子图


    #绘制结果数据
    plt.plot(range(1,len(view)+1),view,color='y',lw=0.5,label='origin')  # 原始图像
    plt.plot(smdata_x,smdata_y,'ro-',ms=3,label='smooth')                # 平滑后的数据
    plt.plot(onediff_x,onediff_y,'go-',ms=3,label='onediff')             # 一阶差分
    plt.plot(peeks_x,peeks_o,'r^',ms=9,label='peak')                     # (原曲线上）绘制峰
    plt.plot(peeks_x,peeks_diff,'g^',ms=9,label='diff_peak')             # (差分线上) 绘制峰,差分线的最后一点
    plt.legend(loc='upper right')
    plt.xlabel('time (s)')
    plt.ylabel('views')
    plt.title(flag)

    # 差分线标注
    plt.axhline(y=max_onediffv,lw=1,ls='-.',color='r')  # 差分上限
    plt.axhline(y=min_onediffv,lw=1,ls='-.',color='r')  # 差分下限
    plt.axhline(y=mean_onediffv,lw=1,ls='-.',color='r') # 差分均值
    plt.axhline(y=threshhold,lw=2,ls='--',color='b')    # 差分上阈值
    plt.axhline(y=-threshhold,lw=2,ls='--',color='b')   # 差分下阈值
    plt.axhline(y=0,lw=2,color='k')

    # 标注高潮区间
    for item in high:
        #plt.axvline(x=item[0],lw=2)
        #plt.axvline(x=item[1],lw=2)
        plt.annotate('',xy=(item[1],1000),xytext=(item[0],1000),arrowprops=dict(arrowstyle="->",connectionstyle="arc3"))
        plt.fill_betweenx([lowlimit,highlimit],item[0], item[1], linewidth=1, alpha=0.2, color='r')

    plt.show()

    # 结果保存
    '''
    despath='D:\\hot_pic1'
    if not os.path.exists(despath):
        os.makedirs(despath)
    fname=os.path.join(despath,cid+'.'+str(filesize)+'.jpg')
    print fname
    plt.savefig(fname,dpi = 300)
    plt.close()
    '''

    return 0


if __name__ == "__main__":
    draw_annotation()

