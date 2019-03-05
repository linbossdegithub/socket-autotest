#coding=utf-8
import json
import unittest

import time

from utils.common.common import getConf
from utils.vnnoxLite.utils_lite import getNowTime, assertControlLog
from utils.vnnoxLite.vnnoxLite_interface import rq_command, rq_commandHistory


class Test_synchronousPlay(unittest.TestCase):

    def test_synchronousPlay(self):
        player_ids = ",".join(str(x).encode("utf-8") for x in json.loads(getConf("data", "lite_player")).values())
        start_time = getNowTime()
        print start_time
        task_id = 4
        ''' step1 设置同步播放 '''
        response = rq_command(task_id=task_id, player_ids=player_ids)
        print response
        '''check1: 同步播放命令返回'''
        self.assertTrue(response["status"] == [11312001], 'LITE 设置同步播放失败')
        time.sleep(5)

        '''step2: 同步播放 日志查询'''
        end_time = getNowTime()

        print end_time
        response = rq_commandHistory(player_ids=player_ids, ttid=3, synPlatform=1, asyPlatform=2,
                                      start_time=start_time, end_time=end_time, status='1,2', offset=0, limit=100,
                                      sort='start_time', sortType='desc')
        print response

        '''check2: 验证设置同步播放命令日志'''
        self.assertTrue(response["status"] == [10000001], 'lite 获取同步播放日志失败')

        '''验证返回的日志结果'''
        assertControlLog(self, response,"设置同步播放", task_id=task_id, scheduledTaskstatus=1)



    def runTest(self):
        pass


