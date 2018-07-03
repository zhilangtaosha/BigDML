#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:tensorflow学习笔记
	Ref:http://www.cnblogs.com/greentomlee/p/5809115.html
	Date:2016/9/24
	Author:tuling56
'''
import os
import sys
import re

reload(sys)
sys.setdefaultencoding('utf-8')

import tensorflow as tf

def fun():
    state=tf.Variable(0,name='counter')
    one=tf.constant(12)
    new_state=tf.add(state,one,name='addop')
    update=tf.assign(state,new_state)

    init=tf.initialize_all_variables()

    with tf.Session() as sess:
        sess.run(init)
        for _ in range(3):
            sess.run(update)
def fun2():
    a = tf.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[2, 3], name='a')
    b = tf.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[3, 2], name='b')
    c = tf.matmul(a, b)

    init=tf.initialize_all_variables()
    with tf.Session() as sess:
        #sess.run(init)
        print sess.run(c)

if __name__ == "__main__":
    fun2()

