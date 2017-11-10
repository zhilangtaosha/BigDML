#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Fun:改造中文分词
    Ref:https://github.com/fxsjy/jieba
    State：
    Date:2017/10/11
    Author:tuling56
'''

import hues
import re, os, sys

reload(sys)
sys.setdefaultencoding('utf-8')

import jieba
from collections import Counter


'''
    改造的中文分词工具
'''
class Cjieba():
    def __init__(self):
        self.hfc=Counter()
        # 临时自定义停止词
        self.stopwordslist =set() #{u'博客园',u'博客',u'的',u'CSDN',u'NET',u'之',u'大',u'与',u'频道',u'我',u'中',u'专栏',u'在线',u'用法',u'搭建',u'伯乐',u'开发',u'程序员',u'详解'}

        self.stop_comm_file='dict/stopwords.txt'
        self.stop_me_file='dict/stopwords_me.txt'
        self.userdict='dict/userdict.txt'

        self.indata=r'E:\\Code\\Git\\Python\\Projects\data_platform\\hf_filter\\test.log'
        self.outdata='out.log'


    def __del__(self):
        pass

    # 初始化停用词集合
    def __init_stoplist(self):
        # 添加通用停止词
        with open(self.stop_comm_file, 'r') as f:
            for line in f:
                line=line.strip().decode('utf8')
                self.stopwordslist.add(line)

        # 添加专用停止词
        with open(self.stop_me_file,'r') as f:
            for line in f:
                line=line.strip().decode('utf8')
                self.stopwordslist.add(line)

    # 初始化用户字典
    def __init_userdict(self):
        jieba.load_userdict(self.userdict)

    # 判断是否是停止词
    def _judge_stop(self,word):
        if word in self.stopwordslist:
            return True

        # 添加其他停止词匹配条件
        if re.match(r'[0-9a-zA-Z]+',word): # 纯数字和英文也算停止词
            return True

        # 是否是但日文
        if re.search(ur"[\u3040-\u309f]+", word) or re.search(ur'[\u30a0-\u30ff]+',word):
            return True

        return False

    # 字符处理
    def _str_proc(self,instr):
        outstr=instr
        return outstr

    # 准备（初始化字典）
    def ready(self):
        self.__init_stoplist()
        self.__init_userdict()

    # 分词
    def fenci(self):
        with open(self.indata,'r') as f:
            i=0
            for line in f:
                i=i+1
                if i%100==0:
                    ration=float(i)*100/10000
                    hues.info("process:%4.2f%%" %(ration))
                gcid,name=line.strip('\n').split('\t')
                fname=self._str_proc(name)
                fl=jieba.cut(fname)
                for w in fl:
                    if not self._judge_stop(w):
                        self.hfc[w]+=1


    # 保存词频统计结果
    def save(self):
        with open(self.outdata,'w') as f:
            for hw,hwc in self.hfc.iteritems():
                if hwc>10:
                    res=hw+"\t"+str(hwc)+"\n"
                    f.write(res)

    # 功能入口
    def entry(self):
        self.ready()
        self.fenci()
        self.save()


# 测试入口
if __name__ == "__main__":
    ct = Cjieba()
    ct.entry()

