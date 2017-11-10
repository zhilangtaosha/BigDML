#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Date:
    Author:tuling56
    Fun:处理维基百科的中文数据，用以训练word2vec模型
'''
import os
import sys
import re

reload(sys)
sys.setdefaultencoding('utf-8')


import logging
import os.path
import sys



'''
    处理维基百科的数据，转换成文本
'''
from gensim.corpora import WikiCorpus
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


if __name__ == "__main__":
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

