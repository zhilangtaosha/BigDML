#!/usr/bin/python

import sys
from operator import itemgetter
word2count = {}
for line in sys.stdin:
    line = line.strip()
    word, count = line.split(' ', 1)
    try:
        count = int(count)
        word2count[word] = word2count.get(word, 0) + count
    except ValueError:
        continue
    sorted_word2count = sorted(word2count.items(), key=itemgetter(0))
    for word, count in sorted_word2count:
        print '%s %s'% (word, count)