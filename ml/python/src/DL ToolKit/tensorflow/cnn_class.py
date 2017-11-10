#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:模型的的保存和加载
	Ref:http://stackoverflow.com/questions/38888120/tensorflow-loaded-model-gives-different-predictions
	Date:2016/9/26
	Author:tuling56
'''
import os
import sys
import re

reload(sys)
sys.setdefaultencoding('utf-8')


import logging
import numpy as np
import tensorflow as tf
import sklearn as sk
import re
import json
import string
import math
import os
from sklearn.metrics import recall_score, f1_score, precision_score

class CNN(object):
	def __init__(self,logger):
		self.logger = logger

	def _weight_variable(self,shape):
		initial = tf.truncated_normal(shape, stddev = 0.1)
		return tf.Variable(initial)
	
	def _bias_variable(self,shape):
		initial = tf.constant(0.1, shape = shape)
		return tf.Variable(initial)
	
	def _conv2d(self,x, W, b, strides=1):
		# convolve and relu activation
		x = tf.nn.conv2d(x, W, strides=[1, strides, strides, 1], padding='SAME')
		x = tf.nn.bias_add(x, b)
		return tf.nn.relu(x)

	def _maxpool(self,x, k=2):
		return tf.nn.max_pool(x, ksize=[1, k, k, 1], strides=[1, k, k, 1], padding='SAME')
	

	'''
		初始化
	'''
	def _init_CNN(self, sentence_width, sentence_height, dropout, learning_rate,n_class,is_training):
		self.logger.info("----------Initiating CNN---------")
		self.X = tf.placeholder(tf.float32, [None, sentence_height * sentence_width])  #None代表训练样本的个数任意
		self.Y = tf.placeholder(tf.float32, [None, n_class])                           #None代表训练样本的人数任意
	
		x = tf.reshape(self.X, shape = [-1, sentence_height, sentence_width, 1])       # 样本矩阵化
	
		#1st convolution layer
		wc1 = tf.Variable(tf.random_normal([3, 3, 1, 5]))
		bc1 = tf.Variable(tf.random_normal([5]))
		stride1 = 2
		pool1 = 2
		conv1 = self._conv2d(x, wc1, bc1,stride1)
		conv1 = self._maxpool(conv1, pool1)
	
		conv2 = conv1
		pools = [2]#,2,2]
		strides = [2]#,1,1]
		last_channel = 5

		first_size = self._get_first_connected_size(sentence_height,sentence_width, strides,pools,last_channel)
	
		# #1st fully connected layer
		wf1 = tf.Variable(tf.random_normal([first_size, 32]))
		bf1 = tf.Variable(tf.random_normal([32]))
	
		fc1 = tf.reshape(conv2, [-1, wf1.get_shape().as_list()[0]])
		fc1 = tf.add(tf.matmul(fc1, wf1), bf1)
		fc1 = tf.nn.relu(fc1)
		fc1 = tf.nn.dropout(fc1, dropout)
	
		#dropout layer
		outw = tf.Variable(tf.random_normal([32, n_class]))
		outb = tf.Variable(tf.random_normal([n_class]))
	
		self.pred = tf.add(tf.matmul(fc1, outw), outb)
		self.y_p = tf.argmax(self.pred,1)
	
		if is_training is False:
			return

		# self.pred = self._predict(self.X,sentence_width, sentence_height, settings, dropout)
		self.cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(self.pred, self.Y))
		self.optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(self.cost)

		#accuracy
		self.y_t = tf.argmax(self.Y,1)
		self.accuracy = tf.reduce_mean(tf.cast(tf.equal(self.y_p, self.y_t), "float"))
		self.init = tf.initialize_all_variables()

	'''
		获取连接权重个数
	'''
	def _get_first_connected_size(self,ih,iw, strides,pools,last_channel):
		i = 1
		while i <= len(strides):
			iw = math.ceil(float(iw) / float(strides[i-1]))
			iw = math.ceil(float(iw) /pools[i-1])
			ih = math.ceil(float(ih) / float(strides[i-1]))
			ih = math.ceil(float(ih) /pools[i-1])
			i = i + 1
		first_connected_size = int(ih*iw*last_channel)
		return first_connected_size


	'''
		模型训练
	'''
	def train(self,data_provider,config):
		self._init_CNN(config.sentence_width, config.num_word, config.dropout, config.learning_rate,config.n_class,True)
		sess = tf.Session()
		sess.run(self.init)
		self.logger.info("Start Training!")

		#saver
		saver = tf.train.Saver()
		cur_max_accuracy = 0
		cur_max_recall = 0
		cur_max_precision = 0
	
		if config.model_init_from is not None and os.path.exists(config.model_init_from):
			#restore model if exist
			saver.restore(sess, config.model_init_from)
	
		for epoch in range(config.epochs):
			data_provider.reset_batch_pointer()
			for i in range(data_provider.num_batches):
				batch_x, batch_y = data_provider.next_batch()
				accuracy_score,y_p,y_t, _, cost = sess.run([self.accuracy,self.y_p, self.y_t, self.optimizer, self.cost], feed_dict={self.X: batch_x, self.Y: batch_y})
				if i %10 == 0:
					self.logger.info("(%d/%d,%d epo) cost = %f, accuracy = %f,precision = %f, recall = %f, f_score = %f" % (i+epoch * data_provider.num_batches, data_provider.num_batches*config.epochs, epoch,cost,accuracy_score,precision_score(y_t, y_p),recall_score(y_t,y_p),f1_score(y_t,y_p)))
			self.accuracy = tf.reduce_mean(tf.cast(tf.equal(self.y_p, self.y_t), "float"))
			accuracy_score,y_p,y_t, _,cost = sess.run([self.accuracy,self.y_p, self.y_t, self.optimizer, self.cost], feed_dict={self.X: data_provider.get_test_X(), self.Y: data_provider.get_test_Y()})
			precision_score1 = precision_score(y_t, y_p)
			recall_score1 = recall_score(y_t,y_p)
			f1_score1 = f1_score(y_t,y_p)
			self.logger.info("#####(%d/%d epoch) cost = %f, accuracy = %f(max: %f), precision = %f(max: %f), recall = %f(max:%f), f_score = %f" % (epoch,config.epochs, cost,accuracy_score,cur_max_accuracy, precision_score1,cur_max_precision,recall_score1,cur_max_recall,f1_score1))
	
			save_loc = saver.save(sess, config.model_save_path)
			print("Model has been saved to: %s" % save_loc)
			cur_max_accuracy = accuracy_score
			cur_max_recall = recall_score1
			cur_max_precision = precision_score1
	'''
		模型测试
	'''
	def predict_cnn_word2vec(self, data_provider, config):
		if not os.path.exists(config.model_init_from):
			self.logger.info("model does not exist!")
			sys.exit(2)
		self._init_CNN(config.sentence_width, config.num_word, config.dropout, config.learning_rate,config.n_class,False)
	
		while True:
			sentence = input("Enter a sentence:")
			with tf.Session() as sess:
				saver = tf.train.Saver()
				saver.restore(sess, config.model_init_from)
	
				batch_x = np.empty((1, config.num_word*300))
				batch_x[0,:] = data_provider.get_sentence_vec(sentence,config)
	
				y_p = sess.run([self.y_p], feed_dict={self.X: batch_x})
				result = "positive" if y_p == [1] else "negative"
				self.logger.info("[%s] is %s" %(sentence,result))


if __name__ == "__main__":
    fun()

