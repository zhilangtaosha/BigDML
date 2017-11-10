# -*- coding: utf-8 -*-
'''
Cached DB, memory dict

'''
import sqlite3

class Db:
    def __init__(self):
        self.conn = sqlite3.connect('./bayes.db')
        self.conn.text_factory = str

        self.words = {}
        self.doctypes = {}
        self.load_words()
        self.load_doctypes()

    def store(self):
        self.dump_words()
        self.dump_doctypes()
        
    def reset(self):
        self.words = {}
        self.doctypes = {}

    def load_words(self):
        words = {}
        v = {}
        c = self.conn.cursor()
        try:
            for row in c.execute('select doctype, word, count, doc_count from word'):
                w = {}
                
                w['count'] = row[2]
                w['doc_count'] = row[3]
                
                if words.get(row[0]) == None:
                    words[row[0]] = {}

                v = words[row[0]]
                v[row[1]] = w

            self.words = words
            return words

        finally:
            c.close()
            self.conn.commit()

    def dump_words(self):
        c = self.conn.cursor()
        try:
            c.execute('delete from word')
            for doctype, words in self.words.iteritems():
                for word, v in words.iteritems():
                    c.execute('insert into word (doctype, word, count, doc_count) values (?,?,?,?)', (doctype, word, v['count'], v['doc_count']))


        finally:
            c.close()
            self.conn.commit()
        

    def dump_doctypes(self):
        c = self.conn.cursor()
        try:
            c.execute('delete from doctype_count')
            for doctype, count in self.doctypes.iteritems():
                c.execute('insert into doctype_count (doctype, count) values (?, ?)', (doctype, count))
        finally:
            c.close()
            self.conn.commit()
        

    def load_doctypes(self):
        doctypes = {}
        c = self.conn.cursor()
        try:
            for row in c.execute('select doctype, count from doctype_count'):
                doctypes[row[0]] = row[1]

            self.doctypes = doctypes
            return doctypes

        finally:
            c.close()
            self.conn.commit()

    def update_word_count(self, doctype, word, num_to_add_to_count):
                
        if self.words.get(doctype) == None:
            self.words[doctype] = {}

        if self.words[doctype].get(word) == None:
            count = 0
            doc_count = 0
        else:
            count = self.words[doctype][word]['count']
            doc_count = self.words[doctype][word]['doc_count']
            
        self.words[doctype][word] = {'count': count + num_to_add_to_count, 'doc_count' : doc_count + 1}
        

    def update_word_counts(self, d, doctype):
        total = 0
        for word, count in d.items():
            self.update_word_count(doctype, word, count)
            total += count
            
        return total

    def update_doctype_count(self, num_new_ads, doctype):
        dt = self.doctypes.get(doctype)
        if dt == None:
            count = num_new_ads
        else:
            count = self.doctypes[doctype] + num_new_ads

        self.doctypes[doctype] = count


    def get_word_count(self, doctype, word):
        '''count of the word appears in doctype '''

        if self.words[doctype].get(word) == None:
            return 0

        return self.words[doctype][word]['count']

    def get_word_doc_count(self, doctype, word):
        ''' count of documents those include the word'''
        if self.words[doctype].get(word) == None:
            return 0

        return self.words[doctype][word]['doc_count']


    def get_words_count(self, doctype):
        d = self.words.get(doctype)
        if d == None:
            return d

        return reduce(lambda x,y: x + y, map(lambda x:x.get('count'), d.values()))

    def get_doctype_counts(self):
        return self.doctypes

    def save_corpus_to_file(self, idf_filename, stopword_filename,
                STOPWORD_PERCENTAGE_THRESHOLD = 0.01):
        """Save the idf dictionary and stopword list to the specified file."""
        output_file = open(idf_filename, "w")
        
        num_docs_spam = dc.get('spam')
        num_docs_ham = dc.get('ham')

        output_file.write("spam: %s, ham: %s\n\n" % (str(num_docs_spam), str(num_docs_ham)))

        for doctype, words in self.words.iteritems():
            for word, v in words.iteritems():
                output_file.write("%s : %s : %s : %s\n" % (doctype, word, str(v['count']), str(v['doc_count'])))

        stopword_file = open(stopword_filename, "w")
        for term, num_docs in sorted_terms:
            if num_docs < STOPWORD_PERCENTAGE_THRESHOLD * self.num_docs:
                break
            
            stopword_file.write(term + "\n")



if __name__ == '__main__':
    d = Db()
    # r = d.load_doctypes()
    # print r
    # r = d.load_words()
    # print r

    print d.get_words_count('spam')
    print d.get_words_count('ham')
