#coding=utf-8

'''
Created on 2018年11月5日

'''
import json
import unittest
from utils.common.common import getConf,setConf
from utils.vnnoxLite.vnnoxLite_interface import rq_generatePlan, rq_program


class Test_GeneratePlan(unittest.TestCase):
    '''   发布 vnnoxLite 节目 '''
    def setUp(self):
        pass

    def test_publish(self):

        '''获取第一个节目'''
        response = rq_program(search='', offset=1, limit=20, sort='update_time', sortType='desc')
        print response
        u'check'
        self.assertTrue(response["status"] == [10000001], 'lite获取节目失败')
        print response["data"]["programList"][0]["id"]
        setConf("data", "program_id", response["data"]["programList"][0]["id"])
        program_id = response["data"]["programList"][0]["id"]


        '''发布 vnnoxLite节目  '''
        player_ids = json.loads(getConf("data", "lite_player")).values()
        response = rq_generatePlan(player_id=player_ids,program_id=program_id)
        print response
        u'check'
        self.assertTrue(response["status"] == [110250010101] ,'lite发布节目失败')



    def tearDown(self):
        pass

