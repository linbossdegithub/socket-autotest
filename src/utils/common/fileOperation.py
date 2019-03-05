#encoding=utf-8
'''
Created on 2018年12月12日

@author: linhuajian
'''
import os
import hashlib
def getFileMd5(filename):
    """
    获取文件 Md5
    :param1   filename        type:str   文件的绝对路径
    :return  type  str   Md5码 
    :example Md5 =  getFileMd5('\\file\\media\\nova\\media\\f6701e6b7e2713a0944872df183269d2.png')
    """
    if not os.path.isfile(filename):
        print "文件路径错误"
        return
    myhash = hashlib.md5()
    f = open(filename,'rb')
    while True:
        b = f.read(8096)
        if not b :
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()

def getFileSize(path):
    """
    计算文件夹 大小
    :param1   path        type:str    文件夹路径
    :return  type  long   文件夹大小 
    :example totalsize = getFileSize("\\file\\media\\nova")
        """

    size = 0L 
    for root , dirs, files in os.walk(path, True): 
        #目录下文件大小累加 
        size += sum([os.path.getsize(os.path.join(root, name))for name in files]) 
    return size