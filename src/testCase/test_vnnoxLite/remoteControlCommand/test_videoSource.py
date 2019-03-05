#coding=utf-8
import json
import unittest

import time

from utils.common.common import getConf
from utils.vnnoxLite.utils_lite import getNowTime, assertControlLog
from utils.vnnoxLite.vnnoxLite_interface import rq_command, rq_commandHistory


class Test_videoSource(unittest.TestCase):

    def test_inside(self):
        print json.loads(getConf("data", "lite_player")).values()
        player_ids = ",".join(str(x).encode("utf-8") for x in json.loads(getConf("data", "lite_player")).values())
        start_time = getNowTime()
        print start_time
        task_id = 9
        ''' step1 设置内部源 '''
        response = rq_command(task_id=task_id, player_ids=player_ids)
        print response
        '''check1: 设置内部源命令返回'''
        self.assertTrue(response["status"] == [11312001], 'lite 设置内部源失败')
        time.sleep(5)

        '''step2: 设置内部源 日志查询'''
        end_time = getNowTime()

        print end_time
        response = rq_commandHistory(player_ids=player_ids, ttid=4, synPlatform=1, asyPlatform=2,
                                      start_time=start_time, end_time=end_time, status='1,2', offset=0, limit=100,
                                      sort='start_time', sortType='desc')
        print response

        '''check2: 验证设置内部源命令日志'''
        self.assertTrue(response["status"] == [10000001], 'lite 获取内部源日志失败')

        '''验证返回的日志结果'''
        assertControlLog(self, response,"设置内部源", noApply=["T1-4G", "T3"],task_id=task_id, scheduledTaskstatus=1)

    def test_HDMI(self):
        print json.loads(getConf("data", "lite_player")).values()
        player_ids = ",".join(str(x).encode("utf-8") for x in json.loads(getConf("data", "lite_player")).values())
        start_time = getNowTime()
        print start_time
        task_id = 8
        ''' step1 设置HDMI源 '''
        response = rq_command(task_id=task_id, player_ids=player_ids)
        print response
        '''check1: 设置HDMI源命令返回'''
        self.assertTrue(response["status"] == [11312001], 'lite 设置HDMI源失败')
        time.sleep(5)

        '''step2: 设置HDMI源 日志查询'''
        end_time = getNowTime()

        print end_time
        response = rq_commandHistory(player_ids=player_ids, ttid=4, synPlatform=1, asyPlatform=2,
                                      start_time=start_time, end_time=end_time, status='1,2', offset=0, limit=100,
                                      sort='start_time', sortType='desc')
        print response

        '''check2: 验证设置HDMI源命令日志'''
        self.assertTrue(response["status"] == [10000001], 'lite 获取HDMI源日志失败')

        '''验证返回的日志结果'''
        assertControlLog(self, response,"设置HDMI源", noApply=["T1-4G", "T3"], task_id=task_id, scheduledTaskstatus=1, )

    def runTest(self):
        pass

if __name__ == "__main__":
    a = Test_videoSource()
    a.test_HDMI()