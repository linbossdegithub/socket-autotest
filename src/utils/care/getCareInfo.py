#coding=utf8
'''
Created on 2018.11.28
@author: chenyongfa
'''
from constant.constant import Constant
from utils.common.common import sendGetCommand



def getCareInfo(self):
    '''
            获取终端在care的注册信息
    :param    self    必须
    :return   reult   字典      key：sn号     value:{
                                            "state":true,
                                            "serverNodes":[
                                                            {
                                                                 "label":"测试",
                                                                 "node":"t.novaicare.com"
                                                            },
                                                            {
                                                                "label":"美国节点",
                                                                "node":"care-us.novaicare.com"
                                                            },
                                                            {
                                                                "label":"中国节点",
                                                                "node":"care.novaicare.com"
                                                            }
                                                        ],
                                            "url":"t.novaicare.com",
                                            "username":"XXX",
                                            "isOnline":true
                                        }
    :example  reult = getCareInfo(self)
              reult = {'bzsa07216j0550000355': {u'username': u'chenyongfa', u'isOnline': True, u'url': u't-docker.novaicare.com', u'webSocketUrl': u'', u'state': True, u'serverNodes': [{u'node': u'care-us.novaicare.com', u'label': u'\u7f8e\u56fd'}, {u'node': u'care.novaicare.com', u'label': u'\u4e2d\u56fd'}, {u'node': u'care-sg.novaicare.com', u'label': u'\u65b0\u52a0\u5761'}]}}

    '''
    data = {}
    data["language"] = "zh-cn"
    result = sendGetCommand(self,Constant.WHAT_MONITOR,Constant.TYPE_CARE,Constant.ACTION_GET,0,data=data,timeout=12,describe="getCareInfo")
    return result


def assertCareResult(self,result,url,username,isOnline=True,state=True):
    '''
            断言获取的到care配置信息是否与预期的一致
    :param    self    必须
              url    字符串    eg：care.novaicare.com  注意不用写"http：//"
              username    字符串    care的用户名
              isOnline   bool
    :example  assertCareResult(self,"10.20.8.161","chenyongfa",True)
    '''
    flag = True
    for i in self.sns:
        li = result[i]
        if li in [Constant.ERROR,Constant.FAILED,Constant.NOAPPLY]:
            print i + ":" + str(li)
            flag = False
        elif (li["url"] != url) or (li["username"]!=username) or (li["isOnline"]!=isOnline) or (li["state"]!=state):
            print i+":"+str(li)
            flag = False
    self.assertTrue(flag,"某些屏体未在care注册成功")
    
    
    
    
    
    
    
