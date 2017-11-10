#!/usr/bin/env python
# -*- coding: utf-8 -*-

import email
import urllib2


dir = '/Users/haojiash/TDT/2005-Jul/data/ham'


def read_eml(feml):
    message = open(feml,'r')
    subject = ''
    text = ''
    try:
        mail = email.message_from_file(message)
        subject = (email.Header.decode_header(mail['subject'])[0][0]).decode('gb2312').encode('utf8')
        print 'SUBJECT: ', subject
        text = ''
        if mail.is_multipart():
            for part in mail.get_payload():
                showmessage(part)
        else:
            charset = mail.get_content_charset()
            if charset == None:
                charset = 'gb2312'
            text = mail.get_payload().decode(charset).encode('utf8')
    except:
        text = ''

    message.close()

    return subject, text


def fc(text):
    url_get_base = "http://api.ltp-cloud.com/analysis/?"
    api_key = 'Z1I632U0ZXQB0zPR2czWExUIGQMiEI8j9DRcbkhD'
    format = 'plain'
    pattern = 'ws'
    words = ''
    
    try:
        result = urllib2.urlopen("%sapi_key=%s&text=%s&format=%s&pattern=%s" % (url_get_base,api_key,text,format,pattern))
        words = result.read().strip()
    except Exception, e:
        print 'Exceptioin: ', e
        
    return words


if __name__ == '__main__':
    import os
    from mmseg import seg_txt;

    names = os.listdir(dir)

    n = 0
    for name in names:
        f = os.path.join(dir, name)
        
        print '\nFile: ', f, '...'
        nout = name + '.txt'
        if os.path.exists(nout):
            print '-- SKIPPED'
            continue
        
        fout = open(nout, 'w')

        subject, text = read_eml(f)
#        words = fc(subject)
        words = seg_txt(subject)
        fout.write('{}\n\n'.format(' '.join(words)))
        
        lines = text.splitlines()
        for line in lines:
            #text = '感谢您关注语言云，您的语言云账号已经激活。这封邮件包含您调用语言云服务时使用的token，以及一些其他帮助您快速使用语言云的信息。'
            line = line.strip()
            # print '[', line, ']'
            if line <> '':
                #words = fc(line)
                words = seg_txt(line)
                fout.write(' '.join(words) + '\n')
                for w in words:
                    print w
                    
        fout.close()
