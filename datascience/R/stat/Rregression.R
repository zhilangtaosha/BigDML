# R回归分析

library(reshape2)
library(plyr)

# cars数据集
fun.rcars <- function()
{

  data <- head(cars)
  print(data)
  print("这是R回归分析")

}

# diamonds数据集(包含在ggplot2软件包中)
fun.rdiam <- function()
{
  library(ggplot2)
  set.seed(1002)
  dsmall <- diamonds[sample(nrow(diamonds),100),]
  # loess
  qplot(carat,price,data=dsmall,geom=c("point","smooth"),span=0.5) # 默认的平滑使用的loess,span参数控制平滑程度
  
  
  # gam
  qplot(carat,price,data=dsmall,geom=c("point","smooth"),method="gam",formula=y~s(x))         # gam
  qplot(carat,price,data=dsmall,geom=c("point","smooth"),method="gam",formula=y~s(x,bs="cs")) # gam 大数据使用
  
  # lm
  qplot(carat,price,data=dsmall,geom=c("point","smooth"),method="lm",formula=y~x)             # lm 线性拟合
  qplot(carat,price,data=dsmall,geom=c("point","smooth"),method="lm",formula=y~poly(x,5))     # lm 多项式拟合
  library(splines)
  qplot(carat,price,data=dsmall,geom=c("point","smooth"),method="lm",formula=y~ns(x,5))       # lm 多项式样条拟合
  
  # rlm
  library(MASS)
  qplot(carat,price,data=dsmall,geom=c("point","smooth"),method="rlm",formula=y~ns(x,5))       # rlm对噪声不敏感
}