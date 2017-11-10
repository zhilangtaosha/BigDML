#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Fun: matplotlib条形图的绘制（注意和柱状图的区别）
    Ref:
    State：
    Date:2017/5/11
    Author:tuling56
'''
import re, os, sys
import hues
import numpy as np
import matplotlib.pyplot as plt

reload(sys)
sys.setdefaultencoding('utf-8')


# 基本条形图
def draw_bar():
    plt.rcdefaults()
    fig, ax = plt.subplots()

    # Example data
    people = ('Tom', 'Dick', 'Harry', 'Slim', 'Jim')
    y_pos = np.arange(len(people))
    performance = 3 + 10 * np.random.rand(len(people))
    error = np.random.rand(len(people))

    ax.barh(y_pos, performance, xerr=error, align='center',color='green', ecolor='red')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(people)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Performance')
    ax.set_title('How fast do you want to go today?')

    plt.show()

# 并行条形图
def draw_mutibar():
    n_groups = 5
    means_VotexF36 = (0.84472049689441, 0.972477064220183, 1.0, 0.9655172413793104, 0.970970970970971)
    means_VotexF50 = (1.0,              0.992992992992993, 1.0, 0.9992348890589136, 0.9717125382262997)
    means_VFH36    = (0.70853858784893, 0.569731081926204, 0.8902900378310215, 0.8638638638638638, 0.5803008248423096)
    means_VFH50    = (0.90786948176583, 0.796122576610381, 0.8475120385232745, 0.8873762376237624, 0.5803008248423096)

    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.3
    opacity   = 0.4

    rects1 = plt.bar(index,             means_VFH36,    bar_width/2, alpha=opacity, color='r', label='VFH36'   )
    rects2 = plt.bar(index+ bar_width/2,  means_VFH50,  bar_width/2, alpha=opacity, color='g', label='VFH50'   )
    rects3 = plt.bar(index+bar_width, means_VotexF36,     bar_width/2, alpha=opacity, color='c', label='VotexF36')
    rects4 = plt.bar(index+1.5*bar_width, means_VotexF50, bar_width/2, alpha=opacity, color='m', label='VotexF50')

    plt.xlabel('Category')
    plt.ylabel('Scores')
    plt.title('Scores by group and Category')

    #plt.xticks(index - 0.2+ 2*bar_width, ('balde', 'bunny', 'dragon', 'happy', 'pillow'))
    plt.xticks(index - 0.2+ 2*bar_width, ('balde', 'bunny', 'dragon', 'happy', 'pillow'),fontsize =18)
    plt.yticks(fontsize =18)  #change the num axis size

    plt.ylim(0,1.5)
    plt.legend()
    plt.tight_layout()
    plt.show()


#  堆叠条形图
def draw_overlab_bar():
    pass


# 测试入口
if __name__ == "__main__":
    #basic_plot()
    #medium_plot()
    #draw_bar()
    draw_mutibar()

