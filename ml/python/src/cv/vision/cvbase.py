#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Fun:
    Ref:
    State：
    Date:2017/1/12
    Author:tuling56
'''
import re, os, sys
import hues
import numpy as np

reload(sys)
sys.setdefaultencoding('utf-8')


HAS_CV=False
try:
    sys.path.append("/usr/local/opencv/lib/python2.7/site-packages")
    import cv2
    HAS_CV=True
except Exception,e:
    from PIL import Image
    print "no cv model,use PIL instead"

def cvdemo(picname):
        if HAS_CV:
            img=cv2.imread(picname,0)
            rzimg=cv2.resize(img,(28,28))
            #cv2.imshow("X",img)
            #cv2.waitKey()
            ndimg=np.array(rzimg)
            fndimg=ndimg.astype(float)
        else:
            im=Image.open(picname)
            img=im.convert('L')
            #print(img.format,img.size,img.mode)
            imr=img.resize((28,28),Image.BILINEAR)
            imgbn=np.asarray(imr,dtype=np.float)
            fndimg=imgbn.T

        norm_ndimg=(fndimg-fndimg.min())/(fndimg.max()-fndimg.min())  # 归一化
        print norm_ndimg.flatten()



if __name__ == "__main__":
    picname='D:'
    cvdemo(picname)

