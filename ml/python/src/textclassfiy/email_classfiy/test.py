#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from optparse import OptionParser
from bayes.bayes import Bayes

class Test:
    def __init__(self):
        self.bayes = Bayes()

    def status(self):
        args = ['', 'status']
        self.bayes.run(args)

    def reset(self):
        args = ['', 'reset']
        self.bayes.run(args)

    def learn(self, dataset, count_spam, count_ham):
        b = self.bayes
        args = ['', 'learn', 'spam', '%s/spam' % dataset, int(count_spam)]
        b.run(args)
        args = ['', 'learn', 'ham', '%s/ham' % dataset, int(count_ham)]
        b.run(args)

    def test(self, dataset, threshold):
            
        b = self.bayes
        
        print '>> Classifying spam ...'
        args = ['./test.py', 'classify', '%s/spam' % dataset, 'spam', 'ham', threshold]
        result = b.run(args)
        tp = result['positive']
        fn = result['count'] - tp

        print '>> Classifying ham ...'
        args = ['./test.py', 'classify', '%s/ham' % dataset, 'spam', 'ham', threshold]
        result = b.run(args)
        fp = result['positive']
        tn = result['count'] - fp
                                    
        precison = 1.0 * tp / (tp + fp)
        recall = 1.0 * tp / (tp + fn)
        fscore = 2/(1/precison + 1/recall)

        fpr = 1.0*fp/(fp+tn)
        tnr = 1 - fpr

        # self.status()
        print "Classifying Results:"
        print "========================================\n"
        print 'POSITIVE: %6d, TP: %6d, FN: %6d'   % (tp + fn, tp, fn)
        print 'NEGATIVE: %6d, TN: %6d, FP: %6d\n' % (tn + fp, tn, fp)
        print 'TPR: %1.4f, FPR: %1.4f, TNR: %1.4f'   % (recall, fpr, tnr)
        print '  R: %1.4f,   P: %1.4f,   F: %1.4f'   % (recall, precison, fscore)
        print "\n========================================\n"

    def tfidf(self, dataset):
            
        b = self.bayes
        
        print '>> TFIDFing spam ...'
        args = ['./test.py', 'tfidf', '%s/spam' % dataset, 'spam', 'ham']
        result = b.run(args)

        print '>> TFIDF ham ...'
        args = ['./test.py', 'tfidf', '%s/ham' % dataset, 'spam', 'ham']
        result = b.run(args)
                                    

    def chi(self, dataset):
            
        b = self.bayes
        
        print '>> TFIDFing spam ...'
        args = ['./test.py', 'chi', '%s/spam' % dataset, 'spam', 'ham']
        result = b.run(args)

        print '>> TFIDF ham ...'
        args = ['./test.py', 'chi', '%s/ham' % dataset, 'spam', 'ham']
        result = b.run(args)


if __name__ == '__main__':

    op = OptionParser(usage="%prog [options]")
    op.add_option("-s", "--status", action="store_true", help="")
    op.add_option("-r", "--reset",  action="store_true", help="")
    op.add_option("-l", "--learn",  metavar="dataset count_spam count_ham", type="string", nargs=3, help="")
    op.add_option("-t", "--test", metavar="dataset threshold", type="string", nargs=2, help="")
    op.add_option("-i", "--tfidf", metavar="dataset", type="string", help="")
    op.add_option("-x", "--chi", metavar="dataset", type="string", help="")
    
    #op.add_option("-c", "--classify", metavar="dataset", type="string", help="")

    options, args = op.parse_args()
    # print options

    t = Test()
    
    if options.status:
        t.status()
    elif options.reset:
        t.reset()
    elif options.learn:
        t.learn(options.learn[0], options.learn[1], options.learn[2])
    elif options.test:
        print options.test
        t.test(options.test[0], options.test[1])
    elif options.tfidf:
        t.tfidf(options.tfidf)
    elif options.chi:
        t.chi(options.chi)

    else:
    print "Usage: " + sys.argv[0] + ' -h'
