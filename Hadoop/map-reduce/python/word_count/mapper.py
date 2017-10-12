#!/usr/bin/python
import sys
for line in sys.stdin:
    #去除字符串两边的空格
    line = line.strip()
    #按照空格去划分单词
    words = line.split()
    for word in words:
        print '%s %s' % (word, 1)