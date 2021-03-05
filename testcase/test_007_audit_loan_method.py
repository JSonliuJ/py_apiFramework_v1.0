# -- encoding: utf-8 --
# @time:    	2020/12/23 23:35
# @Author: 		jsonLiu
# @Email:  		810030709@qq.com
# @file: 		test_007_audit_loan_method.py
import json
import os
import unittest
from jsonpath import jsonpath
from common.excelhandler import ExcelHandle
from common.requesthandler import RequestHandler
from config.settings import dev_settings
from lib import ddt
from middleware import helper
from middleware.db_handler import DBHandler
from middleware.get_yaml_data import yaml_data
from middleware.helper import Context, save_token, save_admin_token, save_added_id
from middleware.log_handler import logger


@ddt.ddt
class TestAuditLoanMethod(unittest.TestCase):
    EH = ExcelHandle(dev_settings.test_data_path)
    data = EH.read_all_data(yaml_data['excel']['sheet'][9])
    log_file = os.path.join(dev_settings.log_path, yaml_data['logger']['file'])

    def setUp(self):
        # 1. 数据库连接
        self.MH = DBHandler()
        # 2. 请求
        self.req = RequestHandler()
        save_added_id()
        save_token()
        save_admin_token()

    def tearDown(self):
        # 3. 数据库关闭
        self.MH.close()
        # 4. 会话关闭
        self.req.close_session()

    @ddt.data(*data)
    def test_007_audit_loan_method(self, test_data):
        if '#loan_id#' in test_data["data"]:
            test_data["data"] = test_data["data"].replace("#loan_id#", str(Context.add_loan_id))
        if '*wrong_loan_id*' in test_data["data"]:
            while True:
                gen_add_loan_id = helper.generate_add_loan_id()
                # 查询数据库，如果数据库当中存在该member_id，那么我们再生成一次，直到不存在为止
                sql = "SELECT id FROM loan WHERE id=%s;"
                db_id_data = self.MH.select_sql(sql, args=(gen_add_loan_id,))
                if not db_id_data:
                    break
            # 错误的借款id：将loan_id 加1或减1赋值给loan_id
            test_data["data"] = test_data["data"].replace('*wrong_loan_id*', str(gen_add_loan_id))
        if "*not_to_audit_loan_id*" in test_data["data"]:
            sql = "select * from loan where status <> 1 limit 1;"
            not_to_audit_id_data = self.MH.select_sql(sql)
            if not_to_audit_id_data:
                test_data["data"] = test_data["data"].replace('*not_to_audit_loan_id*', str(not_to_audit_id_data["id"]))
        # 读取excel，得到字典
        headers = json.loads(test_data["headers"])
        if "member_audit" in test_data["module_name"]:
            headers["Authorization"] = Context.Authorization
        if "admin_audit" in test_data["module_name"]:
            headers["Authorization"] = Context.admin_Authorization
        # # 6. 添加Authorization到headers
        # # 7. 发送请求
        json_data = self.req.request_handler(test_data['method'],
                                             url=(dev_settings.host + test_data['url']),
                                             json=json.loads(test_data['data']),
                                             headers=headers)
        # print(json_data)
        try:
            try:
                # 8. 第一次断言：状态码
                for k, v in json.loads(test_data["expected"]).items():
                    if k in json_data:
                        self.assertEqual(json_data[k], v)
                        self.EH.write_back(
                            file_name=dev_settings.test_data_path,
                            sheet_name=yaml_data['excel']['sheet'][9],
                            row=int(test_data['case_id']) + 1,
                            column=9,
                            write_value='测试通过')
            except AssertionError as e:
                logger.error('用例测试失败：{}'.format(e))
                self.EH.write_back(
                    file_name=dev_settings.test_data_path,
                    sheet_name=yaml_data['excel']['sheet'][9],
                    row=int(test_data['case_id']) + 1,
                    column=9,
                    write_value='测试失败')
                raise e
            # 9. 第二次断言，如果为成功用例进行数据库member_id检验，
            # 判断是否是成功用例，如果是则校验数据
            if not json_data["code"]:
                if json_data["data"]:
                    loan_id = jsonpath(json_data, '$..id')[0]
                    sql = test_data['sql_check']
                    db_data = self.MH.select_sql(sql, args=(loan_id,))
                    if "true" in test_data["data"]:
                        self.assertEqual(db_data["status"], 2)
                    if "false" in test_data["data"]:
                        self.assertEqual(db_data["status"], 5)
                    print(db_data["status"])
                    self.EH.write_back(
                        file_name=dev_settings.test_data_path,
                        sheet_name=yaml_data['excel']['sheet'][9],
                        row=int(test_data['case_id']) + 1,
                        column=9,
                        write_value='测试通过')
        except AssertionError as e:
            logger.error('测试用例失败：{}'.format(e))
            self.EH.write_back(
                file_name=dev_settings.test_data_path,
                sheet_name=yaml_data['excel']['sheet'][9],
                row=int(test_data['case_id']) + 1,
                column=9,
                write_value='测试失败')
            raise e


if __name__ == '__main__':
    unittest.main()
