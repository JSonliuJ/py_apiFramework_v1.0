# -- encoding: utf-8 --
# @time:    2020/12/14 23:49
# @Author: jsonLiu
# @Email: 810030709@qq.com
# @file: test_002_login2.py
import ddt
import unittest
import json

from common.excelhandler import ExcelHandle
from config.settings import dev_settings
from common.requesthandler import RequestHandler
from middleware.db_handler import DBHandler
from middleware.get_yaml_data import yaml_data
from middleware.log_handler import logger
from config.securite_setting import SecurityCofig
from common.generate_mobilephone import GenerateMobilePhone


@ddt.ddt
class TestLogin2(unittest.TestCase):
    EH = ExcelHandle(dev_settings.test_data_path)
    data = EH.read_all_data(yaml_data['excel']['sheet'][2])

    def setUp(self):
        self.MH = DBHandler()
        self.req = RequestHandler()

    def tearDown(self):
        self.req.close_session()
        self.MH.close()

    @ddt.data(*data)
    def test_login_2(self, test_data):
        # 发送请求,json.loads json字符串转字典
        if "#mobile_phone#" in test_data["data"]:
            test_data["data"] = test_data["data"].replace("#mobile_phone#", str(SecurityCofig.mobile_phone))

        if "#pwd#" in test_data["data"]:
            test_data["data"] = test_data["data"].replace("#pwd#", SecurityCofig.pwd)
        if "*wrong_mobile_phone*" in test_data["data"]:
            while True:
                generate_phone = GenerateMobilePhone().generate_mobile_phone()
                sql = "select * from member where mobile_phone=%s;"
                db_data = self.MH.select_sql(sql, args=(generate_phone,))
                if not db_data:
                    break
            test_data["data"] = test_data["data"].replace("*wrong_mobile_phone*", generate_phone)
        if "*pwd*" in test_data["data"]:
            wrong_pwd = ''.join([SecurityCofig.pwd, '1'])
            test_data["data"] = test_data["data"].replace("*pwd*", wrong_pwd)

        # json.loads json字符串转字典
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
                               sheet_name=yaml_data['excel']['sheet'][2],
                               row=int(test_data['case_id']) + 1,
                               column=9,
                               write_value='测试通过')
        except AssertionError as e:
            logger.error("测试用例失败：{}".format(e))
            self.EH.write_back(file_name=dev_settings.test_data_path,
                               sheet_name=yaml_data['excel']['sheet'][2],
                               row=int(test_data['case_id']) + 1,
                               column=9,
                               write_value='测试失败')
            raise e


if __name__ == '__main__':
    unittest.main()
