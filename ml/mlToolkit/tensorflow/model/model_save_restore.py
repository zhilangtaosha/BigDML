#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:模型保存和加载测试
	Ref:http://blog.csdn.net/searobbers_duck/article/details/51721916
	Date:2016/9/26
	Author:tuling56
'''
import os
import sys
import re

reload(sys)
sys.setdefaultencoding('utf-8')


import tensorflow as tf
import os
import numpy as np
from tensorflow.python.platform import gfile #这个是什么文件


flags = tf.app.flags
FLAGS = flags.FLAGS
flags.DEFINE_string('summaries_dir', '/tmp/save_graph_logs', 'Summaries directory')

data = np.arange(10,dtype=np.int32)

'''
	模型保存
'''
def savemodle():
	print u"step1：模型训练和保存".decode('utf8')
	with tf.Session() as sess:
		# 运算依赖型
		input1= tf.placeholder(tf.int32, [10], name="input")
		output1= tf.add(input1, tf.constant(100,dtype=tf.int32), name="output") #  data depends on the input data

		# 直接结果保存型
		saved_result= tf.Variable(data,name="saved1_result") # 直接初始化结果（开始的时候是1-10）
		do_save=tf.assign(saved_result,output1)              #将output1的输出给saved_result（运算后是101-110）

		#变量初始化
		tf.initialize_all_variables()

		#保存模型
		os.system("rm -rf /tmp/save_graph_logs")
		merged = tf.merge_all_summaries()
		train_writer = tf.train.SummaryWriter(FLAGS.summaries_dir,sess.graph) #创建训练保存器

		os.system("rm -rf /tmp/load")
		tf.train.write_graph(sess.graph_def, "/tmp/load", "test.pb", False) # 计算图模型

		# 保存数据（计算的数据和初始化的数据）
		result,_=sess.run([output1,do_save], {input1: data}) # calculate output1 and assign to 'saved_result'
		saver = tf.train.Saver(tf.all_variables())  #保存索引变量的数据
		saver.save(sess,"checkpoint.data")

	print "[DONE]"

'''
	模型加载
'''
def loadmodle():
	print u"step2：模型加载测试".decode('utf8')
	with tf.Session() as persisted_sess:
		print("---1：load graph") #加载计算图
		with gfile.FastGFile("/tmp/load/test.pb",'rb') as f:
			graph_def = tf.GraphDef()
			graph_def.ParseFromString(f.read())
			persisted_sess.graph.as_default()
			tf.import_graph_def(graph_def, name='') #加载图定义

		print("---2,map variables")
		persisted_result = persisted_sess.graph.get_tensor_by_name("saved1_result:0") #获取这个tensor
		tf.add_to_collection(tf.GraphKeys.VARIABLES,persisted_result)  				 #将这个tensor加入到要恢复的变量中

		# 恢复数据
		print("---3,load data")
		try:
			saver = tf.train.Saver(tf.all_variables()) # 'Saver' misnomer! Better: Persister!  #将变量恢复
		except Exception,e:
			print(str(e))
		saver.restore(persisted_sess, "checkpoint.data")  # 将变量的数据重新加载到各个tensor


		#重现运算
		print(persisted_result.eval())
		print("DONE")



if __name__ == "__main__":
	savemodle()
	loadmodle()

