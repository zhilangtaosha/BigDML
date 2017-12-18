##Prophet笔记
[TOC]

### 基础

prophet处理的对象并非必须是日数据，当我们拟合年度效应时，只有每个月第一天的数据，而且对于其他天的周期效应是不可测且过拟合的。当你使用 Prophet 拟合月度数据时，可以通过在 `make_future_dataframe` 中传入频率参数只做月度的预测。

Prophet 提供了一个 `prophet` 函数去拟合模型并且返回一个模型对象，可以对这个模型对象执行“预测”（ `predict` ）和“绘图”（ `plot` ）操作

使用make_future_dataframe函数预测未来数据

使用prophet_plot_components(m,forecast)展示预测中的趋势、周效应和年度效应

```R
f.mprohet <- function()
{
 	# 读入数据集，并对日访问量y做对数处理
 	df <- read.csv('predict/prophet/data/example_wp_peyton_manning.csv') %>% mutate(y=log(y))

	# 模型拟合
	m <- prophet(df)

	# 构建待预测日期数据
	fucture <- make_future_dataframe(m,periods = 365)

	# 利用模型对预测数据集得到预测结果
	forcast <- predict(m,fucture)

	# 展示预测结果(包含以前的数据和预测的数据，如何区分开这两者呢)
 	plot(m,forcast,type='p',col.lab='red')
 	
 	# 预测趋势、周效应和年度效应
 	prophet_plot_components(m,forcast)

}
```

> 备注：
>
> - 趋势- 是按年度来展示
> - 周效应-一周内的变化情况
> - 年效应-一年内每天的变化情况

### 进阶

#### 预测增长

prophet默认使用线性模型进行预测增长，但是在实际情况下通常会存在可达到的最大极限值，所以选择logstatic模型，同时指定承载能力来进行增长预测

#### 趋势突变

##### 调整趋势的灵活性

自动监测突变点，并对趋势做适当调整，可以对突变点做一些调整来达到对趋势的更好控制

可以利用输入参数 `changepoint.prior.scale` 来调整稀疏先验的程度。默认下，这个参数被指定为 0.05 。 增加这个值，会导致趋势拟合得更加灵活。如下代码和图所示：

```R
f.mprohet_sudden <- function()
{
    # 读入数据集，并对日访问量y做对数处理
    df <- read.csv('predict/prophet/data/example_wp_peyton_manning.csv') %>% mutate(y=log(y))
    
    # 模型拟合(增加对趋势突变点的操作)
    m <- prophet(df,changepoint.prior.scale = 0.5)
    
    # 构建待预测日期数据
    fucture <- make_future_dataframe(m,periods = 365)
    
    # 利用模型对预测数据集得到预测结果
    forcast <- predict(m,fucture)
    
    # 展示预测结果(包含以前的数据和预测的数据，如何区分开这两者呢)
    plot(m,forcast,type='p',col.lab='red')
    
    # 预测趋势、周效应和年度效应
    prophet_plot_components(m,forcast)

}
```

![](http://img.dmc.csdn.net/6723E1796D4B94F43EA49AAEA72E9DE6.png)



减少这个值，会导致趋势拟合的灵活性降低，如下

```R
    m <- prophet(df,changepoint.prior.scale = 0.5)
    
    # 构建待预测日期数据
    fucture <- make_future_dataframe(m,periods = 365)
    
    # 利用模型对预测数据集得到预测结果
    forcast <- predict(m,fucture)
    
    # 展示预测结果(包含以前的数据和预测的数据，如何区分开这两者呢)
    plot(m,forcast,type='p',col.lab='red')
```

![趋势灵活性降低](http://img.dmc.csdn.net/88B65641C583C2D6A6E1B67D971DCD33.png)

##### 指定突变点的位置

手动指定突变的位置，而不是利用自动的突变点监测，可以使用changepoints参数

```R
f.mprohet_sudden <- function()
{
    # 读入数据集，并对日访问量y做对数处理
    df <- read.csv('predict/prophet/data/example_wp_peyton_manning.csv') %>% mutate(y=log(y))
    
    # 模型拟合(手工指定突变点的位置)
    m <- prophet(df,changepoints=c(as.Data('2015-01-01')))
    
    # 构建待预测日期数据
    fucture <- make_future_dataframe(m,periods = 365)
    
    # 利用模型对预测数据集得到预测结果
    forcast <- predict(m,fucture)
    
    # 展示预测结果(包含以前的数据和预测的数据，如何区分开这两者呢)
    plot(m,forcast,type='p',col.lab='red')
    
    # 预测趋势、周效应和年度效应
    prophet_plot_components(m,forcast)

}
```

![手工指定突变点的位置](http://img.dmc.csdn.net/C79CE4110CBB0392EED3C68A3D5A238A.png)

#### 节假日效应

需要手工指定节假日的日期，并同时条件节假日的敏感度

```R
 playoffs <- data_frame(
        holiday = 'playoff',
        ds = as.Date(c('2008-01-13', '2009-01-03', '2010-01-16',
                       '2010-01-24', '2010-02-07', '2011-01-08',
                       '2013-01-12', '2014-01-12', '2014-01-19',
                       '2014-02-02', '2015-01-11', '2016-01-17',
                       '2016-01-24', '2016-02-07')),
        lower_window = 0,
        upper_window = 1
    )
    superbowls <- data_frame(
        holiday = 'superbowl',
        ds = as.Date(c('2010-02-07', '2014-02-02', '2016-02-07')),
        lower_window = 0,
        upper_window = 1
    )
    holidays <- bind_rows(playoffs, superbowls)

    # 预测时指定使用节假日效应
    m <- prophet(df, holidays = holidays,holidays.prior.scale = 1)
    future <- make_future_dataframe(m,periods =365 )
    forecast <- predict(m, future)

    # 查看效果
    forecast %>%
        select(ds, playoff, superbowl) %>%
        filter(abs(playoff + superbowl) > 0) %>%
        tail(10)

    # 趋势和效应
    prophet_plot_components(m,forecast)

    #预测
    # plot(m,forecast)

```

通过`holidays.prior.scale`设置节假日的先验规模来避免节假日效应被过度拟合，来达到平滑的目的， 该值默认取10

类似的，还有一个 `seasonality.prior.scale` 参数可以用来调整模型对于季节性的拟合程度。

#### 预测区间

##### 趋势中的不确定性

##### 季节效应中的不确定性



 ##参考

[Prophet的Facebook官网](https://facebook.github.io/prophet/)

[Prophet的Github主页](https://github.com/facebook/prophet)

[Python的Prophet官网](http://prophet.michaelsu.io/en/latest/)

[官方说明文档|手把手教你在R中Prophet](http://ms.csdn.net/geek/198166)

[知乎Prophet预测效果讨论](https://www.zhihu.com/question/56585493)