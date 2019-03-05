#coding=utf8
'''
Created on 2019.02.15
'''
from utils.common.common import getConf,setConf
import json
import urllib
def care_login(param,care_url ='',care_username='',care_password=''):
    '''
    登陆care
    :param1   param self.param 必须
    :param2   care_url  care地址
    :param3  care_username  care 用户名
    :param3  care_password  care 用户密码
    :return  null
    :example care_login(param=self.param,care_url ='http://care.novaicare.com',care_username='linhuajian',care_password='123456')

'''

    url = care_url+'/login/index/redirect/%252F.html'
    result = param.get(url)
    session_id = result.cookies['PHPSESSID']
    print session_id
    if session_id :
        print getConf("data", "Cookie")
        setConf("data","Cookie",'PHPSESSID='+result.cookies['PHPSESSID'])
    else:
        raise Exception("PHPSESSID is not obtained")

    u'''login check'''
    url = care_url+'/login/loginCheck'
    headers = {}
    headers['Origin'] = care_url
    headers['Referer'] = care_url+'/login/index/redirect/%252F.html'
    headers["Cookie"] = getConf("data", "Cookie")
    headers["X-Requested-With"] ="XMLHttpRequest"
    print  'Cookie:'+getConf("data", "Cookie")
    data={}
    data['username'] = care_username
    data['password'] = care_password
    result = param.request(method='get', url=url,headers=headers,params=data)
    print result.text

    u'''get authorization'''
    url = care_url+'/'
    headers = {}
    headers['Cookie'] = getConf('data','cookie')
    result = param.request(method='get', url=url, headers=headers)
    import re
    content = result.text
    authorization =  re.findall(r"value=\'(.+?)\' id=\"token\"", content)
    print 'authorization:'+str(authorization)
    authorization =  'Bearer '+ authorization[0]
    setConf('data','authorization',authorization)
    setConf('constant','care_url',care_url)
    setConf('constant','care_password',care_password)


def rq_getScreenList(param,**kwarg):
    '''
        获取care 屏体列表
        :param1   param self.param 必须
        :param2   **kwarg  FilterList="",Keywords="",OrderName="screenName",OrderType="desc",PageIndex="1",PageSize="10",Status=0,sids=[]
        :return  json
        :example res = rq_getScreenList(param=self.param,FilterList="",Keywords="",OrderName="screenName",OrderType="desc",PageIndex="1",PageSize="10",Status=0,sids=[])

'''

    url = getConf("constant", "care_url")+'/new/backend/screen/getScreenList'
    headers = {}
    headers["Authorization"] = getConf("data", "authorization")
    headers["Cookie"] = getConf("data", "cookie")
    response = param.request(method='post', url=url, headers=headers, params=kwarg,verify = False)
    print "response::" + response.text
    return json.loads(response.text)


def rq_dobrightconfig(param,data=''):
    '''亮度调节表
    :param1   param self.param 必须
    :param2  data  有序字典
                    data=collections.OrderedDict()
                    data["sensorValue"]=33458
                    data["defaultBright"]=0
                    data["sids"]=10766,11093
                    data["switch"]=1
                    data["thbId"]=0
                    data["rowData[]"]="@"+CTime+"@@0@"+value+"@1@0@--"
                    data["b_Id"]=''
                    data["weekDay"]=""
                    data["type"]=0
                    data["brightness"]=value
                    data["colorT"]=0
                    data["GammaT"]='--'
                    data["openbright"]=1
                    data["isOpenBright"]='on'
                    data["args"]=''
    :return  json
    :example res1 = rq_dobrightconfig(param=self.param,data=data)

'''
    #url = getConf("constant","care_url")+'/batchsetting/dobrightconfig'
    url = getConf("constant","care_url")+'/Screenlist/dobrightconfig'

    headers = {}
    headers["Authorization"] = getConf("data", "authorization")
    headers["Cookie"] = getConf("data", "cookie")
    headers["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
    headers["X-Requested-With"] = "XMLHttpRequest"

    data = urllib.urlencode(data)
    print data
    response = param.request(method='post',url=url,headers=headers,data=data)
    print "response::"+response.text
    return json.loads(response.text)

def rq_Adjustment(param,**kwargs):
    '''
        调节日志
        :param1   param self.param 必须
        :param2   **kwarg  sid=10766,currentPage=1,endTime=endTime,startTime=endTime,logType=0,orderName= "record_time",orderType="desc",pageSize=10
        :return  json
        :example res3=rq_Adjustment(param=self.param,sid=10766,currentPage=1,endTime=endTime,startTime=endTime,logType=0,orderName= "record_time",orderType="desc",pageSize=10)

'''

    data = urllib.urlencode(kwargs)
    url = getConf("constant","care_url")+'/new/backend/brightness/logs?'+data
    headers = {}
    headers["Authorization"] = getConf("data", "authorization")
    headers["Cookie"] = getConf("data", "cookie")
    response = param.request(method='get',url=url,headers=headers)



def rq_logList(param,**kwargs):
    url = getConf("constant","care_url")+'/new/backend/screen/logList'
    headers = {}
    headers["Authorization"] = getConf("data", "authorization")
    headers["Cookie"] = getConf("data", "cookie")
    response = param.request(method='POST',url=url,headers=headers,json=kwargs)
    #print "response::"+response.text
    return json.loads(response.text)







