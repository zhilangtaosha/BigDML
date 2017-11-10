# -*- coding: utf-8 -*-

from __future__ import division
from mode import Mode
from cdb import Db
from words import text_to_list
import sys

class Classify(Mode):
    MIN_WORD_COUNT = 5
    RARE_WORD_PROB = 0.5
    EXCLUSIVE_WORD_PROB = 0.99
    THRESHOLD = 0.7999

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

        d = Db().get_doctype_counts()
        if doctype1 not in d.keys():
            raise ValueError('Unknown doctype: ' + doctype1)

        if doctype2 not in d.keys():
            raise ValueError('Unknown doctype: ' + doctype2)

        self.doctype1 = doctype1
        self.doctype2 = doctype2

    def validate(self, args):
        if len(args) != 6:
            raise ValueError('Usage: %s classify <file> <doctype> <doctype>' % args[0])

        self.set_path(args[2])
        self.set_doctypes(args[3], args[4])
        self.THRESHOLD = float(args[5])
        

    def p_for_word(self, db, word):
        total_word_count = self.doctype1_word_count + self.doctype2_word_count

        word_count_doctype1 = db.get_word_count(self.doctype1, word)
        word_count_doctype2 = db.get_word_count(self.doctype2, word)
        
        if word_count_doctype1 + word_count_doctype2 < self.MIN_WORD_COUNT:
            return self.RARE_WORD_PROB

        if word_count_doctype1 == 0:
                return 1 - self.EXCLUSIVE_WORD_PROB
        elif word_count_doctype2 == 0:
                return self.EXCLUSIVE_WORD_PROB

        # P(S|W) = P(W|S) / ( P(W|S) + P(W|H) )

        p_ws = word_count_doctype1 / self.doctype1_word_count
        p_wh = word_count_doctype2 / self.doctype2_word_count

        return p_ws / (p_ws + p_wh)

    def p_from_list(self, l):
        p_product         = reduce(lambda x,y: x*y, l)
        p_inverse_product = reduce(lambda x,y: x*y, map(lambda x: 1-x, l))
        # Bug here: p_* might overflow!!!!
        if p_product < sys.float_info.min:
            return 0.0
        
        return p_product / (p_product + p_inverse_product)

    def execute(self):
        import os
        
        db = Db()
        result = {}
        count = 0
        positive = 0

        d = db.get_doctype_counts()
        self.doctype1_count = d.get(self.doctype1)
        self.doctype2_count = d.get(self.doctype2)

        self.doctype1_word_count = db.get_words_count(self.doctype1)
        self.doctype2_word_count = db.get_words_count(self.doctype2)

        names = os.listdir(self.path_name)

        fout = open(self.path_name.strip('/').split('/')[-1] + '_score.txt', 'w')
        n = len(names)

        for name in names:
            f = os.path.join(self.path_name, name)
            self.set_file_name(f)

            pl = []
            for word in self.words:
                pw = self.p_for_word(db, word)
                pl.append(pw)

            p = self.p_from_list(pl)
            fout.write("%s %1.4f\n" % (name, p) )

            count += 1
            tag = 'F'
            if p > self.THRESHOLD:
                positive += 1
                tag = 'T'

            # if abs(p - self.THRESHOLD) < 0.1:
            #     print '[ %5d / %5d ] %s %16s : %1.4f' %(count, n, tag, name, p)

        fout.write('\nRESULT: [ %d / %d ] %1.2f%%\n' % (positive, count, 100*positive/count) )
        fout.close()

        result['count'] = count
        result['positive'] = positive

        return result
    
    def output(self, result):
        #print '\nRESULT: True %d, False %d\n' % (result['positive'], result['count'] - result['positive'])
        pass
