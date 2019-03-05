#coding=utf-8
import json
import unittest

import time
from utils.common.common import getConf
from utils.vnnoxLite.utils_lite import assertControlLog, getNowTime
from utils.vnnoxLite.vnnoxLite_interface import rq_commandHistory, rq_command


class Test_brightness(unittest.TestCase):

    def test_brightness(self):
        print json.loads(getConf("data", "lite_player")).values()
        player_ids = ",".join(str(x).encode("utf-8") for x in json.loads(getConf("data", "lite_player")).values())
        start_time = getNowTime(addHours=-8)
        print start_time

        ''' step1 设置亮度值 '''
        bright_value = 60
        task_id = 17
        response = rq_command(task_id=task_id, value=bright_value, player_ids=player_ids)
        print response
        '''check1: 亮度控制命令返回'''
        self.assertTrue(response["status"] == [11312001], 'lite设置亮度失败')
        time.sleep(5)


        '''step2: 亮度控制 日志查询'''
        end_time = getNowTime(addHours=-8)
        print end_time
        # time.sleep(10)
        response1 = rq_commandHistory(player_ids=player_ids, ttid=10, synPlatform=1, asyPlatform=4,
                                      start_time=start_time, end_time=end_time, status='1,2', offset=0, limit=50,
                                      sort='start_time', sortType='desc')
        print response1

        '''check2: 验证亮度控制命令日志'''
        self.assertTrue(response1["status"] == [10000001], 'lite获取亮度日志失败')

        '''验证返回的日志结果'''
        assertControlLog(self,response1,"亮度调节",ratio=bright_value,scheduledTaskstatus=1,task_id=str(task_id))

    def runTest(self):
        pass

if __name__ == "__main__":
    a = Test_brightness()
    a.test_brightness()
    # discover = unittest.TestSuite()
    # discover.addTest(CareRegister("test_careRegister"))
    # runner = unittest.TextTestRunner()
    # runner.run(discover)




