#coding=utf-8
import json
import unittest

import time

from utils.common.common import getConf
from utils.vnnoxLite.utils_lite import getNowTime, assertControlLog
from utils.vnnoxLite.vnnoxLite_interface import rq_command, rq_commandHistory


class Test_restart(unittest.TestCase):

    def test_restart(self):
        player_ids = ",".join(str(x).encode("utf-8") for x in json.loads(getConf("data", "lite_player")).values())
        start_time = getNowTime()
        print start_time
        task_id = 1
        ''' step1 重启 '''
        response = rq_command(task_id=task_id, player_ids=player_ids)
        print response
        '''check1: 重启命令返回'''
        self.assertTrue(response["status"] == [11312001], 'this Command is failed')
        time.sleep(20)

        for i in range(20):

            '''step2: 重启 日志查询'''
            print "第"+str(i+1)+"次查询"
            time.sleep(3)
            end_time = getNowTime()
            response = rq_commandHistory(player_ids=player_ids, ttid=1, synPlatform=1, asyPlatform=2,
                                          start_time=start_time, end_time=end_time, status='1,2', offset=0, limit=100,
                                          sort='start_time', sortType='asc')
            if response["data"]["count"] == len(json.loads(getConf("data", "lite_player")).keys()):
                print end_time
                print response
                break


        '''check2: 验证设置同步播放命令日志'''
        self.assertTrue(response["status"] == [10000001], 'this Command is failed')

        '''验证返回的日志结果'''
        assertControlLog(self, response,"设置同步播放", task_id=task_id, scheduledTaskstatus=1)



    def runTest(self):
        pass


