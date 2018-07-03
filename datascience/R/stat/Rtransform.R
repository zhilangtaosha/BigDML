# R transform 数据转换
library(ggplot2)
library(reshape2)

# 获取和设置目录
getwd()
#setwd('E:/OneDrive - std.uestc.edu.cn/Code/Git/R/study/stat')

# 演示数据加载
fun.load_example_data <- function()
{
  d1 <- data.frame(sex=c("M","M","F","F","M"),
                   Color=c("green","blue","green","red","blue"),
                   Freq=c(0,1,3,1,2))
  table(d1)

  olddata_wide <- read.table(header=TRUE, text='
                             subject sex control cond1 cond2
                             1   M     7.9  12.3  10.7
                             2   F     6.3  10.6  11.1
                             3   F     9.5  13.1  13.8
                             4   M    11.5  13.4  12.9
                             ')
  olddata_wide$subject <- factor(olddata_wide$subject)  # Make sure the subject column is a factor（下同）

  olddata_long <- read.table(header=TRUE, text='
                             subject sex condition measurement
                             1   M   control         7.9
                             1   M     cond1        12.3
                             1   M     cond2        10.7
                             2   F   control         6.3
                             2   F     cond1        10.6
                             2   F     cond2        11.1
                             3   F   control         9.5
                             3   F     cond1        13.1
                             3   F     cond2        13.8
                             4   M   control        11.5
                             4   M     cond1        13.4
                             4   M     cond2        12.9
                             ')
  olddata_long$subject <- factor(olddata_long$subject)

}


# 揉数据(以xmp数据卫卫显卡和rmvb关联为例)
fun.datatranform_stat2<-function()
{

  #分组汇总
  sstar <- read.table('data/wwxianka.data',header = T,sep='\t')
  colnames(sstar) <- c('date','channel','dpv','duv')
  sstar$date <-as.Date(as.character(sstar$date),'%Y%m%d')
  sstar_sort <- sstar[order(sstar$channel,na.last = FALSE),]
  g<-ggplot(sstar_sort,aes(x=date))
  g+geom_line(aes(y=duv,colour=channel))+facet_grid(channel~.,scales = 'free_y')+geom_point(aes(y=duv))
  print(g)


  # 行列互转
  wwrmvb<-read.table("data/rmvbres.data",header = T,fileEncoding="utf8") #stringsAsFactors=FALSE, )
  wwrmvb$date <-as.Date(as.character(wwrmvb$date),'%Y%m%d')

  ## 绘图
  g<-ggplot(wwrmvb,aes(x=date))
  g+geom_line(aes(y=cnt,colour=player))+facet_grid(player~.,scales = 'free_y')
  print(g)

  ## 结果转换和保存
  res<-t(dcast(wwrmvb,formula = player~date))
  write.table(res,file='data/wwrmvb_tr.data',row.names = T,col.names=F,quote = F,fileEncoding='utf8',sep='\t')
  res<-read.table("data/wwrmvb_tr.data",header = T,fileEncoding="utf8") #stringsAsFactors=FALSE, )
  write.csv(res,file='data/wwrmvb_tr.csv',row.names = F,quote = F,fileEncoding='utf8')

}


# 揉数据(以kpi数据为例)
fun.datatranform_stat3<-function()
{
  library(reshape2)

  ## 长格式转宽格式
  tmp<-dcast(row2col,mon~week,na.rm=TRUE)
  row.names(tmp)=tmp[['mon']]
  res=tmp[c("Mon","Tue","Wed","Thu","Fri","Sat","Sun")] # 选取指定的列

  #--- 最后的结果形式如下
  #
  #              Mon      Tue      Wed      Thu      Fri      Sat      Sun
  #  201606       NA       NA       NA       NA       NA       NA 43271933
  #  201607 43849688 44276770 44819289       NA 44190928       NA 46551557
  #  201608 43477346 45188957 44567973 44699149 43650183 45116368 46840558

}