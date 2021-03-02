# -- encoding: utf-8 --
# @time:    2020/12/5 11:46
# @Author: jsonLiu
# @Email: 810030709@qq.com
# @file: run.py
from unittestreport.HTMLTestRunnerNew import HTMLTestRunner
import os
import time
import unittest
from common.yamlhandler import YamlHandler
from config.settings import dev_settings
# 1. 初始化testloader(加载器）
loader = unittest.TestLoader()

# 加载方式1： 加载全部测试用例
# 2. suite = testloader.discover(文件夹路径,'test_*.py) 发现(加载)用例
test_case = dev_settings.test_case_path
suite = loader.discover(start_dir=test_case,pattern='test*.py')
# 其他加载方式：类名，模块名

# 3. 把想运行的用例放到指定的文件夹中
report_path = dev_settings.html_report_path
if not os.path.exists(report_path):
    os.mkdir(report_path)

# ts= datetime.now().strftime('%Y%m%d%H%M%S')
ts = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
file_name = 'api_test_{}.html'.format(ts)
file_path = os.path.join(report_path,file_name)

config_data = YamlHandler(dev_settings.conf_yaml_path).read_yaml()

# 4. 打开一个with open() as f:
with open(file_path,'wb',) as f:
    # 5.初始化运行器： runner = 运行器(f)
    runner = HTMLTestRunner(
        stream=f,
        verbosity=config_data['html_report']['verbosity'],
        title=config_data['html_report']['title'],
        description='接口自动化测试报告',
        tester=config_data['html_report']['tester']
    )
    # 6.运行测试用例 runner.run(suite)
    runner.run(suite)

if __name__ == '__main__':
    unittest.main()