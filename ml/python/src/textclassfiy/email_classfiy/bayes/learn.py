# -*- coding: utf-8 -*-

from cdb import Db
from mode import Mode
from words import list_to_dict
from words import text_to_list
import os

class Learn(Mode):
    def validate(self, args):
        valid_args = False
        usage = 'Usage: %s learn <doc type> <dir> <count>' % args[0]

        if len(args) == 5:
            doc_type = args[2]
            
            self.doc_type = doc_type

            self.path_name = args[3]
            try:
                self.count = int(args[4])
            except:
                raise ValueError(usage + '\nEnter an integer value for the "count" parameter')            

        else:
            raise ValueError(usage)


    def learn_file(self, name, count):
        file_contents = None
        words_count = 0
        db = self.db
        try:
            f = open(name, 'r')
            file_contents = f.read()
            f.close()

            l = text_to_list(file_contents)
            d = list_to_dict(l)
            words_count = db.update_word_counts(d, self.doc_type)
            db.update_doctype_count(count, self.doc_type)

            print '>> TRAINING [ %s ]: %5d words learned from "%s"' % (self.doc_type, words_count, name)


        except Exception as e:
            raise ValueError(usage + '\nUnable to read specified file "%s", the error message was: %s' % (args[3], e))

        return words_count

    def execute(self):
        result = {}
        self.db = Db()
                
        try:
            nword = 0
            ndoc = 0

            if os.path.isdir(self.path_name):
                names = os.listdir(self.path_name)
                for name in names:
                    f = os.path.join(self.path_name, name)
                    nword += self.learn_file(f, 1)
                    ndoc += 1
                    if ndoc >= self.count:
                        break
                    
            if os.path.isfile(self.path_name):
                nword += self.learn_file(self.path_name, self.count)
                ndoc += self.count
                        
        except:
            print 'learning unexception'

        result['ndoc'] = ndoc
        result['nword'] = nword

        self.db.store()
        
        return result

    def output(self, result):
        print '>> TRAINING [ %s ]: %5d document(s), %5d words learned from "%s"' % (self.doc_type, result['ndoc'], result['nword'], self.path_name)
