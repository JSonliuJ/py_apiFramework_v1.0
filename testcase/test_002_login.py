# -- encoding: utf-8 --
# @time:    2020/12/5 14:18
# @Author: jsonLiu
# @Email: 810030709@qq.com
# @file: test_002_login.py
import ddt
import unittest
import json

from common.excelhandler import ExcelHandle
from config.settings import dev_settings
from common.requesthandler import RequestHandler
from middleware.db_handler import DBHandler
from middleware.get_yaml_data import yaml_data
from middleware.log_handler import logger


@ddt.ddt
class TestLogin(unittest.TestCase):
    EH = ExcelHandle(dev_settings.test_data_path)
    data = EH.read_all_data(yaml_data['excel']['sheet'][1])

    def setUp(self):
        self.MH = DBHandler()
        self.req = RequestHandler()

    def tearDown(self):
        self.req.close_session()
        self.MH.close()

    @ddt.data(*data)
    def test_login(self, test_data):
        # 发送请求,json.loads json字符串转字典
        json_data = self.req.request_handler(test_data['method'],
                                             url=(dev_settings.host + test_data['url']),
                                             json=json.loads(test_data['data']),
                                             headers=json.loads(test_data['headers']))
        # 获取预期结果
        try:
            for k, v in json.loads(test_data["expected"]).items():
                if k in json_data:
                    self.assertEqual(json_data[k], v)
            self.EH.write_back(file_name=dev_settings.test_data_path,
                               sheet_name=yaml_data['excel']['sheet'][1],
                               row=int(test_data['case_id']) + 1,
                               column=9,
                               write_value='测试通过')
        except AssertionError as e:
            logger.error("测试用例失败：{}".format(e))
            self.EH.write_back(file_name=dev_settings.test_data_path,
                               sheet_name=yaml_data['excel']['sheet'][1],
                               row=int(test_data['case_id']) + 1,
                               column=9,
                               write_value='测试失败')
            raise e


if __name__ == '__main__':
    unittest.main()
