# -- encoding: utf-8 --
# @time:    2020/12/5 14:18
# @Author: jsonLiu
# @Email: 810030709@qq.com
# @file: test_001_register.py
import ddt
import unittest
import json
import os
from mock import Mock
from common.excelhandler import ExcelHandle
from config.settings import dev_settings
from common.requesthandler import RequestHandler

from  common.generate_mobilephone import GenerateMobilePhone

from middleware.get_yaml_data import yaml_data
from middleware.log_handler import logger
from middleware.db_handler import DBHandler
@ddt.ddt
class TestRegister(unittest.TestCase):
    EH = ExcelHandle(dev_settings.test_data_path)
    data = EH.read_all_data(yaml_data['excel']['sheet'][0])

    def setUp(self):
        self.MH = DBHandler()
        self.req = RequestHandler()
    def tearDown(self):
        self.req.close_session()
        self.MH.close()
    @ddt.data(*data)
    def test_register(self,test_data):
        if '#exist_phone#' in test_data['data']:
            # 直接查询数据库，如果数据库当中存在该手机号，那么我们直接使用这个手机号
            db_data1 = self.MH.select_sql("select * from member limit 1;")
            if db_data1:
                test_data['data'] = test_data['data'].replace('#exist_phone#', db_data1['mobile_phone'])
            else:
                # 方式1：随机生成一个手机号，数据库中还是不存在的，注册成功
                # 方式2：直接通过插入数据库
                pass
            # test_data['data'] = test_data['data'].replace('##exist_phone##',mobile)
        if '#new_phone#' in test_data['data']:
            while True:
                gen_phone = GenerateMobilePhone().generate_mobile_phone()
                # 方式1：查询数据库，如果数据库当中存在该手机号，那么我们再生成一次，直到不存在为止
                # 方式2：直接查询数据库，随机找一个，直接使用该号码替换
                db_data2 = self.MH.select_sql("select * from member where mobile_phone=%s;",args=(str(gen_phone),))
                if not db_data2:
                    break
            test_data['data'] =test_data['data'].replace('#new_phone#',str(gen_phone))

        # 客户端mock模拟
        # self.req.request_handler = Mock(return_value=test_data['expected'])
        # 发送请求,json.loads json字符串转字典
        json_data = self.req.request_handler(test_data['method'],
                                             url=(dev_settings.host+test_data['url']),
                                             json=json.loads(test_data['data']),
                                             headers=json.loads(test_data['headers']))
        actual = json_data['code']
        # 获取预期结果
        # excepted = eval(test_data['expected'])['code']
        excepted_result = test_data['expected']
        # 如果断言失败，将错误记录保存到logge ,抛出assertError
        try:
            self.assertEqual(actual,excepted_result)
            self.EH.write_back(
                               file_name =dev_settings.test_data_path,
                               sheet_name=yaml_data['excel']['sheet'][0],
                               row=int(test_data['case_id'])+ 1,
                               column=9,
                               write_value='测试通过')
        except AssertionError as e:
            logger.error("测试用例失败：{}".format(e))
            self.EH.write_back(file_name = dev_settings.test_data_path,
                               sheet_name=yaml_data['excel']['sheet'][0],
                               row=int(test_data['case_id']) + 1,
                               column=9,
                               write_value='测试失败')
            raise e
if __name__ == '__main__':
    # json和字典转换最好不用eval
    unittest.main()