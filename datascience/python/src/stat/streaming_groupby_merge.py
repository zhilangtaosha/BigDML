#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Fun:处理hive的streaming_groupby_merge
    Ref:
    State：
    Date:2018/8/29
    Author:tuling56
'''

import hues
import re, os, sys
from collections import defaultdict

reload(sys)
sys.setdefaultencoding('utf-8')


class CStreamMerge():
    def __init__(self):
        self.gks=defaultdict(list)  # 如何设置默认的value是列表格式呢

    def __del__(self):
        pass

    def run(self):
        with open('test.data','r') as f:
            for line in f:
                guid,active_arr,ds,appid=line.strip().split()
                active_list=eval(active_arr)
                self.gks[guid].extend(active_list)
                print '\t'.join([guid,str(self.gks[guid]),ds,appid])

# 测试入口
if __name__ == "__main__":
    ct = CStreamMerge()
    ct.run()

