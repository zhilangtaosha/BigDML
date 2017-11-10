#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from learn import Learn
from classify import Classify
from reset import Reset
from status import Status
from tfidf import Tfidf
from chi import Chi


class Bayes:

    modes = {}

    def __init__(self):
        try:
            self.register_mode(Learn)
            self.register_mode(Classify)
            self.register_mode(Reset)
            self.register_mode(Tfidf)
            self.register_mode(Chi)
            self.register_mode(Status)
    except Exception as ex:
            print ex

    def register_mode(self, mode_class):
    self.modes[mode_class.__name__.lower()] = mode_class

    def run(self, args):
        result = None
        try:
            usage = 'Usage: %s %s <mode specific args>' % (args[0], '|'.join(self.modes.keys()))
            
            if (len(args) < 2):
                raise ValueError(usage)

            mode_name = args[1]
            if mode_name not in self.modes:
                raise ValueError(usage + '\nUnrecognised mode: ' + mode_name)

            mode = self.modes[mode_name]()
            mode.validate(args)
            result = mode.execute()
            mode.output(result)

    except Exception as ex:
            print ex

        return result


if __name__ == '__main__':

    args = sys.argv

    b = Bayes()
    
    print b.run(args)
    
    # try:
    #     register_mode(Learn)
    #     register_mode(Classify)
    #     register_mode(Reset)
    #     register_mode(Status)

    #     args = sys.argv
    #     usage = 'Usage: %s %s <mode specific args>' % (args[0], '|'.join(modes.keys()))

    #     if (len(args) < 2):
    #         raise ValueError(usage)

    #     mode_name = args[1]
    #     if mode_name not in modes:
    #         raise ValueError(usage + '\nUnrecognised mode: ' + mode_name)

    #     mode = modes[mode_name]()
    #     mode.validate(args)
    #     mode.output(mode.execute())
        
    # except Exception as ex:
    #     print ex
