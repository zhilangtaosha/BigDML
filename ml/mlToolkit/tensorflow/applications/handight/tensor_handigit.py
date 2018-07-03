#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Date:
	Author:tuling56
	Fun:tensorflow手写数字识别入门程序
'''
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf

flags = tf.app.flags
FLAGS = flags.FLAGS
flags.DEFINE_string('data_dir', './', 'Directory for storing data')

mnist = input_data.read_data_sets(FLAGS.data_dir, one_hot=True)
x = tf.placeholder(tf.float32, [None, 784])
W = tf.Variable(tf.zeros([784,10]))
b = tf.Variable(tf.zeros([10]))
y = tf.nn.softmax(tf.matmul(x,W) + b)
y_ = tf.placeholder("float", [None,10])
cross_entropy = -tf.reduce_sum(y_*tf.log(y))
train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)

init = tf.initialize_all_variables()
sess = tf.InteractiveSession()
sess.run(init)
for i in range(1000):
    batch_xs, batch_ys = mnist.train.next_batch(200)
    sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})  # 真正开始训练

# 在测试集上测试模型
correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
#print "correct_prediction:",correct_prediction   # 混淆矩阵
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
#print "accuracy:",accuracy   
print(accuracy.eval({x: mnist.test.images, y_: mnist.test.labels})) # 准确度
