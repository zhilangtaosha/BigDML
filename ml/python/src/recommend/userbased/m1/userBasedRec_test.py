# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：基于用户的协同过滤推荐系统
            作为练手使用
'''

from math import  sqrt

from PythonML.src.recommend.userbased.m1.data import  dataset



#利用欧式距离求相似性
def sim_socre(person1,person2):

    #先进行粗略的判断
    both_shared=[]
    for item in dataset[person1]: #person1看过的内容
        if item in dataset[person2]:
            both_shared[item]=1; #两者都看过的电影标记为1
    if len(both_shared)==0:
        return  0; #如果两者没有共同看过的电影

    #若存在相似性，则详细求解
    sum_of_eclidian_diatance=[]
    for item in dataset[person1]:
        if item in dataset[person2]:
            sum_of_eclidian_diatance.append(pow(dataset[person1][item]-dataset[person2][item],2))

    sum_of_eclidian_diatance=sum(sum_of_eclidian_diatance) #列表求和
    return  1/(1+sqrt(sum_of_eclidian_diatance)) #从反向说明了结果的输入

#pearson相关系数求相似性
def sim_socre_pearson(person1,person2):
    both_shared={} #以字典的方式
    for item in dataset[person1]:
        if item in dataset[person2]:
            both_shared[item]=1
    if len(both_shared)==0:
        return  0;

    #列表推导式子
    p1_like_sum=sum([dataset[person1][item] for item in both_shared])
    p2_like_sum=sum([dataset[person2][item] for item in both_shared])

    #map操作
    p1_like_ssum=sum([pow(dataset[person1][item],2) for item in both_shared])
    p2_like_ssum=sum([pow(dataset[person2][item],2) for item in both_shared])

    p1_p2_sum=0;
    for item in both_shared:
        p1_p2_sum+=dataset[person1][item]*dataset[person2][item]

    #pearson correction
    p1p2=p1_p2_sum-p1_like_sum*p2_like_sum/len(both_shared)
    p1=p1_like_ssum-pow(p1_like_sum,2)/len(both_shared)
    p2=p2_like_ssum-pow(p2_like_sum,2)/len(both_shared)

    pearson_sim=p1p2/sqrt(p1*p2)
    return  pearson_sim

#求最相似的TopN邻居(字典方法)
def findSimNeighbor(person,k):
    neighbours_sim={}
    for item in dataset.keys():
        if item!=person:
            neighbours_sim[item]=sim_socre_pearson(person,item)
    #字典排序
    sorted_neighbours=sorted(neighbours_sim.iteritems(),key=lambda asd:asd[1],reverse=True)
    #但是字典是无序的，如何将结果传出
    neighbours_List=list(sorted_neighbours)
    return  neighbours_List[0:k]


#求最相似的topN(列表方法)
#期望的输出结果：
#[(0.991240, 'Toby'), (0.74701788, 'Jack Matthews'), (0.5940885, 'Mick LaSalle')]
def findSimNeighbor_list(person,k):
    scores=[(sim_socre_pearson(person,other_person),other_person) for other_person in dataset.keys() if other_person!=person ] #求相似性列表
    #列表排序
    scores.sort()
    scores.reverse()
    return scores[0:k]


#计算推荐列表
def recommond_list(person):
    #neighbors_L=findSimNeighbor(person,3) #其中3代表寻找最近的3个邻居
    totals={}
    simSums={}
    rankings_list=[]
    for other in dataset: #数据库中的其它人
        if person==other:
            continue
        sim=sim_socre_pearson(person,other)
        if sim<0:
            continue
        for item in dataset[other]:
            if item not in dataset[person] or dataset[person][item]==0: #对打0分的情况
                totals.setdefault(item,0)
                totals[item]+=dataset[other][item]*sim #计算推荐指数（打分*相似性系数）
                simSums.setdefault(item,0)
                simSums[item]+=sim #计算该物品所有推荐人与查询者的相似性和

    # normalized list
    rankings=[(total/simSums[item],item) for item,total in totals.items()]
    rankings.sort()
    rankings.reverse()
    recom_lists=[recom_item for score,recom_item in rankings] #列表推导式
    return  recom_lists


if __name__ == "__main__":
    recommond_list('Toby')
