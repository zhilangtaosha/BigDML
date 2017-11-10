#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：HMM的Viterbi实现,由显示的活动推测天气状态
  Source: http://www.hankcs.com/nlp/hmm-and-segmentation-tagging-named-entity-recognition.html
'''

#HMM构成
states=('Rainy','Sunny')
observations=('walk','shop','clean')
start_probability={'Rainy':0.6,'Sunny':0.4}
transition_probability={'Rainy':{'Rainy':0.7,'Sunny':0.3},
                        'Sunny':{'Rainy':0.4,'Sunny':0.6}
                       }
emission_probability={
'Rainy':{'walk':0.1,'shop':0.4,'clean':0.5},
'Sunny':{'walk':0.6,'shop':0.3,'clean':0.1}
}

# 打印路径概率表
def print_dptable(V):
    print " ",
    for i in range(len(V)):
        print"%7d" %i,
        print
    for y in V[0].keys():
        print"%.5s:"%y,
        for t in range(len(V)):
            print"%.7s" %("%f"%V[t][y]),
            print

#viterbi算法
def viterbi(obs,states,start_p,trans_p, emit_p):
    """
    :param obs:观测序列
    :param states:隐状态
    :param start_p:初始概率（隐状态）
    :param trans_p:转移概率（隐状态）
    :param emit_p: 发射概率 （隐状态表现为显状态的概率）
    :return:
    """
    #路劲概率表V[时间][天气]=概率
    V=[{}]
    path={}
    #初始化状态
    for y in states: #隐藏状态：天气是晴还是下雨
        V[0][y]=start_p[y]*emit_p[y][obs[0]] #在y天气下进行散步的概率
        path[y]=[y]  #天气路径，初始状态是晴


    for t in range(1,len(obs)): #观察状态，散步，购物还是清理房间
        V.append({})
        newpath={}
        for y in states:
            (prob, state) = max([(V[t - 1][y0] * trans_p[y0][y] * emit_p[y][obs[t]], y0) for y0 in states])
            #记录最大概率
            V[t][y]=prob #这一天最可能是天气y，其概率是prob
            newpath[y]=path[state]+[y]  #更新天气路径
        #不需要保留就路径
        path=newpath
    print_dptable(V)
    (prob, state) = max([(V[len(obs) - 1][y], y) for y in states])  #选取最后一天概率最大的
    return (prob, path[state])                                        #然后返回怎么样达到该状态的最短路径，其实也是最大概率

if __name__=='__main__':
    print viterbi(observations,states,start_probability,transition_probability,emission_probability)

def run():
    print("hello")


if __name__ == "__main__":
    run()
