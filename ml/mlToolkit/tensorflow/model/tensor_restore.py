#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:
	Ref:
	Date:2016/9/30
	Author:tuling56
'''
import os
import sys
import re

reload(sys)
sys.setdefaultencoding('utf-8')


def fun():
	import tensorflow as tf

	# Create some variables.
	v1 = tf.Variable(0, name="v1")
	v2 = tf.Variable(0, name="v2")

	# Add ops to save and restore all the variables.
	saver = tf.train.Saver()

	# Later, launch the model, use the saver to restore variables from disk, and
	# do some work with the model.
	with tf.Session() as sess:
		# Restore variables from disk.
		saver.restore(sess, "/tmp/model.ckpt")
		print "Model restored."
		print "v1 = ", v1.eval()
		print "v2 = ", v2.eval()


if __name__ == "__main__":
	fun()

