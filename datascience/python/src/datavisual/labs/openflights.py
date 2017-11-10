#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：
'''
import  sys
import matplotlib.pyplot as plt
sys.path.append("..\\..\\..\\data")

#（1）数据导入.
import pandas
# Read in the airports data.
airports=pandas.read_csv("..\\..\\..\\data\\airports.dat",header=None,dtype=str) # 按字符串读取
airports.columns=["id","name","city","country","code","icao","latitude","longitude","altitude","offset","dst","timezone"] #设置列名
# Read in the airlines data.
airlines=pandas.read_csv("..\\..\\..\\data\\airlines.dat",header=None,dtype=str)
airlines.columns=["id","name","alias","iata","icao","callsign","country","active"]
# Read in the routes data.
routes=pandas.read_csv("..\\..\\..\\data\\routes.dat",header=None,dtype=str)
routes.columns=["airline","airline_id","source","source_id","dest","dest_id","codeshare","stops","equipment"]
#数据清洗
routes=routes[routes["airline_id"] != "\\N"]

#(2) 计算距离
import math
def haversine(lon1,lat1,lon2,lat2):
    # Convert coordinates to floats.
    lon1,lat1,lon2,lat2=[float(lon1),float(lat1),float(lon2),float(lat2)]
    #  Convert to radians from degrees.
    lon1,lat1,lon2,lat2=map(math.radians,[lon1,lat1,lon2,lat2])

    # Compute distance.
    dlon=lon2-lon1
    dlat=lat2-lat1
    a=math.sin(dlat/ 2) ** 2+math.cos(lat1)* math.cos(lat2)* math.sin(dlon / 2) ** 2
    c=2 * math.asin(math.sqrt(a))
    km=6367 * c
    return km

def calc_dist(row):
    dist=0
    try:
        # Match source and destination to get coordinates.
        source=airports[airports["id"]==row["source_id"]].iloc[0]
        dest=airports[airports["id"]==row["dest_id"]].iloc[0]
        # Use coordinates to compute distance.
        dist=haversine(dest["longitude"],dest["latitude"],source["longitude"],source["latitude"])
    except(ValueError,IndexError):
        pass
    return dist

routes_length=routes.apply(calc_dist,axis=1)

#（3） 绘图控制
# 柱状图
def plot_hist():
    plt.hist(routes_length,bins=20)
    plt.show()

# 模拟图
def curline():
    %matplotlib inline
    import seaborn
    seaborn.distplot(routes_length,bins=20)

# 条形图（实现分类汇总）
def bar():
    import numpy
    # Put relevant columns into a dataframe.
    route_length_df=pandas.DataFrame({"length":routes_length,"id":routes["airline_id"]}) #长度和id
    # Compute the mean route length per airline.
    airline_route_lengths=route_length_df.groupby("id").aggregate(numpy.mean)  # 按id聚合求长度
    # Sort by length so we can make a better chart.
    airline_route_lengths=airline_route_lengths.sort("length",ascending=False)
    plt.bar(range(airline_route_lengths.shape[0]),airline_route_lengths["length"])


if __name__ == "__main__":
    bar()
