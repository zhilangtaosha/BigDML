# plot
f.plot <- function()
{
  
  
}


f.dotchart <- function()
{
  ## 基本实现，可用于检测离群点 
  dotchart(mtcars$mpg,labels=row.names(mtcars),cex=.7, main="Gas Milage for Car Models",xlab="Miles Per Gallon") 

  
  ## 按mpg进行排序，按cylinder进行分组并设定不同的颜色，可用于确定聪明变量 
  x <- mtcars[order(mtcars$mpg),] # sort by mpg 
  x$cyl <- factor(x$cyl) # it must be a factor 
  x$color[x$cyl==4] <- "red" 
  x$color[x$cyl==6] <- "blue" 
  x$color[x$cyl==8] <- "darkgreen"  
  dotchart(x$mpg,labels=row.names(x),cex=.7,groups= x$cyl,main="Gas Milage for Car Models\ngrouped by cylinder",xlab="Miles Per Gallon", gcolor="black", color=x$color)
}



f.pie <- function()
{
  ## 基本实现，绘制饼图并设置标签 
  slices <- c(10, 12,4, 16, 8) 
  lbls <- c("US", "UK", "Australia", "Germany", "France") 
  pie(slices, labels = lbls, main="Pie Chart of Countries") 
  
  
  
  ## 设置百分比标签、颜色 
  slices <- c(10, 12, 4, 16, 8)  
  lbls <- c("US", "UK", "Australia", "Germany", "France") 
  pct <- round(slices/sum(slices)*100) 
  lbls <- paste(paste(lbls, pct) ,"%",sep="") # ad % to labels  
  pie(slices,labels = lbls, col=rainbow(length(lbls)),main="Pie Chart of Countries")  
  
  
  
  ## 3D饼图 
  library(plotrix) 
  slices <- c(10, 12, 4, 16, 8)  
  lbls <- c("US", "UK", "Australia", "Germany", "France") 
  pie3D(slices,labels=lbls,explode=0.1,main="Pie Chart of Countries ") 
}


f.scatter <- function()
{
  ## 基本实现-使用plot() 
  plot(mtcars$wt, mtcars$mpg, main="Scatterplot Example", xlab="Car Weight ", ylab="Miles 
Per Gallon ", pch=19) 
  abline(lm(mtcars$mpg~mtcars$wt), col="red") # 添加回归线 
  
  
  
  ## 散点图矩阵 
  pairs(~mpg+disp+drat+wt,data=mtcars, main="Simple Scatterplot Matrix") 
  
  
  
  ## 3D散点图 
  library(scatterplot3d) 
  scatterplot3d(mtcars$wt,mtcars$disp,mtcars$mpg, main="3D Scatterplot") 
}


f.coplot <- function(){
  ## 单个条件变量的条件图 
  coplot(mtcars$wt ~ mtcars$mpg | 
           as.factor(mtcars$cyl), main="", xlab="", ylab="", 
         pch=19) 
  
  
  
  ## 两个条件变量的条件图 
  coplot(mtcars$wt ~ mtcars$mpg | 
           as.factor(mtcars$cyl) * as.factor(mtcars$vs), 
         main="", xlab="", ylab="", pch=19) 
}


# 直方图绘制
f.hist <- function()
{
  # Create data for the graph.
  v <-  c(9,13,21,8,36,22,12,41,31,33,19)
  
  # Give the chart file a name.
  #png(file = "histogram.png")
  
  # Create the histogram.
  #hist(v,xlab="Weight",col="yellow",border="blue")  
  
  # 直方图指定间隔怎么做？
  hist(v,breaks=c(1,20,50),freq=TRUE,xlab="Weight")# ,col="yellow",border="blue")  
  
  # Save the file.
  #dev.off()
}


#f.dotchart
#f.pie
f.scatter
f.coplot