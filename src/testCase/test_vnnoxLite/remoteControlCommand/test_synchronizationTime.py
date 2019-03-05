#coding=utf-8

'''
Created on 2018年11月5日

'''
import json
import unittest
from utils.common.common import getConf,setConf
from utils.login.search_login import logIns, logout
from utils.timeSyn.getTerminalTime import getTimeConfig, getTimeModel
from utils.vnnoxLite.utils_lite import assertTimeModel
from utils.vnnoxLite.vnnoxLite_interface import rq_correctTime
class CorrectTime(unittest.TestCase):
    '''   对时 '''
    def setUp(self):
        logIns(self)



    def test_loral(self):
        '''   射频 对时  '''
        player_ids = ",".join(str(x).encode("utf-8") for x in json.loads(getConf("data", "lite_player")).values())
        response = rq_correctTime(type=2,nodeUrl='cn',player_ids=player_ids,timezone ="Asia/Shanghai")
        print response
        u'check'
        self.assertTrue(response["status"] == [10000001] ,'lite 设置射频对时失败')
        assertTimeModel(self, model=2)

    def test_manual(self):
        '''   手动 对时  '''
        player_ids = ",".join(str(x).encode("utf-8") for x in json.loads(getConf("data", "lite_player")).values())
        response = rq_correctTime(type=3,nodeUrl='cn',player_ids=player_ids,timezone ="Asia/Shanghai")
        print response
        u'check'
        self.assertTrue(response["status"] == [10000001] ,'lite 设置手动对时失败')
        assertTimeModel(self, model=3)

    def test_NTP_cn(self):
        '''   NTP 对时   '''
        player_ids = ",".join(str(x).encode("utf-8") for x in json.loads(getConf("data", "lite_player")).values())
        response = rq_correctTime(type=1,nodeUrl='cn',player_ids=player_ids,timezone ="Asia/Shanghai")
        print response
        u'check'
        self.assertTrue(response["status"] == [10000001] ,'lite 设置NTP对时失败')

        assertTimeModel(self,model=1)


    def test_NTP_us(self):
        '''   NTP 对时   '''
        player_ids = ",".join(str(x).encode("utf-8") for x in json.loads(getConf("data", "lite_player")).values())
        response = rq_correctTime(type=1,nodeUrl='us',player_ids=player_ids,timezone ="Asia/Shanghai")
        print response
        u'check'
        self.assertTrue(response["status"] == [10000001] ,'lite 设置NTP对时失败')

        assertTimeModel(self,model=1)



    def tearDown(self):
        logout(self)

