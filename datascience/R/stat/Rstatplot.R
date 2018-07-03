# R统计绘图-基础版
library(ggplot2)
library(reshape2)
library(plotly)

# R统计绘图
fun.statplot <- function()
{
  full <- warpbreaks
  # 累积柱图
  barplot(table(full$wool, full$tension), sub="Survival by Title", ylab="number of passengers", col=c("steelblue4","steelblue2"))
  legend("topleft",legend = c("Died","Survived"),fill=c("steelblue4","steelblue2"),inset = .05)

  # 比例柱图
  barplot(prop.table(table(full$wool, full$tension),2), sub="Survival by Title", ylab="number of passengers", col=c("steelblue4","steelblue2"))
  legend("topleft",legend = c("Died","Survived"),fill=c("steelblue4","steelblue2"),inset = .05)

  library('ggthemes')
  ggplot(full, aes(x = Title, fill = factor(Survived))) + geom_bar(stat='count', position='fill') + theme_few()

  # 决策图（有问题）
  library("rpart")
  library("rpart.plot")
  my_tree <- rpart(Fare ~ Pclass + Fsize + Embarked, data = train, method = "class", control=rpart.control(cp=0.0001))
  prp(my_tree, type = 4, extra = 100)
}

# 饼图绘制
fun.statpie <- function()
{
  speeddur=table(cut(cars$speed,5))
  speeddur <- as.data.frame(speeddur)
  speedpercent=round(speeddur$Freq*100/sum(speeddur$Freq),2)

  # 图保存
  png(file = "cars.png")
  pie(speeddur$Freq,labels =speedpercent,main='车速分布',col=factor(speeddur$Var1))
  legend(x=1,y=1,speeddur$Var1, cex=0.8,fill=factor(speeddur$Var1))
  dev.off()
  print("zhengquebnaoc")
}