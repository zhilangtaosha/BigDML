#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Date:
    Author:tuling56
    Fun:获取语料，繁简转换，中文分词，训练word2vec模型，测试word2vec模型（得到词语之间的语义相似度）
'''
import os
import sys
import re

import logging
import os.path
import sys
import multiprocessing

import gensim
from gensim.corpora import WikiCorpus
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence

reload(sys)
sys.setdefaultencoding('utf-8')


'''
    处理维基百科的数据，转换成文本
'''
def process_wiki(inp,outp):
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
    logging.root.setLevel(level=logging.INFO)
    logger.info("running %s" % ' '.join(sys.argv))

    space = " "
    i = 0
    output = open(outp, 'w')
    wiki = WikiCorpus(inp, lemmatize=False, dictionary={})
    for text in wiki.get_texts():
        output.write(space.join(text) + "\n")
        i = i + 1
        if (i % 10000 == 0):
            logger.info("Saved " + str(i) + " articles")

    output.close()
    logger.info("Finished Saved " + str(i) + " articles")



'''
    中文分词
'''
import  jieba
def zh_split(inp,outp):
    fin=open(inp,'r')
    fout=open(outp,'w')
    i=0
    for line in fin:
        i=i+1
        ratio="%f" %(i*100/float(268740))
        print ratio+"%"
        seg_list = jieba.cut(line, cut_all=False)
        segres=" ".join(seg_list)+'\n'
        fout.write(segres)
    fin.close()
    fout.close()


'''
    训练得到word2vec模型
    输入经过繁简转换和分词后的语料
'''
def train_word2vec_modle(inp,outp1,outp2):
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
    logging.root.setLevel(level=logging.INFO)
    logger.info("running %s" % ' '.join(sys.argv))

    model = Word2Vec(LineSentence(inp), size=400, window=5, min_count=5,workers=multiprocessing.cpu_count())

    # trim unneeded model memory = use(much) less RAM
    #model.init_sims(replace=True)
    model.save(outp1)
    model.save_word2vec_format(outp2, binary=False)

'''
    测试word2vec模型
    计算词语之间的语义相似度
'''
def test_word2vec_modle(modlefile):
    modle=gensim.models.Word2Vec.load(modlefile)   #由于文件较大，加载时间会很长
    res=modle.most_similar(u"台球")
    for s in res:
        print s[0],s[1]


if __name__ == '__main__':
    # check and process input arguments
    #if len(sys.argv) < 3:
    #    print globals()['__doc__'] % locals()
    #    sys.exit(1)
    #else:
    #    inp, outp = sys.argv[1:3]
    '''
    inp="D:\\Docs\\zhwiki-latest-pages-articles.xml.bz2"
    outp="D:\\Docs\\zhwiki_text"
    process_wiki(inp,outp)
    '''

    inp_jian="D:\\Docs\\zhwiki_text_jian"
    outp_seg="D:\\Docs\\zhwiki_text_jian_seg"
    zh_split(inp_jian,outp_seg)

    inp="D:\\Docs\\zhwiki_text_jian_seg"
    modlefile="D:\\Docs\\zhwiki_model"
    modlefile_vector="D:\\Docs\\zhwiki_vector"
    #train_word2vec_modle(inp,modlefile,modlefile_vector)
    test_word2vec_modle(modlefile)


