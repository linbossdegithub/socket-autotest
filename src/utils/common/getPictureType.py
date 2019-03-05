#encoding=utf-8
'''
Created on 2018年12月10日

@author: linhuajian
'''
import time
from PIL import Image
#pip install pillow
import os 
from utils.common.common import sendGetCommand
from constant.constant import Constant
from utils.common.ftper import downloadFile
def downloadScreenCapture(self,width=256,height=256,type="PNG"):
    '''
            下载截图
    :param1   self        必须
    :param2   width    宽
    :param3    height   高
    :param3   type   截图类型
    :return     Res   type：dict{sn:True}   sn号:截图下载成功与否   
    :example Res = downloadScreenCapture(self,width=256,height=256,type="PNG")
    '''
    data={"width":width,"height":height,"type":type }
    result = sendGetCommand(self,Constant.WHAT_SCREEN_SHOT,0,Constant.ACTION_GET,0,data=data,timeout=8,describe="截图")
    ftpfiles={}
    for key in result.keys():
        if result[key]=="FAILED" or result[key]=="ERROR":
            ftpfiles[key] = "FAILED"
        else:
            ftpfiles[key]=result[key]["path"].encode("utf-8")
    filedir = os.path.abspath("../file/screenCapture")
    Res = downloadFile(self, user='admin', filepath=filedir, ftpfiles=ftpfiles,filetype='png')
    return Res
def getPictureType(self,purls={}):
    '''
            获取图片状况
    :param1   self        必须
    :param2   picurls   type: Dict    {"picName":picurl}  图片地址
    :return  result    type: Dict        {"Sn",0}        0：屏幕全黑 1:屏幕为灰 2：其他   
    :example result = getPictureType(self,picurl={})
    :example1 result = getPictureType(self,picurl={sn:picurl})
    '''
    result = {}
    if purls == {}:
        picurls = {}
    else:
        picurls = purls
    if picurls == {}:
        downloadRes = downloadScreenCapture(self)
        for sn in self.sns:
            if downloadRes[sn] :
                filename = sn + ".png"
                filedir = os.path.abspath("../file/screenCapture")
                file = os.path.join(filedir, filename)
                picurls[sn] = file
                # print '截图下载成功'
            else:
                result[sn] ='下载失败'
    
    for Sn in picurls.keys():
        try:
            im = Image.open(picurls[Sn].encode("utf-8"))
            (width,height) = im.size
            im = im.convert("RGB")
        except:
            print "截图打开失败"
            return result
        rs=0
        bs=0
        gs=0
        for i in range(width):
            for j in range(height):
                r,g,b = im.getpixel((i,j))
                rs+=r
                gs+=g
                bs+=b
        r = rs/(width*height)
        g = gs/(width*height)
        b = bs/(width*height)
        if r ==0 and g ==0 and b ==0:
            result[Sn] = 0 
        elif r==47 and g==42 and b==41:
            result[Sn] = 1
        else: 
            result[Sn] = 2
    return result   
def getPictureResult(self):
    '''
            判断图片状况结果
    :param1   self        必须
    :return  result    type: int  0：全部屏幕全黑 1:全部屏幕为灰 2：全部播放正常   3：截图状态不一致  
    :example result = getPictureResult(self)
    '''
    result = getPictureType(self)
    flag   = True
    flag1 = True
    flag2 = True
    for key in result.keys():
        if result[key]!=0:
            flag = False
        if result[key]!=1:
            flag1 = False
        if result[key]!=2:
            flag2 = False   
    if flag2 == True:
        return 2
    elif flag1==True:
        return 1
    elif flag == True:
        return 0
    else:
        print result
        return 3

def assertIsPlaying(self):
    n = 0
    while True:
        flag = True
        n+=1
        print "第 " + str(n) + " 次截图"
        result = getPictureType(self)
        for key in result.keys():
            if result[key]!=2:
                flag = False
                if n>=5:
                    print key + "截图检测状态为：" + str(result[key])
        if flag:
            break
        if n>=5:
            break
        time.sleep(1)

    return flag
    
    
    



