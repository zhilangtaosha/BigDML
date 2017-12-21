#!/usr/bin/RScript
# Ref:http://ms.csdn.net/geek/198166


library(prophet)
library(dplyr)

f.mprohet_predict <- function()
{
 	# 读入数据集，并对日访问量y做对数处理
 	#df <- read.csv('predict/prophet/data/example_wp_peyton_manning.csv') %>% mutate(y=log(y))
 	df <- read.csv('predict/prophet/data/xmp_dau',sep = '\t') %>% mutate(y=log(y))

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

f.mprohet_limit <- function()
{
    # 读入数据集，并对日访问量y做对数处理
    df <- read.csv('predict/prophet/data/example_wp_R.csv') %>% mutate(y=log(y))

    # 指定承载能力
    df$cap <- 8.5

    # 指定使用logistic增长
    m <- prophet(df,growth = 'logistic')

    #　预测数据集
    future <- make_future_dataframe(m,periods = 1826)
    future$cap=8.5

    forcast  <- predict(m,future)

    plot(m,forcast)
}

f.mprohet_holidays <- function()
{
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

}

f.mprohet_sudden <- function()
{
    # 读入数据集，并对日访问量y做对数处理
    df <- read.csv('predict/prophet/data/example_wp_peyton_manning.csv') %>% mutate(y=log(y))

    # 模型拟合(增加对趋势突变点的操作)
    m <- prophet(df,changepoint.prior.scale = 0.04)
    # 或者通过手工指定突变点
    #m <- prophet(df,changepoints=c(as.Data('2015-01-01')))

    # 构建待预测日期数据
    fucture <- make_future_dataframe(m,periods = 365)

    # 利用模型对预测数据集得到预测结果
    forcast <- predict(m,fucture)

    # 展示预测结果(包含以前的数据和预测的数据，如何区分开这两者呢)
    plot(m,forcast,type='p',col.lab='red')

    # 预测趋势、周效应和年度效应
    prophet_plot_components(m,forcast)

}