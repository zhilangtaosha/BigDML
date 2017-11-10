# -*- coding: utf-8 -*-

from __future__ import division
from mode import Mode
from cdb import Db
from words import text_to_list
from operator import itemgetter
import sys
import math

class Chi(Mode):
    MIN_WORD_COUNT = 5
    RARE_WORD_PROB = 0.5
    EXCLUSIVE_WORD_PROB = 0.99

    def __init__(self):
        self.db = Db()

    def set_text(self, text):
        words = text_to_list(text)

        if not len(words):
            raise ValueError('Text did not contain any valid words')

        self.words = words
        return self
    
    def set_path(self, path):
        self.path_name = path
        return self.path_name

    def set_file_name(self, file_name):
        try:
            self.file_name = file_name
            f = open(file_name, 'r')
            file_contents = f.read()
            f.close()
            return self.set_text(file_contents)
        
        except Exception as e:
            raise ValueError('Unable to read specified file "%s", the error message was: %s' % (file_name, e))
        
    def set_doctypes(self, doctype1, doctype2):
        if doctype1 == doctype2:
            raise ValueError('Please enter two different doctypes')

        d = self.db.get_doctype_counts()
        if doctype1 not in d.keys():
            raise ValueError('Unknown doctype: ' + doctype1)

        if doctype2 not in d.keys():
            raise ValueError('Unknown doctype: ' + doctype2)

        self.doctype1 = doctype1
        self.doctype2 = doctype2

    def validate(self, args):
        if len(args) != 5:
            raise ValueError('Usage: %s classify <file> <doctype> <doctype>' % args[0])

        self.set_path(args[2])
        self.set_doctypes(args[3], args[4])

    def chi(self, word, num_spam, num_ham):
        A = self.db.get_word_doc_count('spam', word)
        B = self.db.get_word_doc_count('ham', word)
        C = num_spam - A
        D = num_ham - B
        if A * B == 0:
            chi = 0
        else:
            chi = float(pow((A*D-B*C), 2))/((A+B)*(C+D))
        return chi
        

    def execute(self):
        import os
        
        db = self.db
        result = []
        count = 0
        positive = 0

        d = db.get_doctype_counts()
        num_spam = d["spam"]
        num_ham = d["ham"]

        names = os.listdir(self.path_name)

        fout = open(self.path_name.strip('/').split('/')[-1] + '_chi.txt', 'w')

        for name in names:
            fin = os.path.join(self.path_name, name)
            self.set_file_name(fin)
            f = open(self.path_name.strip('/').split('/')[-1] + '_' + name + '.chi', 'w')


            chi = {}
            for word in self.words:
                chi[word] = self.chi(word, num_spam, num_ham)

            result = sorted(chi.items(), key=itemgetter(1), reverse=True)
            
            n = int(math.log(len(result) + 1)) * 10
                        
            # fout.write("%s %s\n\n" % (name, str(result[:n])) )

            for kw, v in result[:n]:
                f.write("%s " % (kw) )
                
            f.close()

        fout.close()

        return result
    
    def output(self, result):
        #print '\nRESULT: True %d, False %d\n' % (result['positive'], result['count'] - result['positive'])
        pass
