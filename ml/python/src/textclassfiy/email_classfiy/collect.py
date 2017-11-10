#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

#dir = 'ham'
#output_prefix = 'ham'                  # 文档集合文件名的前缀

#collection = 1000 # 用于贝叶斯训练的每个文档集合中样本的个数
#total = 1000    # 用于训练的样本总个数

dir = sys.argv[1]
output_prefix = dir

collection = int(sys.argv[2])
total = collection

print dir, collection


if __name__ == '__main__':
    import os

    names = os.listdir(dir)

    n = 0
    for name in names:
        n += 1
        if n % collection == 1:
            fout = open(output_prefix + str(collection) + '.txt', 'w')

        if n % total == 0:
            break
            
        f = os.path.join(dir, name)
        
        fin = open(f, 'r')
        fout.write(fin.read())
        fout.write('\n\n')
        fin.close()
