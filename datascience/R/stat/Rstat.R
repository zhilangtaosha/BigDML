# R统计基础
print(getwd())

fun.statbasic <- function(){
  #indata <- read.csv("src/git_data/rstat.csv")
  #indata <- read.table('src/git_data/rstat.csv',header=TRUE,sep=",")
  indata <- read.table(header = TRUE,sep = ",",text = "
                                    id,name,salary,start_date,dept
                                    1,Rick,623.3,2012-01-01,IT
                                    2,Dan,515.2,2013-09-23,Operations
                                    3,Michelle,611,2014-11-15,IT
                                    4,Ryan,729,2014-05-11,HR
                                    5,Gary,843.25,2015-03-27,Finance
                                    6,Nina,578,2013-05-21,IT
                                    7,Simon,632.8,2013-07-30,Operations
                                    8,Guru,722.5,2014-06-17,Finance")
  
  print(indata)
  retval <- subset(indata, salary == max(salary))
  retval <- subset(indata, as.Date(start_date) > as.Date("2014-01-01"))
  retval <- subset(indata, salary > 600 & dept == "IT")
  print(retval)
  write.csv(retval,"res/output.csv")  # 子结果写入
}

# 执行方法是先source之后再在
#fun.statbasic


fun.ddply <- function()
{
  library(ggplot2)
  library(plyr)
  #head(diamonds)
  print('按颜色分组，选出每组中carat最小')
  ddply(diamonds,.(color),subset,carat == max(carat))

}





