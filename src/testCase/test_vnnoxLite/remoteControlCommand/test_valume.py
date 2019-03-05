#coding=utf-8
import json
import unittest

import time

import datetime

from utils.common.common import getConf
from utils.vnnoxLite.utils_lite import assertControlLog, getNowTime
from utils.vnnoxLite.vnnoxLite_interface import rq_commandHistory, rq_command


class Test_valume(unittest.TestCase):

    def test_valume(self):
        print json.loads(getConf("data", "lite_player")).values()
        player_ids = ",".join(str(x).encode("utf-8") for x in json.loads(getConf("data", "lite_player")).values())
        start_time = getNowTime()
        print start_time

        ''' step1 设置音量值 '''
        valume_value = 50
        task_id = 16
        response = rq_command(task_id=task_id, value=valume_value, player_ids=player_ids)
        print response
        '''check1: 音量控制命令返回'''
        self.assertTrue(response["status"] == [11312001], 'lite 音量调节失败')
        time.sleep(5)


        '''step2: 音量控制 日志查询'''
        end_time = getNowTime()
        print end_time
        response = rq_commandHistory(player_ids=player_ids, ttid=9, synPlatform=1, asyPlatform=4,
                                      start_time=start_time, end_time=end_time, status='1,2', offset=0, limit=100,
                                      sort='start_time', sortType='desc')
        print response

        '''check2: 验证音量控制命令日志'''
        self.assertTrue(response["status"] == [10000001], 'lite 获取音量调节日志失败')

        '''验证返回的日志结果'''
        assertControlLog(self,response,"音量调节",ratio=valume_value,scheduledTaskstatus=1,task_id=task_id)

    def runTest(self):
        pass




