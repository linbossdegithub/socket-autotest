#coding=utf-8

'''
Created on 2018年11月5日

'''
import json
import unittest
from utils.common.common import getConf,setConf
from utils.vnnoxLite.vnnoxLite_interface import rq_clearMedia
class ClearMedia(unittest.TestCase):
    '''   监控 媒体清理 '''
    def setUp(self):
        pass

    def test_a(self):
        '''   监控 媒体清理   不包括清理正在播放的媒体   '''
        player_ids = json.loads(getConf("data", "lite_player")).values()
        response = rq_clearMedia(scope=1,player_ids=player_ids, type="CLEAR_MEDIA")
        print response
        u'check'
        self.assertTrue(response["status"] == [11312001] ,'lite清理媒体失败')

    def test_b(self):
        '''   监控 媒体清理   清理所有媒体   '''
        player_ids = json.loads(getConf("data", "lite_player")).values()
        response = rq_clearMedia(scope=99,player_ids=player_ids,type="CLEAR_MEDIA")
        print response
        u'check'
        self.assertTrue(response["status"] == [11312001] ,'lite清理所有媒体失败')

    def tearDown(self):
        pass
    def runTest(self):
        pass


# if __name__ == "__mian__":
#     a = ClearMedia()
#     a.test_a()

