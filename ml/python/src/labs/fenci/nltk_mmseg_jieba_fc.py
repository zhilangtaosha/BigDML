# -*- coding: utf-8 -*-
import sys,os
import re
reload(sys) 
sys.setdefaultencoding('utf-8')

#nltk带的英文分词
#nltk_data的搜索路径
'''
Resource 'corpora/stopwords' not found.  Please use the NLTK
  Downloader to obtain the resource:  >>> nltk.download()
  Searched in:
    - 'C:\\Users\\jmy/nltk_data'
    - 'C:\\nltk_data'
    - 'D:\\nltk_data'
    - 'E:\\nltk_data'
    - 'C:\\Python27\\nltk_data'
    - 'C:\\Python27\\lib\\nltk_data'
    - 'C:\\Users\\jmy\\AppData\\Roaming\\nltk_data'
'''
import nltk
from nltk.corpus import stopwords
def nltk_en():
    print '--------------------nltk-en分词------------------'
    setence="at!eight o'clock on Thursday morning lost"
    tokens = nltk.word_tokenize(setence)    #分词（输出分词列表）
    print tokens

    #词性标注
    #tagged= nltk.pos_tag(tokens)
    #print tagged
     
    ##句法分析
    #entities=nltk.chunk.ne_chunk(tagged)
    #print entities

    #去标点符号
    english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%']
    tokens = [w for w in tokens if w.lower() not in english_punctuations]

    #词干化
    porter = nltk.PorterStemmer()
    tokens = [porter.stem(t) for t in tokens]

    #去停用词（列表推导） 方法一
    word_list=tokens
    stops=stopwords.words('english')
    filtered_words = [w for w in word_list if not w in stops]  #  word_list为待过滤的词
    print filtered_words

    #去停用词（遍历过滤） 方法二
    filtered_word_list = word_list[:]
    for word in word_list:
      if word in stopwords.words('english'): 
        filtered_word_list.remove(word)   # 只是移除了第一个匹配项，它修改了列表，但是没有返回值
    print filtered_word_list

    #去停用词（集合的差）  方法三
    pattern=re.compile(r'(\w+)')
    segres=list(set(nltk.regexp_tokenize(setence, pattern, gaps=True)) - set(nltk.corpus.stopwords.words('english')))
    print segres

#NLTK暂时不支持中文分词
from stanford_segmenter import StanfordSegmenter
def nltk_cn():
    print '--------------------nltk-cn分词------------------'
    os.environ['JAVAHOME'] = "F://Java//jdk1.8.0_51//bin/"  #注意添加环境变量的方法
    sentence = u"这是斯坦福中文分词器测试"
    stanford_dir="D:\Software\stanford-segmenter-2014-08-27"
    segmenter = StanfordSegmenter(
    path_to_jar=os.path.join(stanford_dir,"stanford-segmenter-3.4.1.jar"),
    path_to_slf4j = os.path.join(stanford_dir,"slf4j-api-1.5.2.jar"),
    path_to_sihan_corpora_dict=os.path.join(stanford_dir,"./data"),
    path_to_model=os.path.join(stanford_dir,"./data/pku.gz"),
    path_to_dict=os.path.join(stanford_dir,"./data/dict-chris6.ser.gz"))
    segres=segmenter.segment(sentence)
    print segres



#pymmseg中文分词（不可用）
#from pymmseg import mmseg
def pymmseg ():
    print '--------------------pymmseg中文分词------------------'
    mmseg.dict_load_defaults()    
    text = '今天的天气真好啊，我们一起出去玩一下吧'
    algor = mmseg.Algorithm(text)    
    word  = []
    for tok in algor:    
        word.append(tok.text)
    print   ' '.join(word).decode('utf8').encode('gb2312')

    #for tok in algor:
    #   print '%s [%d..%d]' % (tok.text, tok.start, tok.end)

#mmseg中文分词（不可用）
import mmseg
#from mmseg import seg_txt
def mmseg():
    print '--------------------mmseg中文分词------------------'
    line="xiaoming ni haode"
    #tokens=seg_txt(line)
    #print ' '.join(tokens)


#jieba中文分词
import  jieba
def mjieba ():
    print '--------------------jieba中文分词------------------'
    seg_list = jieba.cut("beij bus sfdda", cut_all=True)
    print "Full Mode:", "/ ".join(seg_list)  # 全模式

    seg_list = jieba.cut("我来到北京清华大学", cut_all=False)
    print "Default Mode:", "/ ".join(seg_list)  # 精确模式

    seg_list = jieba.cut("他来到了网易杭研大厦")  # 默认是精确模式
    print ", ".join(seg_list)

    seg_list = jieba.cut_for_search("小明硕士毕业于中国科学院计算所，后在日本京都大学深造")  # 搜索引擎模式
    print ", ".join(seg_list)


'''
    mecab分词：依赖性太强
'''
#import MeCab
def mmecab():
    pass

#语言云API（这个需要联网【函数嵌套】）
import urllib2
def yuyanyun():
    print '--------------------fc中文分词------------------'
    fctext='你好，请把你的自行车移动一下啊'
    def fc(text):
        url_get_base = "http://api.ltp-cloud.com/analysis/?"
        api_key = 'Z1I632U0ZXQB0zPR2czWExUIGQMiEI8j9DRcbkhD'
        format = 'plain'
        pattern = 'ws'
        words = ''
        
        try:
            result = urllib2.urlopen("%sapi_key=%s&text=%s&format=%s&pattern=%s" % (url_get_base,api_key,text,format,pattern))
            words = result.read().strip()  #删除正文内容的空白字符   
        except Exception, e:
            print 'Exceptioin: ', e
        return words

    print fc(fctext)

if __name__=="__main__":
    #nltk_en()
    #nltk_cn()
    mjieba()
    #yuyanyun()
