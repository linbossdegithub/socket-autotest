#coding=utf8
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append(os.path.abspath('../'))
import argparse
import time
from HTMLTestRunner import HTMLTestRunner
from run.addTestCase import add_sys_testCase, add_press_restart

from utils.common.common import setConf, getConf
from utils.login.search_login import searchT


def createHTML(discover):
    # 创建html报告

    nowTime = time.strftime('%Y-%m-%d %H_%M_%S', time.localtime(time.time()))
    fileName = '../report/' + nowTime + '_result.html'
    stream = open(fileName, 'wb')
    runner = HTMLTestRunner(stream=stream,
                            title=u"终端自动化测试报告",
                            description=u"用例执行情况",
                            verbosity=2)
    runner.run(discover)
    stream.close()

if __name__ == "__main__":
    parse = argparse.ArgumentParser(description="terminal test")
    parse.add_argument('-sn', nargs='?', type=str, help="sn,eg: 256,3456,12212")
    parse.add_argument('-password', nargs='?', type=str, help="input password")
    parse.add_argument('-email', nargs='?', type=str, help="input email")
    args = parse.parse_args()

    if args.sn:
        setConf("constant", "data", args.sn)
    else:
        setConf("constant", "data", '')
    if args.password:
        setConf("constant", "login_password", args.password)
    # else:
    #     setConf("constant", "login_password", '123456')

    if args.email:
        setConf("constant", "email", args.email)
    else:
        setConf("constant", "email", '18294447754@163.com')

    # flag = searchT()
    # if not flag:
    #     raise RuntimeError("有未搜到的终端")

    '''添加测试用例'''
    discover1 = add_sys_testCase()
    # discover2 = add_press_restart()

    '''运行并生成HTML测试报告'''
    createHTML(discover1)