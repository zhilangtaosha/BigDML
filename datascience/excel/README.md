##Excel笔记
[TOC]

### 基础

#### 入门

##### 引用

###### 引用范围

引用同sheet的

```
A2:B4
```

引用不同sheet的

```
工作表名！A2:B4
```

不同workbook

```shell
[工作簿名]工作表名！A2:B4
```

###### [定义名称](https://jingyan.baidu.com/article/425e69e6bd5fddbe15fc16c7.html)

```shell

```

##### 单元格拆合

单元格的拆分和合并

#### 函数

##### 基础

###### if

```
=IF(AND(a>10,b>10),"V1",IF(a<10,"V2","V3"))
```

###### ISNA/ISERROR

```
处理类似这样的问题"N/A”、“＃VALUE ”、“＃REF ”、“＃DIV/0 ”、“＃NUM ”等删除
```

##### 字符串

###### 查找

index/match

###### 截取拼接

concat

###### 关联匹配

lookup/vlookup

```shell

```

#####  日期



##### 统计

###### average/mean

```shell

```

###### countif

```shell

```

###### sumif/sumproduct

```shell

```

### 应用

#### 行列转换

##### 列转行

//待补充

##### 行转列

//待补充

#### 统计转换

##### 累积和、累积均值

//待添加

##### 月份、季度汇总

//可以直接使用透视图实现，只需要把日期的格式修改成excel能识别的日期格式2017/11/12



### 接口

#### mysql

//excel读取和操作mysql的数据

#### text

//excel读取和操作text数据（非粘贴数据到excel）

### VBA

//这是一大块，待补充



 ##参考

- 基础

  [相对引用和绝对引用](https://support.office.com/zh-cn/article/%E5%9C%A8%E7%9B%B8%E5%AF%B9%E5%BC%95%E7%94%A8%E3%80%81%E7%BB%9D%E5%AF%B9%E5%BC%95%E7%94%A8%E5%92%8C%E6%B7%B7%E5%90%88%E5%BC%95%E7%94%A8%E9%97%B4%E5%88%87%E6%8D%A2-dfec08cd-ae65-4f56-839e-5f0d8d0baca9?ui=zh-CN&rs=zh-CN&ad=CN)

  [单元格的拆分和合并](https://www.toutiao.com/i6553497879183360520/)

- 应用

- 接口

- VBA