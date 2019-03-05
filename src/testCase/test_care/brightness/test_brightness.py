#coding=utf-8
import random
import time
import collections
import json
import datetime
import requests
import unittest
from utils.care.care_login import care_login,rq_getScreenList,rq_dobrightconfig,rq_Adjustment,rq_logList
class Test_care_brightness(unittest.TestCase):
    def setUp(self):
        pass

    def test_brightness(self):
        u'''care下发亮度配置'''

        self.param = requests.Session()
        #登录
        care_login(param=self.param,care_url ='http://care.novaicare.com',care_username='linhuajian',care_password='123456')

        u'''step1: 获取屏体列表'''
        res = rq_getScreenList(param=self.param,FilterList="",Keywords="",OrderName="screenName",OrderType="desc",PageIndex="1",PageSize="10",Status=0,sids=[])
        u'''check1: 是否获取成功 '''
        self.assertTrue(res["status"]==100000,"获取屏体失败")
        #下发命令屏体id
        sids='11160'

        CTime=datetime.datetime.now().strftime('%H:%M')
        value=str(random.randint(1,100))
        # data=collections.OrderedDict()
        # data["sids"]=sids
        # data["sensorValue"]=65534
        # data["defaultBright"]=''
        # data["thbId"]=0
        # data["rowData[]"]="@"+CTime+"@0,1,2,3,4,5,6@0@"+value+"@1@0@--"
        # data["b_Id"]=''
        # data["weekDay"]="0,1,2,3,4,5,6"
        # data["type"]=0
        # data["brightness"]=value
        # data["colorT"]=0
        # data["GammaT"]='--'
        # data["openbright"]=1
        # data["isOpenBright"]='on'
        # data["args"]=''
        data={"sid":sids,"sensorValue":65534,"defaultBright":"","thbId":0,"rowData[]":"@"+CTime+"@0,1,2,3,4,5,6@0@"+value+"@1@0@--","b_Id":"","weekDay":"0,1,2,3,4,5,6","type":0,"brightness":value,"colorT":0,"GammaT":"--","openbright":1,"args":""}



        print data

        u'''step2: 下发亮度调节配置'''
        res1 = rq_dobrightconfig(param=self.param,data=data)
        u'''check2: 是否下发成功 '''
        self.assertTrue(res1["status"]==1,"下发亮度失败")

        endTime=datetime.datetime.now().strftime("%Y-%m-%d")
        totals ={}
        total1s ={}
        bright_values={}
        bright_types={}
        results={}
        for sid in sids.split(','):

            res2=rq_Adjustment(param=self.param,sid=sid,currentPage=1,endTime=endTime,startTime=endTime,logType=0,orderName= "record_time",orderType="desc",pageSize=10)
            totals[sid]=res2["data"]["total"]

        time.sleep(8)

        for sid in sids.split(','):
            u'''step3: 亮度日志查询'''
            res3=rq_Adjustment(param=self.param,sid=sid,currentPage=1,endTime=endTime,startTime=endTime,logType=0,orderName= "record_time",orderType="desc",pageSize=10)

            total1s[sid]=res3["data"]["total"]
            bright_values[sid]=int((res3["data"]["logs"][0]["bright_value"]/2.55)+0.5)
            bright_types[sid]=res3["data"]["logs"][0]["bright_type"]
            results[sid]=res3["data"]["logs"][0]["result"]
            u'''check3: 是否下发成功 '''
            self.assertTrue(res3["status"]==100000,"查询失败")

        u'''check4: 日志校验 '''
        for key in bright_values.keys():
            self.assertTrue( total1s[key]-totals[key]==1,"无亮度调节日志")
            self.assertTrue( bright_values[key]==int(value),"亮度值不一致")
            self.assertTrue( bright_types[key]==0,"亮度调节类型不一致")
            self.assertTrue( results[key]==0,"亮度调节失败")
    def test_logList(self):
        self.param = requests.Session()
        #登录
        care_login(param=self.param,care_url ='http://172.16.80.206',care_username='test',care_password='123456')

        u'''step1: 获取屏体列表'''
        res = rq_getScreenList(param=self.param,FilterList="",Keywords="",OrderName="screenName",OrderType="desc",PageIndex="1",PageSize="100",Status=0,sids=[])
        u'''check1: 是否获取成功 '''
        self.assertTrue(res["status"]==100000,"获取屏体失败")
        endTime=datetime.datetime.now().strftime("%Y-%m-%d")
        s=0
        for i in range(len(res["data"]["ScreenList"])):
            sid = res["data"]["ScreenList"][i]["Sid"]
            u''' 离线日志查询'''
            res3=rq_logList(param=self.param,sid=sid,currentPage=1,endtime=endTime,starttime=endTime,orderName= "addtime",orderType="desc",pageSize=10)
            if res3["data"]["list"]!=[]:
                s+=1
                print json.dumps(res["data"]["ScreenList"][i]["ScreenName"])+'::'+json.dumps(res3["data"])
        print "有  "+str(s)+" :个屏体离线"




    def runTest(self):
        pass

if __name__ == "__main__":
    a = Test_care_brightness()
    a.test_logList()