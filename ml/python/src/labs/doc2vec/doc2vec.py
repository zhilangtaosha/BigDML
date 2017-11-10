#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Fun:带类别标签的文档向量化
    Ref:http://toutiao.com/a6330467508265500930/（注意参考链接下面的引用文献）
    Date:2016/9/20
    Author:tuling56
'''
import os
import sys
import re

reload(sys)
sys.setdefaultencoding('utf-8')

import gensim, logging
from gensim.models.doc2vec import Doc2Vec,LabeledSentence
#from gensim.models import Doc2Vec
#import gensim.models.doc2vec

asin=set
category=set

# 文档向量化（样本制作）
class LabeledLineSentence(object):
    def __init__(self, filename=object):
        self.filename =filename
    def __iter__(self):
        with open(self.filename,'r') as infile:
            data=infile.readlines;
            print "length: ", len(data)
            for uid,line in enumerate(data):
                asin.add(line.split("\t")[0])     #第一个是标签
                category.add(line.split("\t")[1]) #第二个是类别
                yield LabeledSentence(words=line.split("\t")[2].split, labels=[line.split("\t")[0],line.split("\t")[1]])
        print 'load success'
        logging.basicConfig(format = '%(asctime)s : %(levelname)s : %(message)s', level = logging.INFO)

# 模型训练和保存
sentences =LabeledLineSentence('product_bpr_train.txt')
model = Doc2Vec(sentences, size = 100, window = 5, min_count=1)
model.save('product_bpr_model.txt')
print 'train sucess'

# 模型查看
for uid,line in enumerate(model.vocab):
    print line
    print len(model.vocab)
    outid = file('product_bpr_id_vector.txt', 'w')
    outcate = file('product_bpr_cate_vector.txt', 'w')
    for idx, line in enumerate(model.vocab):
        if line in asin :
            outid.write(line +'\t')
            for idx,lv in enumerate(model[line]):
                outid.write(str(lv)+" ")
                outid.write('\n')
        if line in category:
            outcate.write(line + '\t')
            for idx,lv in enumerate(model[line]):
                outcate.write(str(lv)+" ")
                outcate.write('\n')
    outid.close
    outcate.close




if __name__ == "__main__":
    pass


