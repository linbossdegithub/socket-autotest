#coding=utf-8
import json
import unittest

import time

from utils.common.common import getConf
from utils.vnnoxLite.utils_lite import getNowTime, assertControlLog
from utils.vnnoxLite.vnnoxLite_interface import rq_command, rq_commandHistory


class Test_screenStatus(unittest.TestCase):

    def test_closeScreen(self):
        print json.loads(getConf("data", "lite_player")).values()
        player_ids = ",".join(str(x).encode("utf-8") for x in json.loads(getConf("data", "lite_player")).values())
        start_time = getNowTime()
        print start_time
        task_id = "3"
        ''' step1 关屏 '''
        response = rq_command(task_id=task_id, player_ids=player_ids)
        print response
        '''check1: 关屏命令返回'''
        self.assertTrue(response["status"] == [11312001], 'lite关屏命令失败')
        time.sleep(5)

        '''step2: 关屏 日志查询'''
        end_time = getNowTime()

        print end_time
        response = rq_commandHistory(player_ids=player_ids, ttid=2, synPlatform=1, asyPlatform=2,
                                      start_time=start_time, end_time=end_time, status='1,2', offset=0, limit=100,
                                      sort='start_time', sortType='desc')
        print response

        '''check2: 验证设置关屏命令日志'''
        self.assertTrue(response["status"] == [10000001], 'lite获取屏幕状态日志失败')

        '''验证返回的日志结果'''
        assertControlLog(self, response,"关屏", task_id=task_id, scheduledTaskstatus=1)

    def test_openScreen(self):
        print json.loads(getConf("data", "lite_player")).values()
        player_ids = ",".join(str(x).encode("utf-8") for x in json.loads(getConf("data", "lite_player")).values())
        start_time = getNowTime()
        print start_time
        task_id = "2"
        ''' step1 开屏 '''
        response = rq_command(task_id=task_id, player_ids=player_ids)
        print response
        '''check1: 开屏命令返回'''
        self.assertTrue(response["status"] == [11312001], 'lite开屏命令失败')
        time.sleep(5)

        '''step2: 开屏 日志查询'''
        end_time = getNowTime()

        print end_time
        response = rq_commandHistory(player_ids=player_ids, ttid=2, synPlatform=1, asyPlatform=2,
                                      start_time=start_time, end_time=end_time, status='1,2', offset=0, limit=100,
                                      sort='start_time', sortType='desc')
        print response

        '''check2: 验证设置开屏命令日志'''
        self.assertTrue(response["status"] == [10000001], 'lite获取屏幕状态日志失败')

        '''验证返回的日志结果'''
        assertControlLog(self, response,"开屏", task_id=task_id, scheduledTaskstatus=1)


    def runTest(self):
        pass

