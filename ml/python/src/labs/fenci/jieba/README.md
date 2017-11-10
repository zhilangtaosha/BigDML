##Jieba分词指南
[TOC]

### 分词

#### 添加自定义词典

##### 调整词典

### 关键词抽取

#### 基于TF-IDF关键词抽取

#### 基于TextRank关键词抽取

### 其它

#### 词性标注

#### 并行分词

目标文本按行分割之后，把各行文本分配到pyhton进程进行并行分词，然后归并结果。

用法：

- `jieba.enable_parallel(4)` # 开启并行分词模式，参数为并行进程数
- `jieba.disable_parallel()` # 关闭并行分词模式

> 并行分词仅支持默认分词器 `jieba.dt` 和 `jieba.posseg.dt`。

 ##参考

[jieba官网](https://github.com/fxsjy/jieba)