# -- encoding: utf-8 --
# @time:    2020/12/5 12:11
# @Author: jsonLiu
# @Email: 810030709@qq.com
# @file: settings.py
import os

class Settings:
   # 项目路径
   root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
   # dir_path = os.path.split(os.path.abspath(__file__))[0]
   # 测试数据路径
   test_data_path = os.path.join(root_path,'testdata','casedata.xlsx')
   # 测试用例路径
   test_case_path = os.path.join(root_path,'testcase')
   # 日志路径
   log_path = os.path.join(root_path,'log')
   # html报告路径
   html_report_path = os.path.join(root_path,'htmlreport')
   # conf配置文件路径
   conf_path = os.path.join(root_path,'conf')
   # yaml文件路径
   conf_yaml_path = os.path.join(conf_path,'config.yaml')
class DevSettings(Settings):
        host = 'http://120.78.128.25:8766/futureloan'

dev_settings = DevSettings()

if __name__ == '__main__':
    dev_settings = DevSettings().host
