# -- encoding: utf-8 --
# @time:    2020/12/20 0:42
# @Author: jsonLiu
# @Email: 810030709@qq.com
# @file: test_006_add_loan_method1.py
import json
import os
import unittest

from jsonpath import jsonpath

from lib import ddt
from common.excelhandler import ExcelHandle
from common.requesthandler import RequestHandler
from config.settings import dev_settings
from middleware.get_yaml_data import yaml_data
from middleware import helper
from middleware.helper import Context, save_token
from middleware.log_handler import logger
from middleware.db_handler import DBHandler
@ddt.ddt
class TestAddLoanMethod1(unittest.TestCase):
    EH = ExcelHandle(dev_settings.test_data_path)
    data = EH.read_all_data(yaml_data['excel']['sheet'][7])
    log_file = os.path.join(dev_settings.log_path, yaml_data['logger']['file'])

    def setUp(self):
        # 1. 数据库连接
        save_token()
        self.MH = DBHandler()
        # 2. 请求
        self.req = RequestHandler()

    def tearDown(self):
        # 3. 数据库关闭
        self.MH.close()
        # 4. 会话关闭
        self.req.close_session()

    @ddt.data(*data)
    def test_006_add_loan_method1(self, test_data):
        Authorization = Context.Authorization
        member_id = Context.member_id
        # 5. 替换member_id
        if ('#member_id#' in test_data["data"]):
            test_data["data"] = test_data["data"].replace("#member_id#", str(member_id))
        if ('*wrong_member_id*' in test_data["data"]):
            while True:
                gen_member_id = helper.generate_member_id()
                # 查询数据库，如果数据库当中存在该member_id，那么我们再生成一次，直到不存在为止
                member_sql = "SELECT * FROM member WHERE id=%s;"
                db_id_data = self.MH.select_sql(member_sql, args=(gen_member_id,))
                if (not db_id_data):
                    break
            # 错误的用户名：将member_id 加1或减1赋值给wrong_member_id
            test_data["data"] = test_data["data"].replace('*wrong_member_id*', str(gen_member_id))
            # print("我是错误的id:",test_data["data"])
        # 读取excel，得到字典
        headers = json.loads(test_data["headers"])
        # 6. 添加Authorization到headers
        headers["Authorization"] = Authorization
        # 7. 发送请求
        json_data = self.req.request_handler(test_data['method'],
                                             url=(dev_settings.host + test_data['url']),
                                             json=json.loads(test_data['data']),
                                             headers=headers)
        print(json_data)
        try:
            try:
                # 8. 第一次断言：状态码
                for k,v in json.loads(test_data["expected"]).items():
                    if k in json_data:
                        self.assertEqual(json_data[k],v)
                        self.EH.write_back(
                            file_name=dev_settings.test_data_path,
                            sheet_name=yaml_data['excel']['sheet'][7],
                            row=int(test_data['case_id']) + 1,
                            column=9,
                            write_value='测试通过')
            except AssertionError as e:
                logger.error('用例测试失败：{}'.format(e))
                self.EH.write_back(
                    file_name=dev_settings.test_data_path,
                    sheet_name=yaml_data['excel']['sheet'][7],
                    row=int(test_data['case_id']) + 1,
                    column=9,
                    write_value='测试失败')
                raise e
           # 9. 第二次断言，如果为成功用例进行数据库member_id检验，
           # 判断是否是成功用例，如果是则校验数据
            if (not json_data["code"]):
                loan_id = jsonpath(json_data,'$..id')[0]
                sql = test_data['sql_check']
                db_data = self.MH.select_sql(sql, args=(loan_id,))
                self.assertTrue(db_data)
                print(db_data)
                self.EH.write_back(
                    file_name=dev_settings.test_data_path,
                    sheet_name=yaml_data['excel']['sheet'][7],
                    row=int(test_data['case_id']) + 1,
                    column=9,
                    write_value='测试通过')
        except AssertionError as e:
            logger.error('测试用例失败：{}'.format(e))
            self.EH.write_back(
                file_name=dev_settings.test_data_path,
                sheet_name=yaml_data['excel']['sheet'][7],
                row=int(test_data['case_id']) + 1,
                column=9,
                write_value='测试失败')
            raise e


if __name__ == '__main__':
    unittest.main()